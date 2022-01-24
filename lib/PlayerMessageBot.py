import re
import discord
from discord.ext import commands

from lib.PompSettings import PompSettings
from lib.votes import Votes


class MessageValidationException(Exception):
    def __init__(self, message, show_to_sender=True):
        self.__show = show_to_sender
        super().__init__(message)

    def show_to_sender(self):
        return self.__show


class MessageValidator:
    def __init__(self, message, sender, settings: PompSettings, votes, myguild):
        self.message_expr = re.compile(
            settings.get_value("VOTE_TRIGGER"), re.IGNORECASE
        )
        self.cancel_expr = re.compile(
            settings.get_value("WITHDRAW_VOTE_TRIGGER"), re.IGNORECASE
        )
        self.sender = sender
        self.message = message
        self.settings = settings
        self.votes = votes
        self.guild = myguild

    def is_remove_voting_message(self):
        return self.cancel_expr.match(self.message.content.lower())

    def is_voting_message(self):
        return self.message_expr.match(self.message.content.lower())

    def validate_remove_vote(self):
        if self.settings.get_flag("CAN_WITHDRAW_VOTE"):
            if self.votes.get_last_voted_for(self.message.author):
                return True
            else:
                raise MessageValidationException(
                    _("Het spijt mij, u heeft geen openstaande stem om te verwijderen")
                )
        else:
            raise MessageValidationException(
                _(
                    "Nee, het spijt mij, het is mij niet toegestaan uw stem weer te verwijderen"
                )
            )

    def get_member_for_flat_name(self, name):
        votee = None
        for member in self.guild.members:
            if member.display_name.lower() == name.lower():
                votee = member
                break
        return votee

    def get_member_for_index(self, index):
        votee = None
        if len(self.guild.members) >= index:
            votee = self.guild.members[index - 1]
        return votee

    def get_votee_from_message(self):
        votee = None

        # It could be that voting is limited to a single channel
        if (
            self.message.guild
            and self.settings.get_flag("VOTING_CHANNEL_ONLY")
            and self.message.channel is not self.settings.get_vote_channel()
        ):
            raise MessageValidationException(
                _(
                    "Het spijt mij, maar stemmen in andere kanalen dan het stem kanaal is niet toegestaan"
                ),
                False,
            )

        if len(self.message.mentions) == 0:
            # Walrus operator not in 3.7. Walrus sad.
            result = re.search("([0-9]+)", self.message.content)

            # If there was an @ but no mention, lets attempt to fuzzy match
            if "@" in self.message.content:
                result = re.search("@&*([\\w]+)", self.message.content).group(1)
                votee = self.get_member_for_flat_name(result)
            # There might also be a number somehwere in there
            elif result:
                index = int(result.group(1))
                votee = self.get_member_for_index(index)

            # Nothing worked?
            if not votee:
                # Private message and missing member? Show a list.
                if not self.message.guild:
                    allmembers = self.guild.members
                    names = [
                        f"{allmembers.index(member) + 1}) {member.display_name}\n"
                        for member in allmembers
                    ]
                    raise MessageValidationException(
                        _(
                            "Oh, hoogste aller machten, het spijt mij, ik herken de naam niet. Maar wellicht kunt u "
                            "uw keuze duiden met een cijfer? Bijvoorbeeld 'ik stem 1'?\n%s "
                        )
                        % {"".join(names)}
                    )
                else:
                    raise MessageValidationException(
                        _(
                            "Oh, hoogster aller machten, het spijt mij, ik herken de naam niet die u gebruikt. "
                            "Vergeet u niet om uw stem vooraf te laten gaan door een @-teken? Bijvoorbeeld @Pavi? "
                        )
                    )
        elif len(self.message.mentions) > 1:
            raise MessageValidationException(
                _(
                    "Oh, hoogster aller machten, hoe gul u ook bent, ik herinner u graag dat u slecht op "
                    "een enkel persoon kunt stemmen"
                )
            )
        else:
            votee = self.message.mentions[0]

        if votee == self.sender and not self.settings.get_flag("CAN_VOTE_SELF"):
            raise MessageValidationException(
                _(
                    "Het spijt mij. De machten hebben bepaald dat u niet op zichzelf kunt stemmen"
                )
            )
        elif votee == self.settings.get_bot_member():
            raise MessageValidationException(_("Oh nee, nee, alstublieft niet!"))

        if not self.votes.is_open():
            raise MessageValidationException(
                _(
                    "Het spijt mij, maar de almachtige heeft besloten dat er nu niet gestemd kan worden!"
                )
            )

        if self.message.guild and not self.settings.get_flag("PUBLIC_VOTING"):
            raise MessageValidationException(
                _(
                    "Ik kan uw stem niet aannemen, ik verzoek u vriendelijk om uw stemmen direct aan mij te sturen in "
                    "een persoonlijk bericht"
                )
            )

        if not self.message.guild and not self.settings.get_flag("PRIVATE_VOTING"):
            raise MessageValidationException(
                _(
                    "Ik kan uw stem niet in het geniep aannemen, ik verzoek u vriendelijk om uw stem openbaar te plaatsen"
                )
            )

        if not votee:
            votee = self.message.mentions[0]
        return votee


class PlayerMessageBot(commands.Cog):
    def __init__(self, bot, votes, settings: PompSettings):
        self.bot = bot
        self.votes = votes
        self.settings = settings
        self.prayer_expr = re.compile(
            settings.get_value("PRAYER_SOUND_TRIGGER"), re.IGNORECASE
        )

    async def publish_standings(self):
        if self.votes.get_current_votes():
            result = Votes.get_formatted_standing(self.votes.get_current_votes())
        else:
            result = _("*Op dit moment zijn er geen stemmen!*")
        self.bot.dispatch("yell", result)

    def get_member_for_user(self, user):
        for member in self.settings.get_guild().members:
            if member == user:
                return member
        raise Exception(f"Insane. Could not find user {user.name} in my server!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        voter = self.get_member_for_user(message.author)

        # VERY inappropriately placed code. Sorry.
        if self.settings.get_flag("PRAYER_SOUNDS_ENABLED") and self.prayer_expr.match(
            message.content
        ):
            self.bot.dispatch("intro", self.settings.get_value("PRAYER_SOUND"))
            return

        # I should keep this object instead of recreating it every message
        ms = MessageValidator(
            message, voter, self.settings, self.votes, self.settings.get_guild()
        )

        if ms.is_remove_voting_message():
            try:
                ms.validate_remove_vote()
                self.votes.remove_vote(voter)
                await message.reply(_("Ik heb uw stem op uw verzoek verwijderd"))
                await self.publish_standings()
            except MessageValidationException as e:
                if e.show_to_sender():
                    await message.reply(str(e))
                return
        elif ms.is_voting_message():
            try:
                votee = ms.get_votee_from_message()
                # Private messages are outside of the context of a server, so we get a "user" and not a "member"
                if type(votee) == discord.user.User:
                    votee = self.get_member_for_user(votee)

                await message.reply(_("Ik noteer uw stem op %s") % votee.display_name)
                self.votes.vote_for(voter, votee)
                await self.publish_standings()

            except MessageValidationException as e:
                if e.show_to_sender():
                    await message.reply(str(e))
                return

# bot.py
import os
import re

from votes import Votes
import discord
from dotenv import load_dotenv

load_dotenv()

# Setting up some globals
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
votes = Votes()
message_expr = re.compile(os.environ["VOTE_TRIGGER"])

# These will be set in the startup function
standing_channelid = False
myguild = False

# Convenience methode to get a member object from a user object
# A "member" is a subclass of a "user" but is in a guild and for
# example, has a nick name which we use for display purposes.
def get_member_for_user(user):
    for member in myguild.members:
        if member == user:
            return member
    raise Exception(f"Insane. Could not find user {user.name} in my server!")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    global standing_channelid
    all_channels = client.get_all_channels()
    for channel in all_channels:
        if channel.name == os.getenv("VOTING_CHANNEL"):
            standing_channelid = channel.id
            print(f"Publishing standings to channel " + channel.name)
            break
    if not standing_channelid:
        raise Exception("Could not find channel for channel name " + os.getenv("VOTING_CHANNEL"))

    global myguild
    myguild = client.guilds[0]
    print("Connected to server " + myguild.name)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welkom op de kleine-goden discord server!'
    )


async def publish_standings():
    channel = client.get_channel(standing_channelid)
    await channel.send(votes.format_votes(votes.get_current_votes()))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message_expr.match(message.content.lower()):
        if len(message.mentions) == 0:
            if "@" in message.content:
                await message.reply(
                    "Oh, hoogster aller machten, het spijt mij, ik herken de naam niet die u gebruikt na uw apestaart teken.")
            else:
                await message.reply("Oh, hoogster aller machten, ik herinner u graag dat u stemmen kunt uitbrengen "
                                    "door te verwijzen naar de naam van uw stem met voorgaand een @. U zou "
                                    "bijvoorbeeld @Psychopomp kunnen gebruiken, hoewel Pavi mij direct zou "
                                    "neerbliksemen al zou ik die stem aannemen van u.")
        elif len(message.mentions) > 1:
            await message.reply("Oh, hoogster aller machten, hoe gul u ook bent, ik herinner u graag dat u slecht op "
                                "één persoon kunt stemmen")
        elif message.mentions[0] == client.user:
            await message.reply("Oh, hoogster aller machten, hoe gul u ook bent, ik weiger uw stem en hoop zo de "
                                "toorn van mijn meester Pavi te vermijden")
        else:
            try:
                votee = message.mentions[0]

                # Private messages are outside of the context of a server, so we get a "user"  and not a "member"
                if type(votee) == discord.user.User:
                    votee = get_member_for_user(votee)

                if message.guild and os.environ["PUBLIC_VOTING"] != "true":
                    await message.reply("Ik kan uw stem niet aannemen, ik verzoek u vriendelijk om uw stemmen direct aan mij te sturen in een privé bericht" )
                elif os.environ["PRIVATE_VOTING"] != "true":
                    await message.reply("Ik kan uw stem niet aannemen, ik verzoek u vriendelijk om uw stem openbaar te plaatsen")
                else:
                    await message.reply(f"Ik noteer uw stem op {votee.display_name}")
                    votes.vote_for(get_member_for_user(message.author), votee)
                    await publish_standings()
            except Exception as e:
                print(e)
                await message.reply(f"Oh nee! Er ging iets mis in het verwerken van uw stem. Hij is niet aangenomen, ik ben even aan het kijken wat er aan de hand is!")


client.run(os.getenv('DISCORD_TOKEN'))


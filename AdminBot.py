import discord
from discord.ext import commands

from PompSettings import PompSettings
from votes import Votes


class AdminBot(commands.Cog):
    def __init__(self, bot, votes, settings: PompSettings):
        self.bot = bot
        self.votes = votes
        self.settings = settings

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        result = ">>> Current status:\n"
        result += f"- Voting is {'open' if self.votes.is_open() else 'closed'}"
        await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        result = "```\n"
        flags = self.settings.get_all_settings()
        for flag, value in flags:
            result += f"{flag.ljust(30)}{value}\n"
        result += "```"
        await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def votes(self, ctx, command):
        accepted = ["clean", "standing", "show", "open", "close"]
        if command not in accepted:
            await ctx.send(f'Votes {command} was unknown. I only know of {".".join(accepted)}')

        if command == "clean":
            self.votes.clean()
            await ctx.send('Okay, all votes were removed')
        elif command == "standing":
            channel = self.settings.get_vote_channel()
            result = Votes.get_formatted_standing(self.votes.get_current_votes())
            await channel.send(result)
        elif command == "show":
            result = Votes.get_formatted_votes(self.votes.get_current_votes(), self.votes.get_vote_set())
            await ctx.send(result)
        elif command == "open":
            self.votes.open_voting()
            await ctx.send("Voting is now enabled")
            channel = self.settings.get_vote_channel()
            await channel.send("Het doet mij deugd u te mogen melden dat stemmen vanaf nu is toegestaan")
        elif command == "close":
            self.votes.close_voting()
            await ctx.send("Voting is now disabled")
            channel = self.settings.get_vote_channel()
            await channel.send("Vanaf heden is het niet mogelijk om te stemmen")
        else:
            await ctx.send('Unknown command..')




import discord
from discord.ext import commands

from PompSettings import PompSettings
from votes import Votes


class AdminBot(commands.Cog):
    def __init__(self, bot, votes, settings: PompSettings):
        self.bot = bot
        self.votes = votes
        self.settings = settings

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print("Oh man ze praten tegen mij2!")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        await ctx.send('boop')


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def votes(self, ctx, command):
        accepted = ["clean", "standing", "show", "start", "stop"]
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
        else:
            await ctx.send('boop')




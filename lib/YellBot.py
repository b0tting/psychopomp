from discord.ext import commands

from lib.PompSettings import PompSettings


class YellBot(commands.Cog):
    def __init__(self, bot, votes, settings: PompSettings):
        self.bot = bot
        self.votes = votes
        self.settings = settings

    @commands.Cog.listener()
    async def on_yell(self, yelling):
        channel = self.settings.get_vote_channel()
        await channel.send(":star: " + yelling)

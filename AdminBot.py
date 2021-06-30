import os

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
    async def intro(self, ctx, command="list", commandparameter=""):
        if command == "list":
            arr = os.listdir('./mp3')
            result = "On the MP3 menu I have:\n"
            for ar in arr:
                result += f"- {ar}\n"
            await ctx.send(result)
        elif command == "play":
            if not commandparameter.endswith(".mp3"):
                commandparameter += ".mp3"
            self.bot.dispatch("intro", commandparameter)
        elif command == "pause":
            introbot = self.bot.get_cog('IntroBot')
            await introbot.pause()
        elif command == "resume":
            introbot = self.bot.get_cog('IntroBot')
            await introbot.resume()

    async def send_settings(self, ctx):
        result = "```\n"
        flags = self.settings.get_all_settings()
        for flag, value in flags:
            result += f"{flag.ljust(30)}{value}\n"
        result += "```"
        await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        result = "```\n"
        result += f"- Voting is {'open' if self.votes.is_open() else 'closed'}\n"
        timerbot = self.bot.get_cog('TimerBot')
        running = timerbot.timer and not timerbot.timer.done
        result += f"- Timer is {'running' if running else 'paused' if timerbot.minutesleft > 0 else 'done'}\n"
        if running or timerbot.minutesleft > 0:
            result += f"- Timer has {timerbot.minutesleft} minutes left (imprecise!)\n"
        result += "```\n"
        await ctx.send(result)

    async def send_settings(self, ctx):
        result = "```\n"
        flags = self.settings.get_all_settings()
        for flag, value in flags:
            result += f"{flag.ljust(30)}{value}\n"
        result += "```"
        await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx, command="show", commandparameter="", commandvalue=""):
        accepted = ["show", "set", "servers"]
        if command not in accepted:
            await ctx.send(f'Settings {command} was unknown. I only know the following commands: {", ".join(accepted)}')
            return

        if command == "show":
            await self.send_settings(ctx)
        elif command == "servers":
            servers = ", ".join([guild.name for guild in self.bot.guilds])
            await ctx.send(f"Servers authorized for: {servers}")
        elif command == "set":
            if not commandparameter or not commandvalue:
                await ctx.send(
                    f'For the "set" command I need a parameter and a value, like "settings set PUBLIC_VOTING false"')
                return

            if not self.settings.has_setting(commandparameter):
                await ctx.send(
                    f'Setting {commandparameter} does not exist in the settings')
                return

            self.settings.set_property(commandparameter, commandvalue)
            await self.send_settings(ctx)

    async def open_voting(self):
        self.votes.open_voting()
        self.bot.dispatch("yell", "Ik mag u melden dat stemmen vanaf heden is toegestaan")

    async def close_voting(self):
        self.votes.close_voting()
        self.bot.dispatch("yell", "Vanaf heden is het niet mogelijk om te stemmen")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def votes(self, ctx, command):
        accepted = ["clean", "standing", "show", "open", "close"]
        if command not in accepted:
            await ctx.send(f'Votes {command} was unknown. I only know the following commands: {", ".join(accepted)}')
            return

        if command == "clean":
            self.votes.clean()
            await ctx.send('Okay, all votes were removed')
        elif command == "standing":
            result = Votes.get_formatted_standing(self.votes.get_current_votes())
            self.bot.dispatch("yell", result)
        elif command == "show":
            result = Votes.get_formatted_votes(self.votes.get_current_votes(), self.votes.get_vote_set())
            await ctx.send(result)
        elif command == "open":
            await self.open_voting()
            await ctx.send("Voting is now enabled")
        elif command == "close":
            await self.close_voting()
            await ctx.send("Voting is now disabled")
        else:
            await ctx.send('Unknown command..')

    @commands.Cog.listener()
    async def on_timer_start(self):
        await self.open_voting()

    @commands.Cog.listener()
    async def on_timer_done(self):
        await self.close_voting()

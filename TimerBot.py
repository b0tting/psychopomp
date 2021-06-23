import datetime
from discord.ext import commands, timers
from PompSettings import PompSettings


class TimerBot(commands.Cog):
    def __init__(self, bot, votes, settings: PompSettings):
        self.bot = bot
        self.votes = votes
        self.settings = settings
        self.minutesleft = 0
        self.timer = None

    @staticmethod
    def get_next_reminder(minutes):
        if minutes > 10:
            return 5
        else:
            return 1

    def set_timer(self):
        wait_minutes = TimerBot.get_next_reminder(self.minutesleft)
        date = datetime.datetime.utcnow() + datetime.timedelta(minutes=wait_minutes)
        self.minutesleft = self.minutesleft - wait_minutes
        self.timer = timers.Timer(self.bot, "reminder", date, args=())
        self.timer.start()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def timer(self, ctx, command):
        accepted = ["new", "pause", "continue"]
        try:
            self.minutesleft = int(command)
            command = "new"
        except ValueError:
            pass
        if command not in accepted:
            await ctx.send(f'Votes {command} was unknown. I only know the following commands: {", ".join(accepted)}')
            return

        if command == "new":
            if self.timer:
                if not self.timer.done:
                    await ctx.send("There was an active timer, overwriting it with a new one")
                    self.timer.cancel()
            startminutes = self.minutesleft
            self.set_timer()
            self.bot.dispatch("timer_start")
            await ctx.send("Timer was started. Don't forget !votes open to enable voting")
            channel = self.settings.get_vote_channel()
            await channel.send(f":star: Het begint! Het doet mij deugd u te melden dat er nog {startminutes} minuten over zijn!")

        elif command == "pause":
            if not self.timer or self.timer.done:
                await ctx.send(f"There was no running timer.")
            else:
                await ctx.send(f"Timer was paused at {self.minutesleft} minutes")
                self.timer.cancel()

        elif command == "continue":
            if self.timer and not self.timer.done:
                await ctx.send(f"Timer is already running, either start a new one or pause it first")
            elif self.minutesleft > 0:
                await ctx.send(f"Restarting timer at {self.minutesleft} minutes left")
                self.set_timer()
            else:
                await ctx.send(f"There was no running timer. Cowardly refusing to continue.")

    @commands.Cog.listener()
    async def on_reminder(self):
        if self.minutesleft > 0:
            if self.minutesleft == 1:
                yell = f"Het einde is nabij! U heeft nog één minuut om u op uw stem te bezinnen!"
            else:
                yell = f"Het doet mij deugd u te melden dat er nog {self.minutesleft} minuten over zijn!"
            self.set_timer()
        else:
            self.bot.dispatch("timer_done")
            yell = f"**Hora est!** De tijd is op!"
        self.bot.dispatch("yell", yell)







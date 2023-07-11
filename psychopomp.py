import asyncio
import gettext

from discord.ext.commands import Bot, CommandNotFound

import discord

from lib.AdminBot import AdminBot
from lib.IntroBot import IntroBot
from lib.PlayerMessageBot import PlayerMessageBot
from lib.PompSettings import PompSettings
from lib.TimerBot import TimerBot
from lib.YellBot import YellBot
from lib.votes import Votes


# Setting up some globals
intents = discord.Intents.all()
intents.members = True
bot = Bot(intents=intents, command_prefix="!")

# These will be set in the startup function
standing_channelid = False
myguild = None

settings = PompSettings(".env", bot)
votes = Votes()

# This could probably be done in a prettier way
_ = settings.get_locale_function()


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    print("Connected to server " + settings.get_guild().name)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        _("Hi %s, welkom op de kleine-goden discord server!") % member.name
    )


# Catchall to prevent CommandNotFound errors on every message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


async def main():
    async with bot:
        await bot.add_cog(PlayerMessageBot(bot, votes, settings))
        await bot.add_cog(AdminBot(bot, votes, settings))
        await bot.add_cog(IntroBot(bot, settings))
        await bot.add_cog(TimerBot(bot, votes, settings))
        await bot.add_cog(YellBot(bot, votes, settings))

        await bot.start(settings.get_value("DISCORD_TOKEN"))


asyncio.run(main())

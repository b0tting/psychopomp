from discord.ext.commands import Bot, CommandNotFound
from AdminBot import AdminBot
from IntroBot import IntroBot
from PompSettings import PompSettings
from TimerBot import TimerBot
from PlayerMessageBot import PlayerMessageBot
from YellBot import YellBot
from votes import Votes
import discord


# Setting up some globals
intents = discord.Intents.default()
intents.members = True
bot = Bot(intents=intents, command_prefix="!")

# These will be set in the startup function
standing_channelid = False
myguild = None

settings = PompSettings(".env", bot)
votes = Votes()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print("Connected to server " + settings.get_guild().name)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welkom op de kleine-goden discord server!'
    )


# Catchall to prevent CommandNotFound errors on every message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.add_cog(PlayerMessageBot(bot, votes, settings))
bot.add_cog(AdminBot(bot, votes, settings))
bot.add_cog(IntroBot(bot, settings))
bot.add_cog(TimerBot(bot, votes, settings))
bot.add_cog(YellBot(bot, votes, settings))

bot.run(settings.get_value('DISCORD_TOKEN'))

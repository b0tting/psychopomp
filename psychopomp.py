# bot.py
import os

from votes import Votes, MessageValidator, MessageValidationException
import discord
from dotenv import load_dotenv

load_dotenv()

# Setting up some globals
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
votes = Votes()

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

    voter = get_member_for_user(message.author)

    ms = MessageValidator(message, voter)
    if ms.is_voting_message():
        try:
            votee = ms.get_votee_from_message()
            # Private messages are outside of the context of a server, so we get a "user" and not a "member"
            if type(votee) == discord.user.User:
                votee = get_member_for_user(votee)

            await message.reply(f"Ik noteer uw stem op {votee.display_name}")
            votes.vote_for(voter, votee)
            await publish_standings()

        except MessageValidationException as e:
            await message.reply(str(e))

client.run(os.getenv('DISCORD_TOKEN'))


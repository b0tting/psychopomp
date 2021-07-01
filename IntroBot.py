import asyncio
import os

import audioread as audioread
import discord
from discord.ext import commands
from asyncio import sleep

rpgmusicpath = r"./mp3/"

class IntroBot(commands.Cog):
    def __init__(self, client, settings):
        self.bot = client
        self.settings = settings
        self.channel_name = None
        self.voice_client = None


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def intro(self, ctx, command="list", commandparameter=""):
        songlist = os.listdir(self.settings.get_value("MP3_DIRECTORY"))
        if command == "list":
            result = "On the MP3 menu I have:\n```\n"
            i = 0
            for ar in songlist:
                i += 1
                result += f"{i}) {ar}\n"
            result += "```"
            await ctx.send(result)
        elif command == "play":
            # Maybe it's a number?
            mp3 = None
            try:
                number = int(commandparameter)
                mp3 = songlist[number - 1]
            except ValueError:
                pass
            except IndexError:
                pass

             # Probably a song name then
            if not mp3:
                mp3 = commandparameter
                if not mp3.endswith(".mp3"):
                    mp3 += ".mp3"

            if mp3 not in songlist:
                await ctx.send(f"Could not find an MP3 file named {mp3}")
            else:
                await ctx.send(f"Now playing {mp3} on {self.settings.get_voice_channel()}")
                self.bot.dispatch("intro", mp3)
        elif command == "pause":
            introbot = self.bot.get_cog('IntroBot')
            await ctx.send(f"Playing paused, use 'play' for another tune or 'resume' to continue playing")
            await introbot.pause()
        elif command == "resume":
            introbot = self.bot.get_cog('IntroBot')
            await ctx.send(f"Playing resumed")
            await introbot.resume()

    async def get_voice(self):
        if not self.channel_name:
            self.channel_name = self.settings.get_voice_channel()

        voice_chan = self.settings.get_voice_channel()
        if self.voice_client and voice_chan is not self.voice_client.channel:
            await self.voice_client.disconnect()
            self.voice_client = None

        if not self.voice_client:
            self.voice_client = await voice_chan.connect()

        if not self.voice_client.is_connected():
            await self.voice_client.connect()

        return self.voice_client

    async def pause(self):
        voice_client = await self.get_voice()
        if voice_client.is_playing():
            voice_client.pause()

    async def resume(self):
        voice_client = await self.get_voice()
        if voice_client.is_paused():
            voice_client.resume()

    @commands.Cog.listener()
    async def on_intro(self, mp3):
        # replace this with the path to your audio file
        voice = await self.get_voice()
        if voice.is_paused():
            voice.stop()
        path = os.path.join(rpgmusicpath, mp3)
        ffmpeg = self.settings.get_value("FFMPEG_LOCATION")
        voice.play(discord.FFmpegPCMAudio(path, executable=ffmpeg))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.8
        with audioread.audio_open(path) as f:
            # Start Playing
            sleep(f.duration)




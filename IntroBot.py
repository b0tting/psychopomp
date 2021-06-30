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
        voice.play(discord.FFmpegPCMAudio(path, executable="./ffmpeg/ffmpeg.exe"))
        with audioread.audio_open(path) as f:
            # Start Playing
            sleep(f.duration)




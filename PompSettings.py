from configparser import ConfigParser

import discord


class PompNotInitializedError(Exception):
    pass


class PompSettings:
    def __init__(self, settingfile, client:discord.Client):
        self.config = ConfigParser()
        self.client = client
        self.config.read(settingfile)
        self.initialized = False
        self.__vote_channel = None
        self.__guild = None

    def __get_property(self, setting, boolean=False):
        if self.config.has_option("PsychoPomp", setting):
            if boolean:
                return self.config.getboolean("PsychoPomp", setting)
            else:
                return self.config.get("PsychoPomp", setting)
        else:
            raise ValueError(f"Could not find setting {setting}")

    def get_all_settings(self):
        return self.config.items("PsychoPomp")

    def get_vote_channel(self):
        if not self.__vote_channel:
            for channel in self.client.get_all_channels():
                if channel.name == self.get_value("VOTING_CHANNEL"):
                    self.__vote_channel = channel
                    print(f"Publishing standings to channel " + channel.name)
                    break
            if not self.__vote_channel:
                raise Exception("Could not find channel for channel name " + self.get_value("VOTING_CHANNEL"))
        return self.__vote_channel

    def get_guild(self):
        return self.client.guilds[0]

    def get_flag(self, flag):
        return self.__get_property(flag, boolean=True)

    def get_value(self, value):
        return self.__get_property(value)

    def get_bot_member(self):
        return self.client.user
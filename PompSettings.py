from configparser import ConfigParser

import discord


class PompNotInitializedError(Exception):
    pass


class PompSettings:
    def __init__(self, settingfile, client: discord.Client):
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

    def get_vote_channel(self, ignore_cache=False):
        if not self.__vote_channel or ignore_cache:
            for channel in self.__guild.text_channels:
                if channel.name.lower() == self.get_value("VOTING_CHANNEL").lower():
                    self.__vote_channel = channel
                    break
            if not self.__vote_channel:
                raise Exception("Could not find channel for channel name " + self.get_value("VOTING_CHANNEL"))
        return self.__vote_channel

    def get_guild(self, ignore_cache=False):
        if not self.__guild or ignore_cache:
            current_selected = self.__get_property("active_server")
            for server in self.client.guilds:
                if server.name.lower() == current_selected.lower():
                    self.__guild = server
                    break
            if not self.__guild:
                raise ValueError(f"Could not find the 'ACTIVE_SERVER' {current_selected} in the list of authorized servers")
        return self.__guild

    def get_flag(self, flag):
        return self.__get_property(flag, boolean=True)

    def set_property(self, parameter, value):
        self.config.set("PsychoPomp", parameter, value)
        if parameter.lower() == "voting_channel":
            self.get_vote_channel(ignore_cache=True)
        elif parameter.lower() == "active_server":
            self.get_guild(ignore_cache=True)

    def get_value(self, value):
        return self.__get_property(value)

    def get_bot_member(self):
        return self.client.user

    def has_setting(self, setting):
        return self.config.has_option("PsychoPomp", setting)

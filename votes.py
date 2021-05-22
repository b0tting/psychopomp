import os
import re

import discord
from discord import member, message
import datetime


class MessageValidationException(Exception):
    pass


class MessageValidator:

    def __init__(self, message, sender):
        self.message_expr = re.compile(os.environ["VOTE_TRIGGER"])
        self.sender = sender
        self.message = message

    def is_voting_message(self):
        return self.message_expr.match(self.message.content.lower())

    def get_votee_from_message(self):
        if len(self.message.mentions) == 0:
            if "@" in self.message.content:
                raise MessageValidationException("Oh, hoogster aller machten, het spijt mij, ik herken de naam niet die u gebruikt na uw apestaart teken.")
            else:
                raise MessageValidationException("Oh, hoogster aller machten, ik herinner u graag dat u stemmen kunt uitbrengen "
                                    "door te verwijzen naar de naam van uw stem met voorgaand een @. U zou "
                                    "bijvoorbeeld @Psychopomp kunnen gebruiken, hoewel Pavi mij direct zou "
                                    "neerbliksemen al zou ik die stem aannemen van u.")
        elif len(self.message.mentions) > 1:
            raise MessageValidationException("Oh, hoogster aller machten, hoe gul u ook bent, ik herinner u graag dat u slecht op "
                                "één persoon kunt stemmen")
        elif self.message.mentions[0] == self.sender and os.environ["CAN_VOTE_SELF"] != "true":
            raise MessageValidationException("Het spijt mij. De machten hebben bepaald dat u niet op zichzelf kunt stemmen")

        if self.message.guild and os.environ["PUBLIC_VOTING"] != "true":
            raise MessageValidationException(
                "Ik kan uw stem niet aannemen, ik verzoek u vriendelijk om uw stemmen direct aan mij te sturen in een privé bericht")

        if not self.message.guild and os.environ["PRIVATE_VOTING"] != "true":
            raise MessageValidationException(
                "Ik kan uw stem niet privé aannemen, ik verzoek u vriendelijk om uw stem openbaar te plaatsen")

        votee = self.message.mentions[0]
        return votee


class Vote:
    def __init__(self, voter: member):
        self.history = []
        self.time = datetime.datetime.now()
        self.voter = voter

    def vote_for(self, votee: member):
        self.history.append((votee, datetime.datetime.now()))

    def get_last_votee(self):
        return self.history[-1][0]


class Votes:
    def __init__(self):
        self.votes = {}

    def vote_for(self, voter: member, votee: member):
        if voter in self.votes:
            vote = self.votes[voter]
        else:
            vote = Vote(voter)
            self.votes[voter] = vote
        vote.vote_for(votee)

    # Get the current vote standing in a dict of votee:number of votes
    def get_current_votes(self):
        total = {}
        for voter, vote in self.votes.items():
            votee = vote.get_last_votee()
            if votee in total:
                total[votee] = total[votee] + 1
            else:
                total[votee] = 1
        return total

    # Format a votes dict of votee:number of votes into a readable list
    def format_votes(self, votes):
        # Neat trick!
        sorted_votes = dict(sorted(votes.items(), key=lambda item: item[1]))

        returnstring = "**Ik presenteer u uw keuzes!**\n"
        for votee, votes in sorted_votes.items():
            if votes > 1:
                returnstring += f"{votee.display_name} heeft {votes} stemmen\n"
            elif votes == 1:
                returnstring += f"{votee.display_name} heeft {votes} stem\n"
        return returnstring

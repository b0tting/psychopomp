from discord import member
import datetime


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

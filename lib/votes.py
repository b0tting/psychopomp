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
        self.__enabled = False

    def close_voting(self):
        self.__enabled = False

    def open_voting(self):
        self.__enabled = True

    def is_open(self):
        return self.__enabled

    def clean(self):
        self.votes = {}

    def vote_for(self, voter: member, votee: member):
        if voter in self.votes:
            vote = self.votes[voter]
        else:
            vote = Vote(voter)
            self.votes[voter] = vote
        vote.vote_for(votee)

    def get_last_voted_for(self, voter):
        if voter in self.votes:
            return self.votes[voter].get_last_votee()
        else:
            return False

    # Get the current vote standing in a dict of votee:number of votes
    def get_current_votes(self):
        total = {}
        for voter, vote in self.votes.items():
            votee = vote.get_last_votee()
            if votee:
                if votee in total:
                    total[votee] = total[votee] + 1
                else:
                    total[votee] = 1
        return total

    def get_vote_set(self):
        return self.votes.copy()

    def remove_vote(self, voter):
        self.vote_for(voter, None)

    # Format a votes dict of votee:number of votes into a readable list
    @staticmethod
    def get_formatted_standing(votes):
        # Neat trick!
        sorted_votes = dict(sorted(votes.items(), key=lambda item: item[1]))
        if sorted_votes:
            returnstring = _("**Ik presenteer u uw keuzes!**\n")
            returnstring += "\n>>>"
            for votee, votes in sorted_votes.items():
                if votes > 1:
                    returnstring += _("**%s** heeft **%d** stemmen\n") % (
                        votee.display_name,
                        votes,
                    )
                elif votes == 1:
                    returnstring += _("**%s** heeft 1 stem\n") % votee.display_name
        else:
            returnstring = _("**Niemand heeft nog een stem uitgebracht**")
        return returnstring

    # Format a votes dict of votee:number of votes into a readable list
    @staticmethod
    def get_formatted_votes(votes_count, votes_set):
        sorted_votes = dict(sorted(votes_count.items(), key=lambda item: item[1]))
        if sorted_votes:
            returnstring = ">>> "
            for votee, votes in sorted_votes.items():
                if votes > 1:
                    returnstring += _("**%s** heeft **%d** stemmen\n") % (
                        votee.display_name,
                        votes,
                    )
                elif votes == 1:
                    returnstring += _("**%s** heeft 1 stem\n") % votee.display_name
            returnstring += f"\n"
            for voter, vote in votes_set.items():
                votee = vote.get_last_votee()
                if votee:
                    returnstring += _("**%s** heeft gestemd op *%s*\n") % (
                        voter.display_name,
                        votee.display_name,
                    )
                else:
                    returnstring += (
                        _("**%s** heeft niet gestemd\n") % voter.display_name
                    )
        else:
            returnstring = _("Niemand heeft nog gestemd")
        return returnstring

from outcome import BinBuilder
from random import randint, choice

class Table(object):
    """Creates structure to hold bets"""
    def __init__(self, limit, minimum):
        self.limit = limit
        self.minimum = minimum
        self.bets = []

    def place_bet(self, bet):
        self.bets.append(bet)

    def __iter__(self):
        return self.bets[:]

    def __str__(self):
        return " ;".join(str(x) for x in self.bets)

    def __repr__(self):
        return "Table(" + "; ".join(str(x) for x in self.bets) + ")"


            
class Wheel(object):
    """
    Selects Random Bin and returns all 
    winning outcomes through Class :Bin
    """

    def __init__(self):
        binbuilder = BinBuilder()

        self.bins = binbuilder.get_bins()
        self.all_outcomes = binbuilder.get_outcomes()
        self.rng = randint(0, 38)



    def addOutcome(self, number, outcome):
        # adds an outcome to the specified bin
        self.bins[number].add(outcome)

    def next(self):
        return choice(self.bins)

    def get(self, number):
        return self.bins[number]

    def get_outcome(self, name):
        return set((oc for oc in self.all_outcomes if oc.name.lower() == name.lower())).pop()
        
        

class Bet(object):
    """Class to store bets
    and return various information
    pertaining to the bet"""
    def __init__(self, amount_bet, outcome):
        self.amount_bet = amount_bet
        self.outcome = Wheel().get_outcome(outcome)

    def win_amount(self):
        return ((self.outcome.odds * self.amount_bet) + self.amount_bet)

    def lose_amount(self):
        return self.amount_bet

    def __str__(self):
        return "%d on %s"%(self.amount_bet, self.outcome.name)

    def __repr__(self):
        return "Bet(%d, %s)"%(self.amount_bet, self.outcome.name)

class InvalidBet(Exception):
    
    def __init__(self):
        Exception.__init__(self, "Invalid Bet")



from random import randint, choice

class Outcome(object):
    """
    Medium to Outcomes
    """

    def __init__(self, name, odds):
        # initialize name and odds
        self.name = name
        self.odds = odds

    def win_ammount(self, ammount):
        """calculate winnings"""
        return ammount * self.odds

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "%s (%d : 1)" % (self.name, self.odds)

    def __repr__(self):
        return "{class_:s}({name!r}, {odds!r})".format(class_=type(self).__name__, **vars(self))


class Bin(set):
    """
    Contains all possible outcome connections in a frozenset
    Collected by Class :Outcomes
    """
    def __init__(self):
        pass

class BinBuilder(object):
    """create bins that 
    each represent a number 
    in roulette"""
    def __init__(self):
        self.bins = tuple(Bin() for i in range(38))

    def red_numbers(self):
        """yield red numbers as argument list"""
        for i in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            yield i

    def black_numbers(self):
        """yield black numbers as an argument for clarity"""
        for i in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 28, 29, 31, 33, 35]:
            yield i

    def addOutcome(self, outcome, numbers):
        # adds an outcome to the specified bin- later add a distribution algorithm
        for number in numbers:
            self.bins[number].add(outcome)

    def americanized(self):
        self.addOutcome(Outcome("00", 35), [37])
        self.addOutcome(Outcome("00-3 line", 5), [0, 1, 2, 3, 37])

    def straight_bet(self):
        """sets up all straight bet bins"""
        for i in range(0, len(self.bins)):
            self.addOutcome(Outcome(str(i), 35), [i])

    def split_bet(self):
        """sets up all split bet bins"""
        for num in range(1, 37):

            # left-right split
            if num % 3 != 0:
                self.addOutcome(Outcome(("%d-%d split" % (num, (num + 1))), 17), [num, num + 1])

            # up-down split
            if num < 34:
                self.addOutcome(Outcome(("%d-%d split" % (num, (num + 3))), 17), [num, num + 1])

    def street_bet(self):
        """sets up all street bet bins"""
        for i in range(0, 12):
            num = 3 * i
            self.addOutcome(Outcome("%d-%d street" % (num + 1, num + 3), 11), [num + 1, num + 2, num + 3])

    def corner_bet(self):
        """sets up all corner bet bins"""
        for adder in range(1, 3):
            # adjusts num to update the first and then second column
            for i in range(0, 11):
                num = 3 * i + adder
                self.addOutcome(Outcome("%d-%d-%d-%d corner" % (num, num + 1, num + 3, num + 4), 8),
                                [num, num + 1, num + 3, num + 4])

    def line_bet(self):
        """set up line bet bins"""
        for i in range(0, 11):
            num = 3 * i + 1
            self.addOutcome(Outcome("%d-%d line" % (num, num + 5), 5),
                            range(num, num + 6))

    def dozen_bet(self):
        """set up all dozen bet bins"""
        for i in range(0, 3):
            num = 12 * i + 1
            self.addOutcome(Outcome("dozen #%d" % (i + 1), 2), range(num, num + 12))

    def column_bet(self):
        """set up all column bets"""
        for i in range(0, 3):
            keyword_converter = {0: "Left", 1: "Middle", 2: "Right"}
            self.addOutcome(Outcome("%s Column" % (keyword_converter[i]), 2),
                            range(i + 1, i + 35, 3))

    def even_bet(self):
        """set up all even bets"""
        self.addOutcome(Outcome("Even", 1), range(2, 36, 2))

    def odd_bet(self):
        """set up all odd bets"""
        self.addOutcome(Outcome("Odd", 1), range(1, 36, 2))

    def red_bet(self):
        """set up all red bet bins"""
        self.addOutcome(Outcome("red", 1), self.red_numbers())

    def black_bet(self):
        """set up all black bet bins"""
        self.addOutcome(Outcome("black", 1), self.black_numbers())

    def create_bins(self):
        """call all the bin builder functions"""
        self.straight_bet()
        self.split_bet()
        self.street_bet()
        self.corner_bet()
        self.line_bet()
        self.dozen_bet()
        self.column_bet()
        self.even_bet()
        self.odd_bet()
        self.red_bet()
        self.black_bet()
        self.americanized()

    def get_bins(self):
        """returns Bins to Wheel class"""
        self.create_bins()
        return self.bins

    def get_outcomes(self):
        outcomes = set()
        for i in self.bins:
            outcomes = outcomes.union(i)
        return outcomes

class EuropeanBinBuilder(BinBuilder):
    """bin builder with euro rules"""
    def __init__(self):
        BinBuilder.__init__(self)
        self.bins = tuple(Bin() for i in range(37))
    def create_bins(self):
        """call all the bin builder functions"""
        self.straight_bet()
        self.split_bet()
        self.street_bet()
        self.corner_bet()
        self.line_bet()
        self.dozen_bet()
        self.column_bet()
        self.even_bet()
        self.odd_bet()
        self.red_bet()
        self.black_bet()

class AmericanBinBuilder(BinBuilder):
    """binbuilder with american rules"""
    def __init__(self):
        BinBuilder.__init__(self)
        self.bins = tuple(Bin() for i in range(38))
    def create_bins(self):
        """call all the bin builder functions"""
        self.straight_bet()
        self.split_bet()
        self.street_bet()
        self.corner_bet()
        self.line_bet()
        self.dozen_bet()
        self.column_bet()
        self.even_bet()
        self.odd_bet()
        self.red_bet()
        self.black_bet()
        self.americanized()
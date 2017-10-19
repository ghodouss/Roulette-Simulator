import math
import statistics
from random import randint, choice
from table import Table, Wheel, Bet




class Game(object):
    """Object to run a
    round of roullette"""
    def __init__(self, wheel, table):
        self.wheel = wheel
        self.table = table

    def cycle(self, player):
        #give player the table
        player.set_table(self.table)

        #check if player is playing
        if not player.playing():
             return
        
        player.place_bets()
        winning_bin = self.wheel.next()

        #compare and update player stakes
        for bet in self.table.__iter__():
            
            #check if bet is valid
            if bet.amount_bet < self.table.minimum and bet.amount_bet > self.table.limit:
                raise InvalidBet()
            
            #update winnings (hopefully ;)
            if bet.outcome in winning_bin:
                player.win(bet)
            else:
                player.lose(bet)
        self.table.bets = []

class Player(object):
    """Object to manage
    player behavior and interact
    with the table by placing bets"""
    def __init__(self, stake=1000, initial_bet=10, roundstogo=250, table=None):
        self.table = table
        self.stake = stake
        self.roundstogo = roundstogo
        self.initial_bet = initial_bet

    def get_roundstogo(self):
        return self.roundstogo

    def get_stake(self):
        return self.stake

    def set_roundstogo(self, roundstogo):
        self.roundstogo = roundstogo

    def set_stake(self, stake):
        self.stake = stake
    
    def set_table(self, table):
        self.table=table

    def set_initbet(self, bet):
        self.initial_bet = bet  

    def playing(self):
        return (self.roundstogo>0 and self.stake>0)

    def check_bet(self, amount):
        """ amends the amount bet to fit within player's budget and table limit"""
        #limit bet to table limit
        if amount>self.table.limit:
            return self.table.limit

        #limit bet to stake
        if self.stake<amount and self.stake>0:
            return self.stake
        
        #if not enough money, stop bets
        if self.stake<self.table.minimum:
            return 0

        #default bet
        return amount

    def budget_update(self):
        print("Budget: " + str(self.stake))

    def place_bets(self):
        """basic placing bet strategy"""
        amount = self.check_bet(10)
        self.table.place_bet(Bet(amount, "black"))

        #remove bet from stake
        self.stake -= amount

    def win(self, bet):
        """return bet + winnings""" 
        self.stake += bet.win_amount()

        #update rounds to go
        self.roundstogo-=1
        
    def lose(self, bet):
        """Update roundstogo
        No need to subtract bc money
        subtracted at time of bet"""
        self.roundstogo-=1

    def push(self, bet):
        """lose, but return half of lost money"""
        self.stake +=bet.lose_amount/2
        self.roundstogo-=1

class Martingale(Player):
    """Player whose strategy
    is to double his bet every time
    he loses"""
    
    def __init__(self, stake=1000, initial_bet=10, roundstogo=250, table=None):
        Player.__init__(self, stake, initial_bet, roundstogo, table)
        
        #add loss counter to update the bet
        self.loss_count = 0

    @property
    def bet_multiple(self):
        return 2**self.loss_count

    def place_bets(self):
        
        #send the bet to check_bet
        amount = self.check_bet(self.initial_bet*self.bet_multiple)
        
        #place the bet
        self.table.place_bet(Bet(amount, "black"))
        
        #subtract bet from stake
        self.stake -= amount

    def win(self, bet):
        Player.win(self, bet)
        
        #reset loss count
        self.loss_count = 0


    def lose(self, bet):
        Player.lose(self, bet)
        #update loss count
        self.loss_count += 1

    def push(self, bet):
        Player.lose(self, bet)
        
        #update loss count 
        self.loss_count += 1
        
    
    def set_initbet(self, bet):
        Player.set_initbet(self, bet)
        
        #reset loss count
        self.loss_count = 0
        

    def __str__(self):
        return "Martingale"

class Simulator(object):
    """manages all the objects
    in the game and gathers data"""
    def __init__(self, game, player,  initstake=1000, initbet=10, initduration=250,samples=100):
        self.game = game
        self.stat = Statistics()
        self.initduration = initduration
        self.initstake = initstake
        self.set_initbet = initbet
        self.player = player
        self.samples = samples
        self.durations = []
        self.maxima = []
        self.max_points = []
        self.result = []
        
    def session(self):
        "run the game and return stakes flow"
        results = []
        while self.player.playing():
            self.game.cycle(self.player)
            results.append(self.player.get_stake())
        return results

    def gather(self): 
        for i in range(self.samples):

            #reset game
            self.player.set_stake(self.initstake)
            self.player.set_roundstogo(self.initduration)
            self.player.set_initbet(self.set_initbet)

            #run game
            result = self.session()

            #gather data
            self.durations.append(len(result))
            self.maxima.append(max(result))
            self.max_points.append(result.index(max(result)))
            self.result.append(result[-1])

    def stdev(self):
        return statistics.stdev(self.result)
    def mean(self):
        return statistics.mean(self.result)
    def bankrupt(self):
        return self.stat.bankrupt(self.result)
    def median(self):
        return statistics.median(self.result)

class Statistics(object):
    """Class to gather interesting
    statistics"""
    def __init__(self):
        pass

    def bankrupt(self, values):
        "Compute percent of players who go bankrupt"
        tot = 0
        for i in values:
            if i == 0:
                tot += 1
        return 100*tot/len(values)
        

def simulate(game, player, stake=1000, initbet=10, initduration=30):
        #initialize game and simulator
        g = Game(Wheel(), Table(1000, 1))
        s = Simulator(game, player, initstake=stake, initbet=initbet, initduration=initduration)
        
        #run the simulator
        s.gather()

        #print results
        print(str(player))
        print("Mean: " + str(s.mean()))
        print("Median: " + str(s.median()))
        print("Standard Deviation: " + str(s.stdev()))
        print("Percent Bankrupt: " + str(s.bankrupt())+"%")


simulate(Game(Wheel(), Table(1000, 10)), Martingale())

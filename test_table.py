from table import Table, Wheel, Bet
import unittest
t = Table(1000, 10)
w=Wheel()

class TestTableMethods(unittest.TestCase):
    def test_init(self):
        self.assertEqual(t.limit, 1000)
        self.assertEqual(t.minimum, 10)
    def test_place_bet(self):
        t.place_bet(10)
        self.assertEqual(len(t.bets), 1)
    def test_iter(self):
        self.assertEqual(t.__iter__(), t.bets)

class TestWheelMethods(unittest.TestCase):
    def test_init(self):
        

if __name__ == '__main__':
    unittest.main()
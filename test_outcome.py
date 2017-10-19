import unittest
from outcome import Outcome, Bin, BinBuilder

o = Outcome("name", 10)
bb = BinBuilder()

class TestOutcomeMethods(unittest.TestCase):
    def test_init(self):
        self.assertEqual("name", o.name)
        self.assertEqual(10, o.odds)
    def test_win_ammount(self):
        self.assertEqual(100, o.win_ammount(10))
    def test_eq(self):
        self.assertEqual(o, Outcome("name", 1000))

class TestBinBuilder(unittest.TestCase):
    def test_init(self):
        self.assertEqual(len(bb.bins), 38)
    def test_straight_bet(self):
        bb.straight_bet()
        for count, i in enumerate(bb.bins):
            self.assertTrue(Outcome(str(count), 35) in i)
    def test_split_bet(self):
        bb.split_bet()
        
        for count, i in enumerate(bb.bins):
            udstart = count%3 +1
            lrstart = udstart
            if udstart%3 == 0:
                lrstart -= 1
            self.assertTrue(Outcome(("%d-%d split" % (udstart, (udstart + 3))), 17), i)
            self.assertTrue(Outcome(("%d-%d split" % (lrstart, (lrstart + 1))), 17), i)
    def test_street_bet(self):
        for count, i in enumerate(bb.bins):
            start = (count//3)*3
            self.assertTrue(Outcome("%d-%d street" % (start, start + 2), 11), i) 
    def test_line_bet(self):
        for count, i in enumerate(bb.bins):
            start = (count//6)*6
            self.assertTrue(Outcome("%d-%d line" % (start, start + 5), 5), i)
    def test_dozen_bet(self):
        for count, i in enumerate(bb.bins):
            start = (count/12)+1
            self.assertTrue(Outcome("dozen #%d" % (start + 1), 2), i)
    def test_column_bet(self):
        keyword_converter = {0: "Right", 1: "Left", 2: "Middle"}
        for count, i in enumerate(bb.bins):
            name = keyword_converter[count%3]
            self.assertTrue(Outcome("%s Column" % (name), 2), i)
    def test_even_odd_bet(self):
        keyword_converter = {0: "Even", 1: "Odd"}
        for count, i in enumerate(bb.bins):
            name = keyword_converter[count%2]
            self.assertTrue(Outcome(name, 1), i)
    

if __name__ == '__main__':
    unittest.main()
            


import unittest
from covid19plots import util

def fun(x):
    return x + 2

class MyTest(unittest.TestCase):
    def testRunningTotal(self):
        self.assertEqual(util.runningTotal([], 7), [])
        self.assertEqual(util.runningTotal([1], 7), [])
        self.assertEqual(util.runningTotal([1,1,1,1,1,1,], 7), [])
        self.assertEqual(util.runningTotal([1,1,1,1,1,1,1], 7), [7])
        self.assertEqual(util.runningTotal([0,0,0,0,0,0,1], 7), [1])
        self.assertEqual(util.runningTotal([0,0,0,0,0,0,1,1], 7), [1,2])

    def testNewCases(self):
        self.assertEqual(util.newCases([]), [])
        self.assertEqual(util.newCases([0,1]), [0,1])
        self.assertEqual(util.newCases([1,3]), [1,2])
        self.assertEqual(util.newCases([2,2,5,5]), [2,0,3,0])

    def testGetFromTo(self):
        # getFromTo(length, timePeriod, daysBefore, frameNr)
        # returns the index of first data, index+1 of last
        length = 10 # all the data
        timePeriod = 7
        daysBefore = 0 # start from the beginning
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 0), (0,7))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 1), (0,8))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 2), (0,9))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 3), (0,10))

        daysBefore = 1 # start from the end 1 data
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 0), (3,10))

        daysBefore = 2 # start from the 2 last dates
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 0), (2,9))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 1), (2,10))

        daysBefore = 3 # start from the 3 last dates
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 0), (1,8))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 1), (1,9))
        self.assertEqual(util.getFromTo(length, timePeriod, daysBefore, 2), (1,10))


if __name__ == '__main__':
    unittest.main()        
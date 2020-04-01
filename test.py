import unittest
import util

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


if __name__ == '__main__':
    unittest.main()        
import unittest
import pentominos

class TestSaSyb(unittest.TestCase):

    def test_SaSyb(self):
        pentomino = pentominos.F()
        print(pentomino.representation())
        
        testSet = set([pentominos.I(), pentominos.I()])
        print(len(testSet) + testSet.representation())

    def test_flip
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestSaSyb)

if __name__ == '__main__':
    unittest.main()

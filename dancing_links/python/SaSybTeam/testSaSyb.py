import unittest
import pentominos

class TestSaSyb(unittest.TestCase):

    def test_SaSyb(self):
        pentomino = pentominos.F()
        print(pentomino.representation())
        testSet = pentominos.TileSet([pentominos.I(),pentominos.X()])
        print(testSet.representation())

suite = unittest.TestLoader().loadTestsFromTestCase(TestSaSyb)

if __name__ == '__main__':
    unittest.main()

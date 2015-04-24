import unittest
import pentominos

class TestSaSyb(unittest.TestCase):

    def test_SaSyb(self):
        pentomino = pentominos.F()
        print(pentomino.representation())
        pentomino.translate_by([2,1])
        print(pentomino.representation())
        #testSet = pentominos.TileSet(pentomino)
        #print(testSet.representation())
        print(pentomino.__eq__(pentominos.I()))

suite = unittest.TestLoader().loadTestsFromTestCase(TestSaSyb)

if __name__ == '__main__':
    unittest.main()

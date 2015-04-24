import unittest
import pentominos

class TestSaSyb(unittest.TestCase):

    def test_SaSyb(self):
        pentomino = pentominos.F()
        print(pentomino.representation())
<<<<<<< HEAD
        
        testSet = set([pentominos.I(), pentominos.I()])
        print(len(testSet) + testSet.representation())

    def test_flip
        pass
=======
        pentomino.translate_by([2,1])
        print(pentomino.representation())
        #testSet = pentominos.TileSet(pentomino)
        #print(testSet.representation())
        print(pentomino.__eq__(pentominos.I()))
>>>>>>> 826b5f0da5c8e8d3f85f374de77d5a0462bf709a

suite = unittest.TestLoader().loadTestsFromTestCase(TestSaSyb)

if __name__ == '__main__':
    unittest.main()

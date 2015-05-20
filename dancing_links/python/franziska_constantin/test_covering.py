import unittest
import pentominos
import covering
import examples
import copy

class TestCoveringMethods(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_Board_init(self):
        B = covering.Board([3,2,2], {'[0, 1, 1]': 0, '[2, 1, 0]':5, '[1, 1, 1]': 2})
        #self.assertEqual([3,5,str([[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,3],[1,4],[2,0],[2,1],[2,3],[2,4]])], [T.rows, T.cols, T.representation()])
       
    def test_Board_valid_tile_placement(self):
	B = covering.Board([8,8],{'[3, 3]': 0,'[3, 4]': 0,'[4, 3]': 0,'[4, 4]': 0})
	self.assertEqual(False, B.valid_tile_placement([[3,2],[3,3],[3,4],[3,5],[3,6]]))
       
    #def test_covering_init(self):
	#B = covering.Board(8,8,[[3,3],[3,4],[4,3],[4,4]])
	#C = covering.Covering(B,covering.TileSet(pentominos.all_pentominos()),[])
	
    def test_covering_n_solutions(self):
	B = covering.Board([8,8],{'[3, 3]': 0,'[3, 4]': 0,'[4, 3]': 0,'[4, 4]': 0})
	C = covering.Covering(B,pentominos.TileSet(pentominos.all_pentominos()),{'X': [[[0,2],[1,2],[1,1],[1,3],[2,2]]]})
	self.assertEqual(19, C.n_solutions())
	C = covering.Covering(B,pentominos.TileSet(pentominos.all_pentominos()),{'X': [[[0,3],[1,3],[1,2],[1,4],[2,3]]]})
	self.assertEqual(20, C.n_solutions())
        C = covering.Covering(B,pentominos.TileSet(pentominos.all_pentominos()),{'X': [[[1,2],[2,2],[2,1],[2,3],[3,2]]]})
	self.assertEqual(26, C.n_solutions())
	

    
if __name__ == '__main__':
    unittest.main()

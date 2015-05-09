'''
Created on 08.05.2015

@author: lovis
'''
import unittest
from incidence_matrix import IncidenceMatrix
import incidence_matrix
import sudoku


class Test(unittest.TestCase):


    def testName(self):
        example1= [[0,2,8],[0,4,6],[0,7,4],[1,1,5],[1,3,3],[1,4,2],[2,0,3],[2,2,7],[2,5,8],[2,7,9],[3,0,9],[3,1,3],[3,6,4],[3,7,6],[4,2,6],[4,5,4],[4,6,5],[4,7,7],[5,1,4],[5,7,8],
                   [5,8,2],[6,0,5],[6,1,8],[6,3,1],[6,4,4],[6,6,2],[6,7,3],[6,8,7],[7,2,3],[7,5,8],[7,6,8],[7,7,5],[8,0,2],[8,4,7],[8,6,8]]
        empty = []
        names=sudoku.sudokuListHeaders(empty)
        print(len(names))
        I=incidence_matrix.IncidenceMatrix(names)
        I.insertSudokuRows(empty)
        print(I.rows)
        I.calculatePentominoSolution(0, [])
        print(len(I.solutions))
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
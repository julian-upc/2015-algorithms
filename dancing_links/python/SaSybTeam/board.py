# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:38:22 2015
This class gives a board for the pentominos to cover
@author: Thinkerbell
"""
import pentomino
import incidence_matrix

class Board(object):
    def __init__(self, rows, columns, covered):
        """ rows are the given rows of the board
            columns are the given columns of the board
            covered is a list of tupel [i,j] with all covered coordinates 
        """
        self.rows = rows
        self.columns = columns
        self.covered = covered
    
    def representation(self):
        """ returns a string representation of this board.
            a board is represented with its uncovered coordinates, so
            the string is a list of all uncovered coordinates
        """
        rep = []
        for i in range(self.rows):
            for j in range(self.columns):
                if [i,j] not in self.covered([i,j]):
                    rep.append([i,j])
        return str(rep)
            
    def containsCoo(coo):
        if coo not inHole(coo):
            if 0 <= coo[0] <= self.rows:
                if 0 <= coo[1] <= self.columns:
                    return true
        else:
            retrun false
            
    def containsPentomino(pentomino):
        count = 0
        for coo in pento.coos:
            if Board.containsCoo(coo):        
                count += 1
        if count == 5:
            return true
        else:
            return false
    
def inHole(coo):
    """ The methode 'isInHole(coo)' checks, if a given coordinate coo equals 
        one of the coordinates [[3,3],[3,4],[4,3],[4,4]] """
    if coo not in [[3,3],[3,4],[4,3],[4,4]]:
        return true
    else:
        return false   
        
class scott(object):
    def __init__(self, IncidenceMatrix, Board):
        self.InciMatrix = IncidenceMatrix
        self.Board = Board
        
    def matrixRows(self):
        self.InciMatrix = scott_matrixTitels()
        # append all rows for all pentominos on all possible valid positions
        allPentoTypes = pentomino.all_fixed_pentominos()
        for pento in allPentoTypes:
            for i in range(self.Board.rows):
                for j in range(self.Board.columns):
                    pento.normalize()
                    pento.translate_by([i,j])
                    if self.Board.containsPentomino(pento):
                        self.InciMatrix.appendRow(pento.name, pento.coos)
        
    def matrixTitels():
        """ The methode 'scott_example()' creates all ColumnObjects for:
                - all the possible pentominos
                - all positions on the actual board
            and returns the corresponding incidence Matrix """
        names = ["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"]
        for i in range(self.Board.rows):
            for j in range(self.Board.columns):
                if not inHole([i,j]):
                    names.append(str(i)+str(j))
        return incidence_matrix.IncidenceMatrix(names)

    
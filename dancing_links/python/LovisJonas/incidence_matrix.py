import pentominos
import sudoku
import copy

from copy import deepcopy
from sudoku import cal_square
def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        pass
    return False


class IncidenceCell(object):
    def __init__(self, left, right, up, down, listHeader, name):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.listHeader = listHeader
        self.name = name

    def representation(self):
        rep = ["c", self.name]
        for c in [self.left, self.right, self.up, self.down]:
            rep.append(c.name)
        return rep
    
class ColumnObject(IncidenceCell):
    def __init__(self, left, right, up, down, name):
        IncidenceCell.__init__(self, left, right, up, down, self, name)
        self.size = 0

    def representation(self):
        hrep = ["h(" + str(self.size) + ")", self.name]
        for c in [self.left, self.right, self.up, self.down]:
            hrep.append(c.name)
        rep = [[hrep]]

        currentCell = self.down
        while currentCell is not self:
            rep[0].append(currentCell.representation())
            currentCell = currentCell.down
        
        return rep

class IncidenceMatrix(object):
    def __init__(self, names):
        self.h = ColumnObject(None, None, None, None, "root")
        self.h.left = self.h.right = self.h.up = self.h.down = self.h

        currentColumnObject = self.h
        self.columnObjectOfName = dict()
        self.columnObjectOfName["root"] = self.h

        self.indexOfPiecePlacement = dict()
        for n in names:
            self.indexOfPiecePlacement[n] = 0
            self.insertColumnObject(currentColumnObject, self.h, n)
            currentColumnObject = currentColumnObject.right
            self.columnObjectOfName[n] = currentColumnObject

        self.rows = 0

    def representation(self):
        currentColumnObject = self.h

        rep = currentColumnObject.representation()
        currentColumnObject = currentColumnObject.right

        while currentColumnObject.name is not "root":
            rep += currentColumnObject.representation()
            currentColumnObject = currentColumnObject.right
            
        return rep

    def rowRepresentation(self):
        rowRep = []
        currentColumnObject = self.h.right
        while currentColumnObject.name is not "root" and not is_number(currentColumnObject.name):
            head_elt = currentColumnObject.down
            while head_elt is not currentColumnObject:
                row = [ head_elt.name ]
                current_elt = head_elt.right
                while current_elt is not head_elt:
                    row.append(current_elt.listHeader.name)
                    current_elt = current_elt.right
                rowRep.append(row)
                head_elt = head_elt.down
            currentColumnObject = currentColumnObject.right
        return rowRep

    def insertColumnObject(self, left, right, name):
        newColumn=ColumnObject(left,right,None,None,name)
        newColumn.up=newColumn.down=newColumn
        newColumn.left.right=newColumn
        newColumn.right.left=newColumn
        

    def appendRow(self, tileName, placement):
        self.indexOfPiecePlacement[tileName]+=1
        columnTile=self.columnObjectOfName[tileName]
        columnTile.size+=1
        tileNameCell=IncidenceCell(columnTile,columnTile,columnTile.up,columnTile,columnTile,str(tileName)+str([self.indexOfPiecePlacement[tileName]-1]))
        tileNameCell.up.down=tileNameCell
        columnTile.up=tileNameCell
        listOfPlacementCells = []
        self.rows+=1
        for position in placement:
            columnPlacement=self.columnObjectOfName[position]
            listOfPlacementCells.append(IncidenceCell(columnPlacement, columnPlacement, columnPlacement.up, columnPlacement, columnPlacement, str(tileName)+str(position)))
        for k in listOfPlacementCells:
            columnPlacement=self.columnObjectOfName[k.listHeader.name]   
            columnPlacement.up=k
            k.up.down=k
            columnPlacement.size+=1
        n=len(listOfPlacementCells)
        rep = [n]
        for k in listOfPlacementCells:
            rep.append(k.representation())
        for i in range(n):
            if i==0:
                listOfPlacementCells[i].left=tileNameCell
            elif i in range(1,n):
                listOfPlacementCells[i].left=listOfPlacementCells[i-1]
            if i==n-1:
                listOfPlacementCells[i].right=tileNameCell
            elif i in range(n-1):
                listOfPlacementCells[i].right=listOfPlacementCells[i+1]
        rep = [n]
        for k in listOfPlacementCells:
            rep.append(k.representation())
        tileNameCell.left=listOfPlacementCells[n-1]
        tileNameCell.right=listOfPlacementCells[0]

            
    def coverColumn(self, columnTile):
        columnTile.left.right=columnTile.right
        columnTile.right.left=columnTile.left
        currentCell=columnTile.down
        currentCellHorizontal=columnTile.down
        while currentCell != columnTile:
            currentCellHorizontal=currentCell.right
            while currentCellHorizontal != currentCell:
                currentCellHorizontal.up.down=currentCellHorizontal.down
                currentCellHorizontal.down.up=currentCellHorizontal.up
                currentCellHorizontal.listHeader.size-=1
                currentCellHorizontal=currentCellHorizontal.right
            currentCell=currentCell.down
        
    def uncoverColumn(self, c):
        currentCell=c.up
        currentCellHorizontal=c.up
        while currentCell != c:
            currentCellHorizontal=currentCell.left
            while currentCellHorizontal != currentCell:
                currentCellHorizontal.up.down=currentCellHorizontal
                currentCellHorizontal.down.up=currentCellHorizontal
                currentCellHorizontal.listHeader.size+=1
                currentCellHorizontal=currentCellHorizontal.left
            currentCell=currentCell.up 
        c.left.right=c
        c.right.left=c
            
    def insertAllPlacements(self, pentomino):
        pentomino.normalize()
        versionList=pentominos.fixed_pentominos_of(pentomino)
        coordinatesAsStrings=[]
        for p in versionList:
            for i in range(8):
                for k in range(8):
                    if p.legal():
                        for l in range(5):
                            coordinatesAsStrings.append(str(p.coos[l][0])+str(p.coos[l][1]))
                        self.appendRow(p.name, coordinatesAsStrings)
                    p.translate_one(1)
                    coordinatesAsStrings=[]
                p.translate_by([0,-8])
                p.translate_one(0)
            
        
    def initializeTheIncidenceMatrix(self):
        allPentos=pentominos.all_pentominos()
        for p in allPentos:
            self.insertAllPlacements(p)
    
    def initializeSudokuMatrix(self, sudoku):
        self.sudokuListHeaders(sudoku)
        pass
  
                            
    def insertSudokuRows(self,givenSudoku,names):
        for row in range(9) :
            for column in range(9) :
                for value in range(1,10):
                    if [row,column,value] not in givenSudoku:
                        if ((str(row)+str(column)) in names and ("r"+str(row)+str(value)) in names and ("c"+str(column)+str(value)) in names and ("sq"+str(cal_square(row,column))+str(value)) in names):
                            self.appendRow(str(row)+str(column),["r"+str(row)+str(value),"c"+str(column)+str(value),"sq"+str(sudoku.cal_square(row,column))+str(value)])
                        
        
    
    
    
     
        
        
        
        
    def smallestColumnObject(self):
        currentColumn = self.h.right
        currentSize = 10000
        while currentColumn != self.h :
            if currentSize > currentColumn.size :
                currentSize = currentColumn.size                    
                smallestColumn = currentColumn
            currentColumn = currentColumn.right
        return smallestColumn
    
    #Global variable for valid solutions 
    solutions = []
    zacka = []
    def calculatePentominoSolution(self,k,solution):
        if self.h == self.h.right:
        
            self.solutions.append(solution)
            for n in solution:
                self.zacka.append(n.name)
            return
        selectedColumn = self.smallestColumnObject()
        
        if selectedColumn.size <= 0:
            return
        
        currentCell = selectedColumn.down
        self.coverColumn(selectedColumn)
        while currentCell != selectedColumn:
            walkingCell = currentCell.right
            solution.append(walkingCell)
            while walkingCell != currentCell:
                self.coverColumn(walkingCell.listHeader)
                walkingCell = walkingCell.right
            self.calculatePentominoSolution(k+1,solution)
            solution.pop(k)
            walkingCell=currentCell.left
            while walkingCell!=currentCell:
                self.uncoverColumn(walkingCell.listHeader)
                walkingCell=walkingCell.left
            currentCell=currentCell.down
        self.uncoverColumn(selectedColumn)
            
        return       
                    
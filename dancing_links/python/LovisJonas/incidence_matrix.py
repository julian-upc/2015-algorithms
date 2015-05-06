import pentominos
import copy

from copy import deepcopy
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
        #print("vorher: " + str(rep))
        for i in range(n):
            #print(str(i)+":vorher" + str(listOfPlacementCells[i].representation()))
            if i==0:
                listOfPlacementCells[i].left=tileNameCell
            elif i in range(1,n):
                listOfPlacementCells[i].left=listOfPlacementCells[i-1]
            if i==n-1:
                listOfPlacementCells[i].right=tileNameCell
            elif i in range(n-1):
                listOfPlacementCells[i].right=listOfPlacementCells[i+1]
            #print("nachher" + str(listOfPlacementCells[i].representation()))
        rep = [n]
        for k in listOfPlacementCells:
            rep.append(k.representation())
        #print("nachher: " + str(rep))
        tileNameCell.left=listOfPlacementCells[n-1]
        tileNameCell.right=listOfPlacementCells[0]

        
        
        """ a placement is a list of coordinates that indicates which squares the piece named tileName covers"""
    
    def coverColumn(self, c):
        columnTile=c
        columnTile.left.right=columnTile.right
        columnTile.right.left=columnTile.left
        currentIncidentCell=columnTile.down
        currentIncidentCellHorizontal=columnTile.down
        while currentIncidentCell != columnTile:
            currentIncidentCellHorizontal=currentIncidentCell.right
            while currentIncidentCellHorizontal != currentIncidentCell:
                currentIncidentCellHorizontal.up.down=currentIncidentCellHorizontal.down
                currentIncidentCellHorizontal.down.up=currentIncidentCellHorizontal.up
                currentIncidentCellHorizontal.listHeader.size-=1
                currentIncidentCellHorizontal=currentIncidentCellHorizontal.right
            currentIncidentCell=currentIncidentCell.down
        
    def uncoverColumn(self, c):
        currentIncidentCell=c.up
        currentIncidentCellHorizontal=c.up
        while currentIncidentCell != c:
            currentIncidentCellHorizontal=currentIncidentCell.left
            while currentIncidentCellHorizontal != currentIncidentCell:
                currentIncidentCellHorizontal.up.down=currentIncidentCellHorizontal
                currentIncidentCellHorizontal.down.up=currentIncidentCellHorizontal
                currentIncidentCellHorizontal.listHeader.size+=1
                currentIncidentCellHorizontal=currentIncidentCellHorizontal.left
            currentIncidentCell=currentIncidentCell.up 
        c.left.right=c
        c.right.left=c
            
    def insertAllPlacements(self, pentomino):
        pentomino.normalize()
        versionList=pentominos.fixed_pentominos_of(pentomino)
        coordinatesListAsStrings=[]
        for p in versionList:
            for i in range(8):
                for k in range(8):
                    if p.legal():
                        for k in range(5):
                            coordinatesListAsStrings.append(str(p.coos[k][0])+str(p.coos[k][1]))
                        #print(coordinatesListAsStrings)
                        self.appendRow(p.name, coordinatesListAsStrings)
                    p.translate_one(1)
                    k+=1
                    coordinatesListAsStrings=[]
                p.translate_by([0,-10])
                p.translate_one(0)
                i+=1
            
        
    def initializeTheIncidenceMatrix(self):
        allPentos=pentominos.all_pentominos()
        for p in allPentos:
            self.insertAllPlacements(p)
    
    solution = []
    solutions = []
    
    def smallestColumnObject(self):
        currentColumnObject = self.h.right
        currentSize = self.h.size
        smallestColumnObject = currentColumnObject
        while currentColumnObject != self.h:
            if currentSize > currentColumnObject.size:
                currentSize = currentColumnObject.size
                smallestColumnObject = currentColumnObject
            currentColumnObject = currentColumnObject.right
        return smallestColumnObject
    
    def calculatePentominoSolution(self,k):
        
        if self.h.right == self.h:
            self.solutions.append(self.solution)
            self.solution = self.solution.pop
            return
    
        
        singlePentomino=[]
        smallestColumnObject = self.smallestColumnObject()
        currentIncidenceCell=smallestColumnObject.down
        self.coverColumn(smallestColumnObject)
        while currentIncidenceCell!=smallestColumnObject:
            walkingIncidenceCell=currentIncidenceCell.right
            singlePentomino.append(smallestColumnObject.name)
            while walkingIncidenceCell!=currentIncidenceCell:
                self.coverColumn(walkingIncidenceCell.listHeader)
                singlePentomino.append(walkingIncidenceCell.listHeader.name)
                walkingIncidenceCell=walkingIncidenceCell.right
            self.solution.append(singlePentomino)
            #print("Eine Pentomino:   "+ str(self.solution))
            self.calculatePentominoSolution(k+1)
            walkingIncidenceCell=currentIncidenceCell.left
            while walkingIncidenceCell!=currentIncidenceCell:
                self.uncoverColumn(walkingIncidenceCell.listHeader)
                walkingIncidenceCell=walkingIncidenceCell.left
            currentIncidenceCell=currentIncidenceCell.down
            
        self.solution.pop
        #print("test")
        #self.uncoverColumn(smallestColumnObject)
        #return
        
        
                    
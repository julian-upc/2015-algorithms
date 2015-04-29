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
        print(tileName)
        #print(placement)
        columnTile=self.columnObjectOfName[tileName]
        columnTile.size+=1
        tileNameCell=IncidenceCell(columnTile,columnTile,columnTile.up,columnTile,columnTile,tileName)
        listOfPlacementCells = []
        for position in placement:
            columnPlacement=self.columnObjectOfName[position]
            listOfPlacementCells.append(IncidenceCell(columnPlacement, columnPlacement, columnPlacement.up, columnPlacement, columnPlacement, position))
        n=len(listOfPlacementCells)
        for i in range(0,n-1):
            if i==0:
                print(listOfPlacementCells[i].representation())
                listOfPlacementCells[i].left=tileNameCell
                print(listOfPlacementCells[i].representation())
            elif i in range(1,n-1):
                listOfPlacementCells[i].left=listOfPlacementCells[i-1]
            if i==n-1:
                listOfPlacementCells[n-1].right=tileNameCell
            elif i in range(0,n-2):
                listOfPlacementCells[i].right=listOfPlacementCells[i+1]
        tileNameCell.left=listOfPlacementCells[n-1]
        tileNameCell.right=listOfPlacementCells[0]
        
        #columPositionTile0=self.columnObjectOfName[placement[0]]
        #positionTile0=IncidenceCell(cellTile, columnTile, columPositionTile0.up, columPositionTile0, columPositionTile0, placement[0])
        #columPositionTile1=self.columnObjectOfName[placement[0]]
        #positionTile1=IncidenceCell(positionTile0, columnTile, columPositionTile0.up, columPositionTile0, columPositionTile0, placement[1])
        #columPositionTile2=self.columnObjectOfName[placement[0]]
        #positionTile2=IncidenceCell(positionTile1, columnTile, columPositionTile0.up, columPositionTile0, columPositionTile0, placement[2])
        #columPositionTile3=self.columnObjectOfName[placement[0]]
        #positionTile3=IncidenceCell(positionTile2, columnTile, columPositionTile0.up, columPositionTile0, columPositionTile0, placement[3])
        #columPositionTile4=self.columnObjectOfName[placement[0]]
        #positionTile4=IncidenceCell(positionTile3, cellTile, columPositionTile0.up, columPositionTile0, columPositionTile0, placement[4])
        #positionTile0.right=positionTile1
        #positionTile1.right=positionTile2
        #positionTile2.right=positionTile3
        #positionTile3.right=positionTile4
        #cellTile.left=positionTile4
        #cellTile.right=positionTile0
        #self.rows+=1
        #self.indexOfPiecePlacement[tileName]+=1
        
        
        """ a placement is a list of coordinates that indicates which squares the piece named tileName covers"""
    
    def coverColumn(self, c):
        columnTile=c
        columnTile.left.right=columnTile.right
        columnTile.right.left=columnTile.left
        currentIncidentCell=columnTile.down
        currentIncidentCellHorizontal=columnTile.down
        while currentIncidentCell is not columnTile:
            currentIncidentCellHorizontal=currentIncidentCellHorizontal.right
            while currentIncidentCellHorizontal is not currentIncidentCell:
                currentIncidentCellHorizontal.up.down=currentIncidentCellHorizontal.down
                currentIncidentCellHorizontal.down.up=currentIncidentCellHorizontal.up
                currentIncidentCellHorizontal=currentIncidentCellHorizontal.right
            currentIncidentCell=currentIncidentCell.down
        
    def uncoverColumn(self, c):
        columnTile=self.columnObjectOfName[c]
        currentIncidentCell=columnTile.up
        currentIncidentCellHorizontal=columnTile.up
        while currentIncidentCell is not columnTile.up:
            currentIncidentCellHorizontal=currentIncidentCellHorizontal.left
            while currentIncidentCellHorizontal is not currentIncidentCell:
                currentIncidentCellHorizontal.up.down=currentIncidentCellHorizontal
                currentIncidentCellHorizontal.down.up=currentIncidentCellHorizontal
                currentIncidentCellHorizontal=currentIncidentCellHorizontal.left
            currentIncidentCell=currentIncidentCell.up 
        columnTile.left.right=columnTile
        columnTile.right.left=columnTile

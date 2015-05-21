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
        """ insert a column header object into the circular linked list that contains the "root" node """
        co = ColumnObject(left,right,None,None,name)
        co.up = co.down = left.right = right.left = co
        

    def appendRow(self, tileName, placement):
        """ 
        a placement is a list of coordinates that indicates which squares the piece named `tileName` covers.
        This function appends a row to the incidence matrix. A row consists of
        - one IncidenceCell in the column corresponding to tileName
        - one IncidenceCell in each column corresponding to a coordinate in `placement`.
        These must be assembled into a circularly linked list, and each cell must be inserted into the 
        circular linked list of its corresponding column.
        """
        tileCell = IncidenceCell(None,None, self.columnObjectOfName[tileName].up, self.columnObjectOfName[tileName], self.columnObjectOfName[tileName], tileName + "["+ str(self.indexOfPiecePlacement[tileName]) + "]")
        self.indexOfPiecePlacement[tileName] += 1	#?
        self.columnObjectOfName[tileName].size += 1
        tileCell.left = tileCell.right = tileCell.down.up = tileCell.up.down = tileCell
        for coo in sorted(placement):
	    cooCell = IncidenceCell(tileCell.left, tileCell, self.columnObjectOfName[str(coo)].up, self.columnObjectOfName[str(coo)], self.columnObjectOfName[str(coo)], tileName + str(coo))
	    cooCell.down.up = cooCell.up.down = cooCell.left.right = cooCell.right.left = cooCell
	    self.columnObjectOfName[str(coo)].size += 1
	self.rows += 1
	    

    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        
        #adjust links of the column objects
        c.left.right = c.right
        c.right.left = c.left
        
        #adjust all links in IncidenceCells which are in a row of c
        currRowCell = c.down
        while currRowCell is not c:
	    currColCell = currRowCell.right
	    while currColCell is not currRowCell:
		currColCell.down.up = currColCell.up
		currColCell.up.down = currColCell.down
		currColCell.listHeader.size -= 1
		currColCell = currColCell.right
	    currRowCell = currRowCell.down

    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        
        #adjust all links in IncidenceCells which are in a row of c
        currRowCell = c.down
        while currRowCell is not c:
	    currColCell = currRowCell.left
	    while currColCell is not currRowCell:
		currColCell.down.up = currColCell
		currColCell.up.down = currColCell
		currColCell.listHeader.size += 1
		currColCell = currColCell.left
	    currRowCell = currRowCell.down
	
	#adjust links of the column objects
        c.left.right = c
        c.right.left = c

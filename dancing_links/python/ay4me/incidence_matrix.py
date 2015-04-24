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
        self.listHeader = listHeader #points to ColumnObject of the relevant column
        self.name = name

    def representation(self):
        rep = ["c", self.name]
        for c in [self.left, self.right, self.up, self.down]:
            rep.append(c.name)
        return rep

        
class ColumnObject(IncidenceCell):
    def __init__(self, left, right, up, down, name):
        IncidenceCell.__init__(self, left, right, up, down, self, name)
        self.size = 0 #number of 1s in the column

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
        self.h.left = self.h.right = self.h.up = self.h.down = self.h #unused fields all point to h itself

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

    #creates new ColumnObject and inserts it between left and right
    def insertColumnObject(self, left, right, name):
        # __init__(self, left, right, up, down, name)
        newColumnObject = ColumnObject(left, right, None, None, name)
        newColumnObject.up = newColumnObject.down = newColumnObject #right now the column has only this element
        #change links in left and right
        left.right = newColumnObject
        right.left = newColumnObject

    def appendRow(self, tileName, placement):
        """ a placement is a list of coordinates that indicates which squares the piece named tileName covers"""
        for p in placement:
            if p not in columnObjectOfName: #add columns for placements, we not yet have in the matrix
                #error
                pass
        currentColumnObject = self.columnObjectOfName[tileName] #pentomino column
        #def __init__(self, left, right, up, down, listHeader, name):
        currentCell = self.IncidenceCell(None,None,currentColumnObject.up,currentColumnObject,currentColumnObject,"")
        currentCell.left = currentCell.right = currentCell #right now the row has only this element
        currentColumnObject.up.down = currentCell
        currentColumnObject.up = currentCell


        for col in placement:
            currentColumnObject = self.columnObjectOfName[col]
            newCell = self.IncidenceCell(currentCell,currentCell.right,currentColumnObject.up,currentColumnObject,currentColumnObject,"")
            currentColumnObject.up.down = newCell
            currentColumnObject.up = newCell
            currentCell.left.right = newCell
            currentCell.right = newCell
            currentCell = newCell

    #def insertIncidenceCell(self,):

    def coverColumn(self, c):
        pass

    def uncoverColumn(self, c):
        pass

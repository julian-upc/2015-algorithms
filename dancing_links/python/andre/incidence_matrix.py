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
        col = ColumnObject(left, right, None, None, name)
        col.up = col.down = left.right = right.left = col

    def appendRow(self, tileName, placement):
        """ 
        a placement is a list of coordinates that indicates which squares the piece named `tileName` covers.
        This function appends a row to the incidence matrix. A row consists of
        - one IncidenceCell in the column corresponding to tileName
        - one IncidenceCell in each column corresponding to a coordinate in `placement`.
        These must be assembled into a circularly linked list, and each cell must be inserted into the 
        circular linked list of its corresponding column.
        """
        header = self.columnObjectOfName[tileName]
        newName = tileName + "[" + str(self.indexOfPiecePlacement[tileName]) + "]"
        cell = IncidenceCell(None, None, header.up, header, header, newName)
        cell.left = cell.right = cell.up.down = cell.down.up = cell

        header.size += 1
        self.indexOfPiecePlacement[tileName] += 1

        tmpCell = cell
        for n in placement:
            newHeader = self.columnObjectOfName[n]
            newHeader.size += 1
            newCell = IncidenceCell(tmpCell, tmpCell.right, newHeader.up, newHeader, newHeader, tileName + n)
            newCell.left.right = newCell.right.left = newCell.up.down = newCell.down.up = newCell
            tmpCell = newCell

    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        # cover header
        c.left.right = c.right
        c.right.left = c.left
        
        rowCell = c.down
        while rowCell is not c:
            colCell = rowCell.right
            while colCell is not rowCell:
                colCell.down.up = colCell.up
                colCell.up.down = colCell.down
                colCell.listHeader.size -= 1
                colCell = colCell.right
            rowCell = rowCell.down

    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        rowCell = c.up
        while rowCell is not c:
            colCell = rowCell.left
            while colCell is not rowCell:
                colCell.listHeader.size += 1
                colCell.up.down = colCell.down.up = colCell
                colCell = colCell.left
            rowCell = rowCell.up
        c.left.right = c.right.left = c


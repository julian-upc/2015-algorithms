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
        colobj = ColumnObject(left, right, None, None, name)
        colobj.up = colobj.down = colobj
        left.right = colobj
        right.left = colobj

    def appendRow(self, tileName, placement):
        """ a placement is a list of coordinates that indicates which squares the piece named tileName covers"""
        tile = self.columnObjectOfName[tileName]
        cell = IncidenceCell(None, None, tile.up, tile, tile, str(tile.name) + "[" + str(self.indexOfPiecePlacement[tileName]) + "]")
        self.indexOfPiecePlacement[tileName] += 1
        tile.up.down = tile.up = cell
        tile.size += 1
        for place in placement:
            pcol = self.columnObjectOfName[place]
            pcell = IncidenceCell(None, None, pcol.up, pcol, pcol, str(tile.name) + str(pcol.name))
            pcol.up.down = pcell
            pcol.up = pcell
            pcell.left = cell
            cell.right = pcell
            cell = pcell
            pcol.size += 1
        cell.right = tile.up
        tile.up.left = cell 

    def coverColumn(self, c):
        #print(str(c.name))
        c.right.left = c.left
        c.left.right = c.right
        currow = c.down
        while currow is not c:
            curcell = currow.right
            while curcell is not currow:
                curcell.down.up = curcell.up
                curcell.up.down = curcell.down
                curcell.listHeader.size -= 1
                curcell = curcell.right
                #print(str(currow.name) + " " + str(curcell.name))
            currow = currow.down

    def uncoverColumn(self, c):
        currow = c.up
        while currow is not c:
            curcell = currow.left
            while curcell is not currow:
                curcell.down.up = curcell
                curcell.up.down = curcell
                curcell.listHeader.size += 1
                curcell = curcell.left
            currow = currow.up
        c.right.left = c
        c.left.right = c

    def is_valid_placement(self, coos):
        tiles = []
        j = self.h.right
        while j is not self.h:
            if is_number(j.name):
                tiles.append(j.name)
            j = j.right
        for c in coos:
            if str(c[0]) + str(c[1]) not in tiles:
                #print(str(coos) + " is not valid")
                return False    
        return True
            
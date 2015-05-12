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
        """ insert a column header object into the circular linked list 
            that contains the "root" node """
        newColumn = ColumnObject(left,right,None,None,name)
        newColumn.listHeader = newColumn
        newColumn.up = newColumn
        newColumn.down = newColumn
        newColumn.left.right = newColumn
        newColumn.right.left = newColumn
        return self

    def appendRow(self, tileName, placement):
        """ 
        a placement is a list of coordinates that indicates which squares the piece named `tileName` covers.
        This function appends a row to the incidence matrix. A row consists of
        - one IncidenceCell in the column corresponding to tileName
        - one IncidenceCell in each column corresponding to a coordinate in `placement`.
        These must be assembled into a circularly linked list, and each cell must be inserted into the 
        circular linked list of its corresponding column.
        """
        #try to insert a row on given columnOfName[tileName], 
        # this could fail, if there is no such ColumnObject 
        try:
        # Add a cell (corresponding to pentomino) at the end of the 
        # matching pentomino type Column
            currentColumn = self.columnObjectOfName[tileName]
            # The name is e.g. I[1] for the 2nd Pentomino of type I.
            pentoCellName = tileName + '[' + str(currentColumn.size) + ']'
            newPentoCell = IncidenceCell(None,None,currentColumn.up,
                                currentColumn, currentColumn, pentoCellName)
            # rearrange the links of the circularly list and upgrade the size            
            currentColumn.up.down = newPentoCell            
            currentColumn.up = newPentoCell
            self.columnObjectOfName[tileName].size += 1
        # add 5 cells (corresponding to placement of pentomino) at the 
        # end of the matching Coordinate Columns
            placement.sort()
            leftNeighbour = newPentoCell
            for co in placement:
                currentColumn = self.columnObjectOfName[co]
                # the name us e.g. I00, if this I pentomino covers the place 00
                cooCellName = tileName + currentColumn.name 
                newCooCell = IncidenceCell(leftNeighbour,None,currentColumn.up,
                                currentColumn,currentColumn,cooCellName)
                # rearrange the links of the current circular lists and 
                # upgrade the size                 
                leftNeighbour.right = newCooCell
                currentColumn.up.down = newCooCell            
                currentColumn.up = newCooCell
                leftNeighbour = newCooCell
                currentColumn.size += 1
            # links the beginning of this row (the pentominoCell) with the end
            # of this row (last placementCell) --> circular list
            newPentoCell.left = leftNeighbour
            leftNeighbour.right = newPentoCell
            return self
        except:
            print('There accured a problem appending a row in column'+tileName)
    
    # The operation of covering column c removes c from the header list and 
    # removes all rows in c's own list from the other column lists they are in
    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper.""" 
        # nehme den Header der Spalte c        
        curr = c.listHeader
        # setze fuer alle Objekte in c den Linken und rechten Zeiger um
        c.right.left = c.left
        c.left.right = c.right
        # merke dir das erste Element unter dem Header
        d = curr.down
        # iteriere ueber die Spalte von oben nach unten
        while d is not curr:
            # merke dir das naechste Element in der Zeile
            r = d.right
            # iteriere ueber die Zeile von links nach rechts
            while r is not d:
                # setze fuer alle Elemente in dieser Zeile die Zeiger fuer up & down um
                r.down.up = r.up
                r.up.down = r.down
                # gehe eins weiter die Zeile entlang
                d.right = r.right
            # gehe ein Element weiter die Spalte entlang
            d = d.down
            # verkuerze die Laenge der Spalte um 1, da eine Zeile abgearbeitet wurde
            c.size = c.size-1 # koennte falsch sein
        return self
                      
    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper.""" 
        curr = c.listHeader
        i = curr.up
        # iteriere ueber die Spalte von unten nach oben
        while i is not curr:
            j = i.left
            # iteriere ueber die Zeile links nach rechts
            while j is not i:
                c.size = c.size+1 # koennte falsch sein
                # 
                j.down.up = j
                j.up.down = j
                # iteriere in der Zeile eins weiter
                j = j.left
            # dies mit der oberen Schleife tauschen!??!? Nochmal in Ruhe durchdenken    
            curr.right.left = curr
            curr.left.right = curr
            curr = curr.up
        return self
        
            
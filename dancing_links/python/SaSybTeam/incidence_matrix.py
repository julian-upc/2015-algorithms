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
        # size gives the number of Cells in total in a Column        
        self.size = 0
        # masterSize gives the number of leading Cells in a Column
        self.masterSize = 0        
        # this is kind of confusing, because in our problem, there should be no 
        # difference between size and masterSize
        # this is only needed, if there is a column that is for a pentomnio AND 
        # for a placement, which makes (at least in my head) no sence
        
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
        # try to append a row to the Incidence_Matirx,
        # starting with a new IncidenceCell at the end of a given Column. 
        # this could fail, if there is no such ColumnObject 
        try:
        # Add a masterCell (corresponding to given tileName) at the end
        # of the matching pentomino/coordinate type column
            masterColumn = self.columnObjectOfName[tileName]
            # The name is e.g. 'C[1]' for the 2nd Pentomino of type C.
            # Notice: A possible columnObject C could be:
            #        'C','C[0]','AC','IC', 'C[1]', size=4, masterSize=2 
            masterCellName = tileName + '[' + str(masterColumn.masterSize) + ']'
            newMasterCell = IncidenceCell(None,None,masterColumn.up,
                                masterColumn, masterColumn, masterCellName)
            # rearrange the links of the circularly lists and upgrade the sizes            
            masterColumn.up.down = newMasterCell            
            masterColumn.up = newMasterCell
            masterColumn.size += 1
            masterColumn.masterSize += 1
        # add cells (corresponding to the list 'placement') at the 
        # end of the matching Coordinate/Pentomino Columns
            placement.sort() #this should make example-creating more easier
            leftNeighbour = newMasterCell
            for place in placement:
                currColumn = self.columnObjectOfName[place]
                # the name is e.g. I00, if this I pentomino covers the place 00
                placeCellName = tileName + place 
                newPlaceCell = IncidenceCell(leftNeighbour,None,currColumn.up,
                                currColumn,currColumn,placeCellName)
                # rearrange the links of the current circular lists and 
                # upgrade the size    
                currColumn.up.down = newPlaceCell            
                currColumn.up = newPlaceCell
                currColumn.size += 1 
                    # Notice: masterSize needs no upgrade here! a placeCell 
                    #         is not a masterCell
                leftNeighbour.right = newPlaceCell
                leftNeighbour = newPlaceCell
            # links the beginning of this row (the masterCell) with the end
            # of this row (last placeCell) --> circular list
            leftNeighbour.right = newMasterCell
            newMasterCell.left = leftNeighbour            
            self.rows += 1
            return self
        except:
            print('There accured a problem appending a row in column'+tileName)
    
    def coverColumn(self, c):
        """ removes c from the header list and removes all rows in c s own list
            from the other column lists they are in 
        """
        if c!=self.h:
            try:
                c.left.right = c.right
                c.right.left = c.left
                currRow = c.listHeader
                for i in range(c.size):
                    currRow = currRow.down
                    currPlacement = currRow.right
                    while currPlacement.listHeader != c.listHeader:
                        currPlacement.up.down = currPlacement.down
                        currPlacement.down.up = currPlacement.up
                        currPlacement.listHeader.size = currPlacement.listHeader.size-1
                        currPlacement = currPlacement.right
                    self.rows -= 1
                return self
            except:
                print('No matching column found to cover')
        else:
            print('You cannot cover the root h')
        
    def uncoverColumn(self, c):
        """ uncover a given column c, this is where the links do their dance
        """
        if c != self.h:
            try:
                currRow = c
                for i in range(c.size):
                    currRow = currRow.up
                    currPlacement = currRow.left
                    while currPlacement.listHeader != c.listHeader:                    
                        currPlacement.listHeader.size = currPlacement.listHeader.size+1
                        currPlacement.down.up = currPlacement
                        currPlacement.up.down = currPlacement
                        currPlacement = currPlacement.left
                    self.rows += 1
                c.right.left = c
                c.left.right = c
                return self
            except:
                print('No matching column found to uncover')
        else:
            print('you cannot uncover the root h')
    """    
    # The operation of covering column c removes c from the header list and 
    # removes all rows in c's own list from the other column lists they are in
    def coverColumn(self, c):
        # implement and document the algorithm in Knuth's paper. 
        # nehme den Header der Spalte c. Note to self: funktioniert nicht!      
        # curr = c.listHeader
        # nehme c als aktuelles Objekt!
        # setze fuer alle Objekte in c den Linken und rechten Zeiger um
        c.right.left = c.left
        c.left.right = c.right
        # merke dir das erste Element unter dem Header
        d = c.down
        # iteriere ueber die Spalte von oben nach unten
        while d is not c:
            #print('in Schleife 1 cover')
            # merke dir das naechste Element in der Zeile
            r = d.right
            # iteriere ueber die Zeile von links nach rechts
            while r is not d:
                #print('in Schleife 2 cover')
                # setze fuer alle Elemente in dieser Zeile die Zeiger fuer up & down um
                r.down.up = r.up
                r.up.down = r.down
                # verkuerze die Laenge der Spalte um 1, da eine Zeile abgearbeitet wurde
                r.listHeader.size -= 1 # koennte falsch sein
                # gehe eins weiter die Zeile entlang
                r = r.right
            # gehe ein Element weiter die Spalte entlang
            d = d.down
            # verkuerze die Laenge der Zeilen um 1, da eine Spalte entfernt wurde
            #self.rows = self.rows-1
        return self
    
    def uncoverColumn(self, c):
        # implement and document the algorithm in Knuth's paper.
        # nehme c und nicht c.listHeader!
        # curr = c.listHeader
        i = c.up
        # iteriere ueber die Spalte von unten nach oben
        while i is not c:
            j = i.left
            # iteriere ueber die Zeile links nach rechts
            while j is not i:
                j.listHeader.size += 1 # koennte falsch sein
                j.down.up = j
                j.up.down = j
                # iteriere in der Zeile eins weiter
                j = j.left
                # setze die Laenge neu
            # gehe eins weiter
            c = c.up
            # erhoehe die Laenge der Zeilen um 1, da eine Spalte hinzugefuegt
           # self.rows = self.rows+1
        c.right.left = c
        c.left.right = c
        return self
        
        """    
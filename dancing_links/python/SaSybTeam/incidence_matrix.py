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
        # size gives the number of cells in total in a column        
        self.size = 0
        # masterSize gives the number of leading cells in a column
        self.masterSize = 0        
        # this is kind of confusing, because in our problem, there should be no 
        # difference between size and masterSize
        # this is only needed, if there is a column that is for a pentomnio AND 
        # for a placement, which makes (at least in my head) no sense
        # NOTE Sa to Syb: compare with page 5 'root h, 
        # which serves as a master header for all active headers'
        
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
        # try to append a row to the Incidence_Matrix,
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
                # NOTE: it would be better to use MasterCellName to get a unique representation
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
    
    # The operation of covering column c removes c from the header list and 
    # removes all rows in c's own list from the other column lists they are in
    def coverColumn(self, c):
        """ removes c from the header list and removes all rows in c s own list
            from the other column lists they are in 
        """
        # implement and document the algorithm in Knuth's paper. 
        if c!=self.h:
            try:
                # take the header of column c
                currRow = c.listHeader
                 # change the left and right link of c 
                c.right.left = c.left
                c.left.right = c.right
                # iterate over the column c from top to bottom
                for i in range(c.size):
                    # note: there should be no difference between runtime 
                    # with a for or a while loop
                    # while currRow is not c:
                    # currRow == d in the paper
                    # one step further down the column
                    currRow = currRow.down
                    # remember the next element in the row
                    # currPlacement == r in the paper
                    currPlacement = currRow.right
                    # iterate over the row from left to right and change
                    # the pointers for up & down for all elements in the row
                    while currPlacement.listHeader != c.listHeader:
                        currPlacement.down.up = currPlacement.up
                        currPlacement.up.down = currPlacement.down
                        # update size of column - one row has been 'finished'
                        currPlacement.listHeader.size -= 1
                        # one step further along the row
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
        # implement and document the algorithm in Knuth's paper.
        if c != self.h:
            try:
                # currRow == i in the paper
                currRow = c
                # iterate over the column bottom to top
                for i in range(c.size):
                    currRow = currRow.up
                    # currPlacement == j in the paper
                    currPlacement = currRow.left
                    # iterate over the row left to right
                    while currPlacement.listHeader != c.listHeader:                    
                        currPlacement.listHeader.size += 1
                        currPlacement.down.up = currPlacement
                        currPlacement.up.down = currPlacement
                        # walk one step further in the row
                        currPlacement = currPlacement.left
                    self.rows += 1
                c.right.left = c
                c.left.right = c
                return self
            except:
                print('No matching column found to uncover')
        else:
            print('you cannot uncover the root h')
         
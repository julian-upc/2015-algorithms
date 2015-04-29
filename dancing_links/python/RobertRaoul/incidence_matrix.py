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
        
        
        newColumn=ColumnObject(left,right,None,None,name)
        newColumn.up=newColumn.down=newColumn
        newColumn.left.right=newColumn
        newColumn.right.left=newColumn



    def appendRow(self, tileName, placement):
        """ 
        a placement is a list of coordinates that indicates which squares the piece named `tileName` covers.
        This function appends a row to the incidence matrix. A row consists of
        - one IncidenceCell in the column corresponding to tileName
        - one IncidenceCell in each column corresponding to a coordinate in `placement`.
        These must be assembled into a circularly linked list, and each cell must be inserted into the 
        circular linked list of its corresponding column.
        """
        pass

    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        
        #c dances horizontally out of the list
        c.left.right=c.right
        c.right.left=c.left
        #initialize a field current_c_cell to travel down the column c
        current_d_cell=c.down
        #in every row of c let all cells but the cell in column c dance vertically out of the list
        while current_d_cell != c:
            current_r_cell=current_d_cell.right
            while current_r_cell != current_d_cell:
                #the dance out and update size(-1)
                current_r_cell.up.down=current_r_cell.down
                current_r_cell.down.up=current_r_cell.up
                current_r_cell.listHeader.size-=1
                #travel right in the row
                current_r_cell=current_r_cell.right
            
            #travel down column c
            current_d_cell=current_d_cell.down

    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """

        #we just undo the covering of c, so we start by going UP!
        #initialize a field current_c_cell to travel up the column c
        current_u_cell=c.up
        #in every row of c let all cells but the cell in column c dance vertically out of the list
        while current_u_cell != c:
            current_l_cell=current_u_cell.left
            while current_l_cell != current_u_cell:
                #the dance back in line and update size(+1)
                current_l_cell.up.down=current_l_cell
                current_l_cell.down.up=current_l_cell
                current_l_cell.listHeader.size+=1
                #travel LEFT in the row
                current_l_cell=current_l_cell.left
            
            #travel up column c
            current_u_cell=current_u_cell.up
            
        #finally c dances horizontally back in the header list    
        c.left.right=c
        c.right.left=c   
            
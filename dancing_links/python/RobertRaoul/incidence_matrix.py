
import pentominos


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
    
    counter = 0
    
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
        print(names)

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
        #TODO selber
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

    #Hallo Welt
    def coverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """
        if c != c.left.right:
            print("falsches covern")
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
            self.rows-=1

    def uncoverColumn(self, c):
        """ implement and document the algorithm in Knuth's paper. """

        #we just undo the covering of c, so we start by going UP!
        #initialize a field current_c_cell to travel up the column c
        current_u_cell=c.up
        current_u_cell_horizontal=c.up
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
            self.rows+=1
        #finally c dances horizontally back in the header list    
        c.left.right=c
        c.right.left=c
        
    def appendPentominoRows(self, pentomino):
        pentomino.normalize()
        coords = []
        for p in pentominos.fixed_pentominos_of(pentomino):   
            for i in range(8):
                for j in range(8):
                    if p.legal():
                        for k in range(5):
                            coords.append(str(p.coos[k][0])+str(p.coos[k][1])) 
                        self.appendRow(p.name, coords)
                    p.translate_one(0)
                    coords=[]
                p.translate_by([-8,0])
                p.translate_one(1)
                
                
                
    def initializeIncidenceMatrix(self):
        for p in pentominos.all_pentominos():
            self.appendPentominoRows(p)
            print(str(self.rows))

    def solve(self):
        solution = []
        self.algo(solution)
        print(len(solution))
        
    def algo(self, solution):
        if(self.h.right == self.h):
            self.counter = self.counter+1
            print(self.counter)
            if self.isLegalSolution(solution):
                print("check")
            #print("solution: " + str(len(solution)))
            #for row in solution:
               # self.printRow(row)
            return
        
        
        column = self.chooseColumnObject()
        if column.name == "root":
            return
        else:
            self.coverColumn(column)
            r = column.down
            while r != column:
                solution.append(r)
                j = r.right
                while j != r:
                    self.coverColumn(j.listHeader)
                    j = j.right
                self.algo(solution)
                solution.pop(len(solution)-1)
                #column = r.listHeader #ToDo check if line is really needed
                j = r.left
                while j != r:
                    self.uncoverColumn(j.listHeader)
                    j = j.left
                r = r.down
            self.uncoverColumn(column)
            
            return
                
    def printRow(self, row):
        string = ""
        string = string + row.listHeader.name + " "
        current = row.right
        while current != row:
            string = string + current.listHeader.name + " "
            current = current.right
        print(string)
        
    def chooseColumnObject(self):
        size = self.h.right.size
        column = self.h.right
        current = self.h.right
        while current != self.h:
            if current.size < size:
                size = current.size
                #ToDo check if deep_copying is needed
                column = current
            current = current.right
        if size < 1:
            return self.h
        return column
    
    def isLegalSolution(self, solution):
        all = set()
        for i in solution:
            all.add(i.listHeader.name)
            current = i.right
            while current != i:
                all.add(current.listHeader.name)
                current = current.right
                
        if len(all) == 72:
            return True
        else: 
            return False 
            
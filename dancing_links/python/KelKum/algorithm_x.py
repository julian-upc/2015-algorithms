import incidence_matrix
import pentominos
import examples
import copy

class Algorithm_X(object):
    def __init__(self, matrix):
        self.matrix = matrix
        #print(self.matrix.columnObjectOfName.keys())
        #self.o = []
        self.search(0, [])
        #print(self.matrix.representation())
    
    def search(self, k, o):
        #print("search k = " + str(k) + " R[h] = " + str(self.matrix.h.right.name))
        if self.matrix.h.right == self.matrix.h:
            print("All pentominos placed")
            print_current_solution(o)
            return
        c = self.chooseColumnObj()
        self.matrix.coverColumn(c)
        #print("column c covered")
        #print(str(c.representation()))
        r = c.down
        while r is not c:
            #print(str(r.name) + " " + str(c.down.name))
            #o.append(r)
            j = r.right
            while j is not r:
                #print(str(j.name) + " " + str(j.listHeader.name))
                self.matrix.coverColumn(j.listHeader)
                j = j.right
            self.search(k + 1, o + [r])
            j = r.left
            while j is not r:
                self.matrix.uncoverColumn(j.listHeader)
                j = j.left
            r = r.down
        self.matrix.uncoverColumn(c)
        
    def print_current_solution(self, o):
        for obj in o:
            s = str(obj.listHeader.name)
            r = obj.right
            while r is not obj:
                s += " " + str(r.listHeader.name)
                r = r.right
            print(s + "\n")
        print("\n")
                
    def chooseColumnObj(self):
        #print("choose column object")
        c = self.matrix.h
        s = 1e100000
        j = self.matrix.h.right
        while j is not self.matrix.h and not incidence_matrix.is_number(j.name):
            if j.size < s:
                c = j
                s = j.size
            j = j.right
        #print(str(c.representation()))
        return c
        
def append_all_possible_placements(matrix):
    names = []
    tiles = []
    currentColumnObject = matrix.h.right
    while currentColumnObject.name is not "root":
        if incidence_matrix.is_number(currentColumnObject.name):
            tiles.append(currentColumnObject.name)
        else:
            names.append(currentColumnObject.name)
        currentColumnObject = currentColumnObject.right
    pset = pentominos.fixed_pentominos_of_name_list(names)
    #print(str(len(names)) + " " + str(pset.size()))
    max0 = max([int(s[0]) for s in tiles])
    max1 = max([int(s[1]) for s in tiles])
    #print(str(max0) + " " + str(max1))
    for p in pset.set:
        for i in range(0, max0):
            for j in range(0, max1):
                q = copy.deepcopy(p)
                q.translate_by([i, j])
                if matrix.is_valid_placement(q.coos):
                    matrix.appendRow(q.name, [str(c[0]) + str(c[1]) for c in q.coos])
        
def run_scott_example():
    matrix = examples.scott_example()
    #print(str(matrix.representation()))
    append_all_possible_placements(matrix)
    #print(str(matrix.representation()))
    Algorithm_X(matrix)    

if __name__ == '__main__':
    run_scott_example()
    
    
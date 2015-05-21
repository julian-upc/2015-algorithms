import pentominos
import incidence_matrix
import examples
import copy

class Scott_matrix(object):
    def __init__(self, width, height):
        self.width = 8;
        self.height = 8;
        self.solution = dict()

        self.noSolutions = 0

    
    def create_scott_matrix(self, legal):
        self.IM = examples.scott_example()

        for p in pentominos.all_fixed_pentominos():
#            if p.name in ["I","L","U","V","Y"]:#TODO remove
                self.create_all_rows_for(p, legal)
        self.solve_scott_matrix()
        return self.IM

    def solve_scott_matrix(self):
        self.search(0)
        print("#sol="+str(self.noSolutions))

    def search(self, i):
        if self.IM.h.right == self.IM.h:
            #TODO solution found
            #print("\none solution is")
            #for j in range(i):
            #    print(str(self.solution[j].rowRep()))
            self.noSolutions += 1
            return
        #search column with min possibilities
        minPossibilities = curr = self.IM.h.right
        while curr != self.IM.h:
            if curr.size < minPossibilities.size:
                minPossibilities = curr
            curr = curr.right

        #cover c
        self.IM.coverColumn(minPossibilities)
        #start deeper search (play all scenarios, where c could be placed. one after another)
        currPlace = minPossibilities.down
        while currPlace != minPossibilities:

            self.solution[i] = currPlace
            #cover places, which are blocked now
            curr = currPlace.right
            while curr != currPlace:
                self.IM.coverColumn(curr.listHeader)
                curr = curr.right
            
            self.search(i+1)

            #uncover curr
            curr = currPlace.left
            while curr != currPlace:
                self.IM.uncoverColumn(curr.listHeader)
                curr = curr.left
            currPlace = currPlace.down

        #uncover c
        self.IM.uncoverColumn(minPossibilities)

    def create_all_rows_for(self, p, legal):
        #p.normalize();
        for i in range(self.width):
            for j in range(self.height):
                if legal(copy.deepcopy(p)):
                    #placement = []
                    #for pos in p.coos:
                    #    placement.append(str(pos[0])+str(pos[1]))
                    #print(" p"+p.name+" ij="+str(i)+str(j)+"  "+str([str(pos[0])+str(pos[1]) for pos in p.coos]))
                    #self.IM.appendRow(p.name, placement) #([[c[0]+1,c[1]] for c in pentominos.I().coos]
                    self.IM.appendRow(p.name, [str(pos[0])+str(pos[1]) for pos in p.coos])
                p.translate_one(1);
            p.normalize_coo(1);
            p.translate_one(0);

    def scott_legal(self, p):
        for hole in [ [3,3],[3,4],[4,3],[4,4] ]:
            if hole in p.coos:
                return False
        if p.max()[0] > self.width-1 or p.max()[1] > self.height-1:
            return False;
        return True


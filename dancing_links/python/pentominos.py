import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos #coordinates
        self.dim = len(coos[0])
        return self
        
    def normalize_coo(self, coo):
        ref = self.min_box() #current position
        offset = ref[coo]
        if coo==1:
            self.translate_by[0,min_box[1]]
        else:
            self.translate_by[min_box[0],0]
        return self

    def normalize(self):
        if self.name == "F":
            self.coos = [[0,1],[1,0],[1,1],[1,2],[2,2]]
        elif self.name == "I":
            self.coos = [[0,0],[0,1],[0,2],[0,3],[0,4]]
        elif self.name == "L":
            self.coos = [[0,0],[0,1],[0,2],[0,3],[1,0]]
        elif self.name == "P":
            self.coos = [[0,0],[0,1],[0,2],[1,1],[1,2]]
        elif self.name == "N":
            self.coos = [[0,0],[0,1],[1,1],[1,2],[1,3]]
        elif self.name == "T":
            self.coos = [[0,2],[1,0],[1,1],[1,2],[2,2]]
        elif self.name == "U":
            self.coos = [[0,0],[0,1],[1,0],[2,0],[2,1]]
        elif self.name == "V":
            self.coos = [[0,0],[1,0],[2,0],[2,1],[2,2]]
        elif self.name == "W":
            self.coos = [[0,0],[1,0],[1,1],[2,1],[2,2]]
        elif self.name == "X":
            self.coos = [[0,1],[1,0],[1,1],[1,2],[2,1]]
        elif self.name == "Y":
            self.coos = [[0,0],[1,0],[2,0],[2,1],[3,0]]
        elif self.name == "Z":
            self.coos = [[0,2],[1,0],[1,1],[1,2],[2,0]]
        else:
            #error
            print "This is not a pentomino, I cannot normalize it."
        return self

    def flip(self, coo):
        #1 : flip along x-axis (y-values change)
        #0 : flip along y-axis (x-values change)
        # flip along axis of the first coordinate
        flip_point = self.coos[0] #get reference point
        flip_value = flip_point[coo] #get reference coordinate value
        offset = 0 #how far away from reference point
        for c in self.coos:
            offset = c[coo] - flip_value
            c[coo] = c[coo] - 2*offset
        return self
        
    def translate_one(self, coo):
        #0: move one on x-axis
        #1: move one on y-axis
        for c in self.coos:
            c[coo] = c[coo]+1
        return self

    def translate_coo(self, coo, amount):
        for c in self.coos:
            c[coo] = c[coo]+ amount
        return self

    def translate_by(self, by_vector):
        x_shift = by_vector[0]
        y_shift = by_vector[1]
        for c in self.coos:
            c[0] = c[0]+ x_shift
            c[1] = c[1]+ y_shift
        return self

    def turn90(self):
        ref_point = self.min_box()
        self.translate_by([-ref_point[0],-ref_point[1]]) #move pentomino to origin
        # Now turn around origin
        for c in self.coos:
            x = c[0]
            y = c[1]
            c[0] = y
            c[1] = -x
        pos = self.min_box()
        #normalise back into positive space
        if pos[0]<0:
            self.translate_coo(0,-pos[0])
        if pos[1]<0:
            self.translate_coo(1,-pos[1])
        self.translate_by(ref_point) #move back to former position
        return self

    #returns smallest field of bounding box
    def min_box(self):
        min_x = self.coos[0][0]
        min_y = self.coos[0][1]
        for c in self.coos:
            if c[0]< min_x:
                min_x = c[0]
            if c[1]< min_y:
                min_y = c[1]
        # min_x,min_y smallest field of bounding box
        return [min_x,min_y]

    def max(self):
        max_value = 0
        max_coos = [0,0]
        for c in self.coos:
            x = c[0]
            y = c[1]
            if max_value < x+y:
                max_value = x+y
                max_coos = [x,y]
        return max_coos

    def __hash__(self):
        ref = self.min_box()
        self.translate_by([-ref[0],-ref[1]]) #move pentomino to origin
        bitstring = []
        for j in range(5):
            for i in range(5):
                if [4-i,4-j] in self.coos:
                    bitstring.append('1')
                else:
                    bitstring.append('0')
        self.translate_by(ref) #move back to former position
        return int(''.join(bitstring), 2)


    #two different pentominos are equal iff they have same name and orientation
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
        #to use the hashfunction for equality checks is only ok, because it is perfect and no collisions can happen

    def representation(self):
        return "[" + self.name + ":" + str(self.coos) + "]"



class F(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "F", [[0,1],[1,0],[1,1],[1,2],[2,2]])

class I(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "I", [[0,0],[0,1],[0,2],[0,3],[0,4]])

class L(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "L", [[0,0],[0,1],[0,2],[0,3],[1,0]])

class N(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "N", [[0,0],[0,1],[1,1],[1,2],[1,3]])

class P(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "P", [[0,0],[0,1],[0,2],[1,1],[1,2]])

class T(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "T", [[0,2],[1,0],[1,1],[1,2],[2,2]])

class U(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "U", [[0,0],[0,1],[1,0],[2,0],[2,1]])

class V(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "V", [[0,0],[1,0],[2,0],[2,1],[2,2]])

class W(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "W", [[0,0],[1,0],[1,1],[2,1],[2,2]])

class X(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "X", [[0,1],[1,0],[1,1],[1,2],[2,1]])

class Y(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "Y", [[0,0],[1,0],[2,0],[2,1],[3,0]])

class Z(Pentomino):
    def __init__(self):
        Pentomino.__init__(self, "Z", [[0,2],[1,0],[1,1],[1,2],[2,0]])

def fixed_pentominos_of(f):
    pent = TileSet()
    pent.add(f)
    f.turn90()
    pent.add(f)
    f.turn90()
    pent.add(f)
    f.turn90()
    pent.add(f)
    f.turn90()
    f.flip(0)
    pent.add(f)
    f.turn90()
    pent.add(f)
    f.turn90()
    pent.add(f)
    f.turn90()
    pent.add(f)
    return pent

def all_fixed_pentominos():
    pent = TileSet()
    pent.update(fixed_pentominos_of(F()))
    pent.update(fixed_pentominos_of(I()))
    pent.update(fixed_pentominos_of(L()))
    pent.update(fixed_pentominos_of(P()))
    pent.update(fixed_pentominos_of(N()))
    pent.update(fixed_pentominos_of(T()))
    pent.update(fixed_pentominos_of(U()))
    pent.update(fixed_pentominos_of(V()))
    pent.update(fixed_pentominos_of(W()))
    pent.update(fixed_pentominos_of(X()))
    pent.update(fixed_pentominos_of(Y()))
    pent.update(fixed_pentominos_of(Z()))
    return pent


def all_pentominos():
    return [F(), I(), L(), P(), N(), T(), U(), V(), W(), X(), Y(), Z()]

#The purpose of TileSet is to store one representative of each orientation of a pentomino, in normalized coordinates.
#That is to say, two translated copies should be merged into one, but a chiral pentomino and its reflected copy should be two different elements in the set.
class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        present = 0
        for q in self.set:
            if p==q:
                present = 1
        if present == 0:
            self.set.add(copy.deepcopy(p))

    def size(self):
        return len(self.set)

    def update(self,other):
        self.set |= other.set
        return self

    def representation(self):
        rep = "["
        i = 0
        for p in self.set:
            if i>0:
                rep += ","
            else:
                i = 1
            rep += str(p.coos)
        rep += "]"
        return rep



import copy
import numpy as np

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        self.coos.sort() # safety first ;)

    # normalize only one dimension
    def normalize_coo(self, coo):
        min = self.coos[0][coo]
        for i in range(1,5):
            if min > self.coos[0][coo]:
                min = self.coos[0][coo]
        self.translate_coo( coo, -min )
        return self

    # normalize object
    def normalize(self):
        # find bounding box left bottom corner
        minX = self.coos[0][0]
        minY = self.coos[0][1]

        for i in range(1,5):
            if minX > self.coos[i][0]:
                minX = self.coos[i][0]
            if minY > self.coos[i][1]:
                minY = self.coos[i][1]

        # translate this object to origin
        self.translate_by( [-minX,-minY] )
        return self

    def flip(self, coo):
        for i in range(len(self.coos)):
            self.coos[i][coo] = -self.coos[i][coo]
        self.normalize()
        return self
        
    def translate_one(self, coo):
        self.translate_coo(coo, 1)
        self.coos.sort()
        return self

    def translate_coo(self, coo, amount):
        for i in range(0,5):
            self.coos[i][coo] += amount
        self.coos.sort()
        return self

    def translate_by(self, by_vector):
        for i in range(0,5):
            self.coos[i][0] += by_vector[0]
            self.coos[i][1] += by_vector[1]
        self.coos.sort()
        return self

    def turn90(self):
        # create a rotation matrix
        rotMatrix = np.matrix([[0,1],[-1,0]])

        # rotate each vector
        for i in range(0,5):
            convert = np.transpose(np.matrix(self.coos[i]))
            self.coos[i] = np.transpose(rotMatrix * convert)

        # convert back to native list
        self.coos = np.array(self.coos).reshape(5,2).tolist()

        # normale position
        self.normalize()
        return self

    def max(self):
        max = [self.coos[0][0], self.coos[0][1]]
        for i in range(1,len(self.coos)):
            if max[0] < self.coos[i][0]:
                max[0] = self.coos[i][0]
            if max[1] < self.coos[i][1]:
                max[1] = self.coos[i][1]

        return max

    def __hash__(self):
        return hash(str(self.coos))

    def __eq__(self, other):
        return hash(self) == hash(other)

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


def all_pentominos():
    return [F(), I(), L(), P(), N(), T(), U(), V(), W(), X(), Y(), Z()]

def fixed_pentominos_of(pentomino):
    c = copy.deepcopy(pentomino)
    s = TileSet()

    for i in range(4):
        s.add(c.turn90())
        s.add(c.flip(i%2))
        c.flip(i%2) # flip back for rotation

    return s

def all_fixed_pentominos():
    all = TileSet()

    for p in all_pentominos():
        pentSet = fixed_pentominos_of(p)
        all.add_all(pentSet)

    return all

class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        # test first, if this p is still known
        for q in self.set:
            if q == p:
                return
        self.set.add(copy.deepcopy(p))

    def add_all(self, set):
        for p in set:
            self.add(p)

    def size(self):
        return len(self.set)

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

import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        coo_min = self.coos[len(self.coos) - 1][coo]
        for i in range(len(self.coos) - 1):
            if coo_min > self.coos[i][coo]:
                coo_min = self.coos[i][coo]
        self.translate_coo(coo, -coo_min)
        return self

    def normalize(self):
        for coo in range(self.dim):
            self.normalize_coo(coo)
        self.coos.sort()
        return self

    def flip(self, coo):
        for i in range(len(self.coos)):
            self.coos[i][(coo+1)%2] = - self.coos[i][(coo+1)%2];
        self.normalize()
        return self
        
    def translate_one(self, coo):
        for i in range(len(self.coos)):
            self.coos[i][coo] = self.coos[i][coo] + 1;
        return self

    def translate_coo(self, coo, amount):
        for i in range(len(self.coos)):
            self.coos[i][coo] = self.coos[i][coo] + amount;
        return self

    def translate_by(self, by_vector):
        for i in range(len(self.coos)):
            for coo in range(self.dim):
                self.coos[i][coo] = self.coos[i][coo] + by_vector[coo];
        return self

    def turn90(self):
        x = 0
        for i in range(len(self.coos)):
            x = self.coos[i][0]
            self.coos[i][0] = - self.coos[i][1]
            self.coos[i][1] = x
        self.normalize()
        return self

    def max(self):
        compmax = self.coos[len(self.coos) - 1]
        for coo in range(self.dim):
            for i in range(len(self.coos) - 1):
                if compmax[coo] < self.coos[i][coo]:
                    compmax[coo] = self.coos[i][coo]
        return compmax

    def __hash__(self):
        hashstr = ""
        #TODO sort?
        for i in range(len(self.coos)):
            for coo in range(self.dim):
                hashstr += str(self.coos[i][coo])
        return int(hashstr)

    def __eq__(self, other):
        if self.dim != other.dim or self.name != other.name or len(self.coos) != len(other.coos):
            return False
        #return hash(self) == hash(other)
        for i in range(len(self.coos)):
            j = 0
            i_eq_j = False
            while (not i_eq_j) and j < len(self.coos):
                i_eq_j = True
                for coo in range(self.dim):
                    if self.coos[i][coo] != other.coos[j][coo]:
                        i_eq_j = False
                        break
                j = j + 1

            if i_eq_j == False:
                return False
        return True

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

def fixed_pentominos_of(p):
    reps = TileSet()
    for i in range(4):
        reps.add(p)
        p.flip(0)
        reps.add(p)
        p.flip(1)
        reps.add(p)
        p.flip(0)
        reps.add(p)
        p.flip(1)

        p.turn90()
    return reps

def all_fixed_pentominos():
    reps = TileSet()
    for p in all_pentominos():
        for fixp in fixed_pentominos_of(p):
            reps.add(fixp)
    return reps

class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        self.set.add( copy.deepcopy(p) )

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



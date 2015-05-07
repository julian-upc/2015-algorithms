import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        minn = 100000
        for i in self.coos:
            if i[coo] < minn:
                minn = i[coo]
        return self.translate_coo(coo, -minn)

    def normalize(self):
        return self.normalize_coo(0).normalize_coo(1)

    def flip(self, coo):
        minn = 100
        maxx = -100
        for i in self.coos:
            if maxx < i[coo]:
                maxx = i[coo]
            if minn > i[coo]:
                minn = i[coo]
        if maxx - minn == 1:
            for i in range(5):
                if self.coos[i][coo] == minn:
                    self.coos[i][coo] = maxx
                elif self.coos[i][coo] == maxx:
                    self.coos[i][coo] = minn
        elif maxx - minn == 2:
            for i in range(5):
                if self.coos[i][coo] == minn:
                    self.coos[i][coo] = maxx
                elif self.coos[i][coo] == maxx:
                    self.coos[i][coo] = minn
        elif maxx - minn == 3:
            for i in range(5):
                if self.coos[i][coo] == minn:
                    self.coos[i][coo] = maxx
                elif self.coos[i][coo] == maxx:
                    self.coos[i][coo] = minn
                elif self.coos[i][coo] == minn +1:
                    self.coos[i][coo] = maxx -1
                else:
                    self.coos[i][coo] = minn + 1 
        return self
                    
        
    def translate_one(self, coo):
        for i in self.coos:
            i[coo] += 1
        return self

    def translate_coo(self, coo, amount):
        for i in self.coos:
            i[coo] += amount
        return self

    def translate_by(self, by_vector):
        for i in self.coos:
            i[0] += by_vector[0]
            i[1] += by_vector[1]
        return self

    def turn90(self):
        a = 0
        for i in self.coos:
            a = i[0]
            i[0] = i[1]
            i[1] = a
        self.flip(1)
        return self

    def max(self):
        a = 0
        maxx = 0
        counter = 0
        for i in self.coos:
            counter = counter +1
            if i[0] + i[1] > maxx:
                maxx = i[0] + i[1]
                a = counter
        return self.coos[a-1]

    def __hash__(self):
        n = 10000000000
        k = 1
        for i in range(5):
            for j in range(2):
                n += self.coos[i][j]*k
                k*= 10
        return n

    def __eq__(self, other):
        self.normalize()
        other.normalize()
        self.coos.sort()
        other.coos.sort()
        return self.__hash__() == other.__hash__()

    def representation(self):
        return "[" + self.name + ":" + str(self.coos) + "]"


    def legal(self):
        for c in self.coos:
            if c[0]<0: 
                return False
            if c[1]<0: 
                return False
            if c[0]>7: 
                return False
            if c[1]>7: 
                return False
        for p in [[3,3],[3,4],[4,3],[4,4]]:
            if p in self.coos:
                return False
         
        return True        
                

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

def fixed_pentominos_of(orig_p):
    p = copy.deepcopy(orig_p)
    pentoList = TileSet()
    p.normalize()
    pentoList.add(p)
    for i in range(3):
        p.turn90()
        if not p in pentoList:
            pentoList.add(p.normalize())
    p.turn90()
    p.flip(1)
    if not p in pentoList:
            pentoList.add(p.normalize())
    for i in range(3):
        p.turn90()
        if not p in pentoList:
            pentoList.add(p.normalize())
    #print(p.name + " " + str(len(pentoList.set)))
    return pentoList

def all_fixed_pentominos():
    pentoList = TileSet()
    for i in all_pentominos():
        for j in fixed_pentominos_of(i):
            pentoList.add(j)
    return pentoList
    
class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        if p not in self.set:
            self.set.add(copy.deepcopy(p))

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
    
    
    


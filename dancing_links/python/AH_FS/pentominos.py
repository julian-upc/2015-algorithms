import copy
from array import *
import numpy as np

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        a = np.array(self.coos)
        minimum = np.amin(a[coo])
        a[:,coo] -= minimum
        self.coos = a.tolist()
         

    def normalize(self):
        for i in range(self.dim):
            normalize_coo(self,i)

    def flip(self, coo):
        a = np.array(self.coos)
        minimum = np.amin(a[coo])
        a[:,coo] -= (a[:,coo]- minimum) * 2
        self.coos = a.tolist()
        nomalize(self)
        
    def translate_one(self, coo):
        a = np.array(self.coos)
        a[:,coo] += 1
        self.coos = a.tolist()

    def translate_coo(self, coo, amount):
        a = np.array(self.coos)
        a[:,coo] += amount
        self.coos = a.tolist()

    def translate_by(self, by_vector):
        a = np.array(self.coos)
        a += by_vector
        self.coos = a.tolist()

    def turn90(self):
        pass

    def max(self):
        pass

    def __hash__(self):
        pass

    def __eq__(self, other):
        pass

    def representation(self):
        return "[" + self.name + ":" + str(self.coos) + "]"
    


c = [[-4,1],[1,0],[1,1],[1,2],[2,2]]
a = np.array(c)
minimum = np.amin(a[0])
print minimum
a[:,1] -= minimum
print a.tolist()


c = [[-12,1],[-11,0],[-11,1],[-11,2],[-10,2]]
a = np.array(c)
#minimum = np.amin(a[0])
#a[:,0] -= (a[:,0]- minimum) * 2
a += [1,1]
print a.tolist()         

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


class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        pass

    def size(self):
        pass

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



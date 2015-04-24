import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        return self
        
    
    # the function "find_min_coo(self, coo) finds the minimal coos of one given coo
    def find_min_coo(self, coo):
        min = self.coos(coo)
        for c in self.coos:
            if c(coo)<min:
                min=c(coo)
            return self
                
    # the function "normalize_coo(self, coo)" moves the pentomino straight to the coo-axis, till its touching the coo-axis
    def normalize_coo(self, coo):
        dist_to_axis = find_min_coo(self, coo)
        translate_coo(self, coo, dist_to_axis)
        return self

    # the function "normalize(self)" founds the representive pentomino of its equivalent class
    # it is the one nearest the origin with only positiv coordinates, using only translating  (no rotations)     
    def normalize(self):
        for c in self.coos:
            normalize_coo(self, c)
        return self

    # the function flip mirrors the pentomino on the given coordinate/axis
    # hence for coo=0 it flips over the x-axis, for coo=1 over the y-axis
    def flip(self, coo):
        #lower left corner of the boundingbox of pentomino
        lower_coos = [self.find_min_coo(c) for c in self.coos]
        #normalize
        self.normalize()
        #flip
        for c in self.coos:
            a = -c[coo]
            c[coo] = a  
        #denormalize back into the boundingbox
        self.normalize()
        self.translate_by(lowercoos)
        return self
        
    def translate_one(self, coo):
        for co in self.coos:
            co[coo] += 1
        return self

    def translate_coo(self, coo, amount):
        for co in self.coos:
            co[coo] += amount
        return self

    def translate_by(self, by_vector):
        pass

    #the function turn90 
    def turn90(self):
        pass

    #the function max returns the maximum coordinate in each axis
    def max(self):
        upper_coos = [0]*self.dim
        for i in range(self.dim):
            for c in self.coos:
                if c[i] > upper_coos[i]:
                    upper_coos[i] = c[i]               
        return upper_coos

    def __hash__(self):
        pass

    def __eq__(self, other):
        pass

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
"""
# this function creates a TileSet of all normalized representatives of the given pentomino p
def fixed_pentominos_of(p):
pass

def all_fixed_pentominos():
    all_pSet = Tileset(all_pentominos())
    #all_p = all_pentominos()
    while(all_pSet.__iter__()!=
        all_pSet.add(self,fixed_pentominos_of(p))
"""
def all_pentominos():
    return [F(), I(), L(), P(), N(), T(), U(), V(), W(), X(), Y(), Z()]

class TileSet(object):
    
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)

    # this function adds a pentomino to this TileSet    
    def add(self, p):
        present = 0
        for q in self.set:
            if p==q:
                present = 1
        if present == 0:
            self.set.add(copy.deepcopy(p))
        
    # this function adds a TileSet to this TileSet
    def add_TileSet(self, tileSet):
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



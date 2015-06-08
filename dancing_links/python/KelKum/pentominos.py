import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        m = min([c[coo] for c in self.coos])
        return self.translate_coo(coo, -m)

    def normalize(self):
        self = self.normalize_coo(0)
        self = self.normalize_coo(1)
        self.coos.sort()
        return self

    def flip(self, coo):
        for c in self.coos:
            c[coo] = -c[coo]
        return self.normalize_coo(coo)
        
    def translate_one(self, coo):
        return self.translate_coo(coo, 1)
    
    def translate_coo(self, coo, amount):
        x, y = 0, 0
        if coo == 0:
            x = amount
        elif coo == 1:
            y = amount
        for c in self.coos:
            c[0] += x
            c[1] += y
        return self

    def translate_by(self, by_vector):
        #print("Translate " + str(self.coos) + " by " + str(by_vector))
        self = self.translate_coo(0, by_vector[0])
        self = self.translate_coo(1, by_vector[1])
        return self

    def turn90(self):
        self.coos = [[-c[1], c[0]] for c in self.coos]
        return self.normalize()

    def max(self):
        return max(self.coos)

    def __hash__(self):
        self.coos.sort()
        h = str()
        for c in self.coos:
            h += str(c[0] + 1) + str(c[1] + 1) 
        return int(h)

    def __eq__(self, other):
        for c in self.coos:
            if c not in other.coos:
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
    t = TileSet()
    t.add(p)
    t.add(p.flip(0))
    t.add(p.flip(1))
    t.add(p.flip(0))
    t.add(p.flip(1).turn90())
    t.add(p.flip(0))
    t.add(p.flip(1))
    t.add(p.flip(0))
    return t

def fixed_pentominos_of_name_list(list):
	is_list_of_pentominos(list)
	t = TileSet()
	for name in list:
		p = pentomino_by_name(name)
		t.addlist(fixed_pentominos_of(p))
	return t
	
def is_list_of_pentominos(list):
	all = ["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"]
	for p in list:
		if p not in all:
			raise ValueError("Error in pentomino list: " + str(p) + " is not a pentomino")

def pentomino_by_name(name):
	pentominos = all_pentominos()
	for p in pentominos:
		if p.name == name:
			return p
    
def all_fixed_pentominos():
    plist = all_pentominos()
    t = TileSet()
    for p in plist:
        t.addlist(fixed_pentominos_of(p))
    return t

class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        self.addlist(plist)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        q = copy.deepcopy(p)
        #print(p.representation() + ' ' + str(p.__hash__()))
        #print(q.representation() + ' ' + str(q.__hash__()))
        self.set.add(q)
        
    def addlist(self, plist):
        for p in plist:
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



import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        if coo == 0:
	    self.translate_by([-min([c[0] for c in self.coos]),0])
	else:
	    self.translate_by([0,-min([c[1] for c in self.coos])])


    def normalize(self):
	self.translate_by([-min([c[0] for c in self.coos]),-min([c[1] for c in self.coos])])
	return self

    def flip(self, coo):
        if coo == 0:
	    self.coos = [[c[0],-c[1]] for c in self.coos]
	else:
	    self.coos = [[-c[0],c[1]] for c in self.coos]
	self.normalize()
	return self
        
    def translate_one(self, coo):
	if coo == 0:	
            self.coos = [[c[0]+1,c[1]] for c in self.coos]    
	else:
            self.coos = [[c[0],c[1]+1] for c in self.coos]    
	return self

    def translate_coo(self, coo, amount):
        if coo == 0:	
            self.coos = [[c[0]+amount,c[1]] for c in self.coos]    
	else:
            self.coos = [[c[0],c[1]+amount] for c in self.coos]
	return self
  
    def translate_by(self, by_vector):
        self.coos = [[c[0]+by_vector[0],c[1]+by_vector[1]] for c in self.coos]
	return self

    def turn90(self):
        self.coos = [[-c[1],c[0]] for c in self.coos] 
        self.normalize()
        return self

    def max(self):
	return [max([c[0] for c in self.coos]), max([c[1] for c in self.coos])]
        

    def __hash__(self):
        self.coos = sorted(self.coos)
        return hash(str(self.coos))

    def __eq__(self, other):
	self.normalize()
	other.normalize()
        return self.__hash__() == other.__hash__()

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
    fp = TileSet()
    for i in range(4):
	p.turn90()
	fp.add(p)
	p.flip(0)
	fp.add(p)
	p.flip(0)
    return fp
    
def all_fixed_pentominos():
    plist = []
    for p in all_pentominos():
	plist += fixed_pentominos_of(p)
    return TileSet(plist)
  
class TileSet(object):
    def __init__(self, plist=[], stock=None):
        self.set = set()
        for p in plist:
	    self.add(p)
        if stock == None:
	    self.stock = dict.fromkeys([p.name for p in plist],1)
	else:
	    self.stock = stock
	    self.stock.update(dict.fromkeys([p.name for p in plist if p.name not in self.stock],0))
	  
    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        self.set.add(copy.deepcopy(p))	#not desirable
        return self

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



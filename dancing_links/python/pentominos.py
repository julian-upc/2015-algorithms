import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos #coordinates
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        pass

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
            pass

    def flip(self, coo):
        #0 : x-axis
        #1 : y-axis
        pass
        if self.name == "F":
            self.coos = [[0,1],[1,0],[1,1],[1,2],[2,2]]
        elif self.name == "I":
            
        elif self.name == "L":
            first_field = self.coos[0]
            next_horizontal = [first_field[0]+2,first_field[1]]
            next_vertical = [first_field[0],first_field[1]+2]
            
            if (next_horizontal in self.coos && coo == 1): #L lies horizontally and we flip 
            
            elif
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
            pass
        
    def translate_one(self, coo):
        #0: move one on x-axis
        #1: move one on y-axis
        for c in self.coos:
            c[coo] = c[coo]+1

    def translate_coo(self, coo, amount):
        for c in self.coos:
            c[coo] = c[coo]+ amount

    def translate_by(self, by_vector):
        x_shift = by_vector[0]
        y_shift = by_vector[1]
        for c in self.coos:
            c[0] = c[0]+ x_shift
            c[1] = c[1]+ y_shift

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
        if p not in self.set:
            self.set.append(p)
        else:
            pass

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



import copy

max_coord = 999

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        return self
    
    def normalize_coo(self, coo):
        """ moves the given self straight to the given coo-axis.
            returns an axis touching self, with only positiv coo-coordinates
            coo: given axis
        """
        dist_to_axes = self.min()
        self.translate_coo(coo, (-1)*self.min()[coo])
        return self
    
    def normalize(self):
        """ normalize the given self. 
            returns an all axes touching self, with only positiv coordinates,
            with lexicographical orderd coordinates
        """
        self.coos.sort()
        for i in range(self.dim):
            self.normalize_coo(i)
        return self
    
    def translate_one(self, coo):
        """ translates the given self by one along the given coo-axis
            coo: gives the axis
        """
        for co in self.coos:
            co[coo] += 1
        return self

    def translate_coo(self, coo, amount):
        """ translates the given self by amount along the given coo-axis
            coo: axis to translate along
            amount: translaing distance
        """
        for co in self.coos:
            co[coo] += amount
        return self

    def translate_by(self, by_vector):
        """ translates the given self by an given vector
            by_vector: vactor to translate the self with
        """
        if len(by_vector) != self.dim:
            print("dimension missmatch")
        else:
            for i in range(len(by_vector)):
                self.translate_coo(i, by_vector[i])
            return self

    def flip(self, coo):
        """ mirrors the given self over the given coo-axis
            coo: given axis
            hence for coo=0 it flips over the x-axis, for coo=1 over the y-axis   
        """
        # remember the place of it self and normalize
        lower_coos = self.min()
        self.normalize()
        # flip it over the coo-axis
        for c in self.coos:
            a = -c[coo]
            c[coo] = a
        # bring it back to where it was before
        self.normalize()
        self.translate_by(lower_coos)
        return self
    
    def turn90(self):
        """ turns the given self clockwise around 90 degree.
            the lower-bounding box stays where it was
        """
        if self.dim == 2:
            # remember the place of it and normalize it
            re_place = self.min()
            self.normalize()
            # flip it along the identity line
            for c in self.coos:
                temp = c[0]
                c[0] = c[1]
                c[1] = temp
            # flip it along the x-axis to turn clockwise
            self.flip(0)
            # replace it, to where it was before
            self.normalize()
            self.translate_by(re_place)
            return self
        else:
            print("turn90 is only defined in dimension 2")  

    def min(self):
        """ finds the minimum coordinate in each axis,
            these are representated as a "lower-bounding-box"
            these lower-bounding-box is initialized with the maximal coordinates max_coord
        """
        lower_coos = [max_coord]*self.dim
        for i in range(self.dim):
            for c in self.coos:
                if c[i] < lower_coos[i]:
                    lower_coos[i] = c[i]
        return lower_coos
    
    def max(self):
        """ finds the maximum coordinate in each axis,
            these are representated as an "upper-bounding-box"
            these lupper-bounding-box is initialized with the maximal coordinates max_coord
        """
        upper_coos = [(-1)*max_coord]*self.dim
        for i in range(self.dim):
            for c in self.coos:
                if c[i] > upper_coos[i]:
                    upper_coos[i] = c[i]               
        return upper_coos

    def __hash__(self):
        """ gives back an integer which represents the given pentomino in an unique way.
            our hash has the form "dim | coordinate of normalized pentomino | translate vector".
            translate vector is bounded by [0:999,0:999].
            example:  the pentomino: [[12,4],[13,3],[13,4],[13,5],[14,5]]
                      is F = [[0,1],[1,0],[1,1],[1,2],[2,2]] translated by [12,3]
                      hash is: 2|0110111222|012003 (without "|" of course)
        """
        #save the origin position of self and normalize it
        lower_coos = self.min()
        self.normalize()
        # sort the coordinates in lexikografic order
        self.coos.sort()
        #construct the hash code in the describted way
        hash = self.dim
        for c in self.coos:
            for i in range(self.dim):
                hash = hash*10 + c[i]
        for i in range(self.dim):
            hash = 1000*hash + lower_coos[i]
        # bring self back to where it was before
        self.translate_by(lower_coos)
        return hash

    def __eq__(self, other):
        """ checks the equality of the data from "self" and "other"
        """
        return self.__hash__() == other.__hash__()

    def representation(self):
        """ Gives back a string representation of the given self
        """
        return "[" + self.name + ":" + str(self.coos) + "]"

""" The following classes implements all kinds of pentominos in normalized coordinates
"""
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

def fixed_pentominos_of(p):
    """ adds all possible representations of the given pentomino (turned and flipped) to self
    """
    allReps = TileSet()
    for i in range(4):
        allReps.add(p.turn90())
    allReps.add(p.flip(0))
    for i in range(3):
        allReps.add(p.turn90())
    return allReps

def all_fixed_pentominos():
    """ gives back all possible representations of all possible pentominos 
    """
    all_pSet = TileSet()
    pento_list = all_pentominos()
    for p in pento_list:
        all_pSet.add_TileSet(fixed_pentominos_of(p))
    return all_pSet

def all_pentominos():
    """ gives back all possible pentominos
    """
    return [F(), I(), L(), P(), N(), T(), U(), V(), W(), X(), Y(), Z()]

""" 
"""
class TileSet(object):
    
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
 
    def add(self, p):
    """ adds the given pentomino to self
    """
        if p not in self.set:
            self.set.add(copy.deepcopy(p))
    
    def add_TileSet(self, tileSet):
    """ adds the given tileSet to self
    """
        for p in tileSet:
            if p not in self.set:
                self.add(p)
        return self
                     
    def size(self):
        return len(self.set)
                     
    def representation(self):
    """ gives back a representation for tileSet
    """
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



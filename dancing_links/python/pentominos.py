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
            #c = [c[1],-c[0]]
        pos = self.min_box()
        #normalise back into positive space
        if pos[0]<0:
            self.translate_coo(0,-pos[0])
        if pos[1]<0:
            self.translate_coo(1,-pos[1])
        self.translate_by(ref_point) #move back to former position
        return self
        #turns the pentomino by 90 degrees clockwise around its first coordinate
        # turning_point = self.coos[0]
        # for c in self.coos:
        #     offset = [c[0]-turning_point[0],c[1]-turning_point[1]] #vector from turning point to currently considered field
        #     offset_new = [offset[1],-offset[0]] #new offset vector, flip is and negate second component
        #     c[0] = turning_point[0]+offset_new[0]
        #     c[1] = turning_point[1]+offset_new[1]
        # return self

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

    def __hash__old(self):
        ref_point = self.coos[0]
        if self.name == "F":
            return self.hashF(ref_point)
        elif self.name == "I":
            if [ref_point[0],ref_point[1]+1] in self.coos or [ref_point[0],ref_point[1]-1] in self.coos: #field over or under ref is taken -> vertical I
                return 21
            else: #horizontal I
                return 22
        elif self.name == "L":
            return self.hashL(ref_point)
        elif self.name == "P":
            return self.hashP(ref_point)
        elif self.name == "N":
            return self.hashN(ref_point)
        elif self.name == "T":
            return self.hashT(ref_point)
        elif self.name == "U":
            return self.hashU(ref_point)
        elif self.name == "V":
            return self.hashV(ref_point)
        elif self.name == "W":
            return self.hashW(ref_point)
        elif self.name == "X":
            return 9
        elif self.name == "Y":
            return self.hashY(ref_point)
        elif self.name == "Z":
            return self.hashZ(ref_point)
        else:
            #error
            print "This is not a pentomino, I cannot hash it."
        return self

    def hashF(self,ref_point):
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref taken
            if [ref_point[0]+1,ref_point[1]+2] in self.coos:
                return 18
            else:
                return 17
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref is taken
            if [ref_point[0]+1,ref_point[1]-2] in self.coos:
                return 16
            else:
                return 15
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref is taken
            if [ref_point[0]+2,ref_point[1]+1] in self.coos:
                return 11
            else:
                return 13
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref is taken
            if [ref_point[0]-2,ref_point[1]+1] in self.coos:
                return 12
            else:
                return 14
        print "unreachable code reached"
        #error if code reaches here

    def hashL(self,ref_point):
        if [ref_point[0],ref_point[1]+2] in self.coos: #field two above ref is taken -> long end to top
            if [ref_point[0]+1,ref_point[1]] in self.coos: #right to ref is taken -> normal L
                return 31
            else:
                return 32
        if [ref_point[0],ref_point[1]-2] in self.coos: #field two below ref is taken -> long end to bottom
            if [ref_point[0]+1,ref_point[1]] in self.coos: #right to ref is taken
                return 33
            else:
                return 34
        if [ref_point[0]+2,ref_point[1]] in self.coos: #field two to the right of ref is taken -> L lying to the right
            if [ref_point[0],ref_point[1]+1] in self.coos: #short end looks up
                return 37
            else:
                return 38
        if [ref_point[0]-2,ref_point[1]] in self.coos: #field two to the left of ref is taken -> L lying to the left
            if [ref_point[0],ref_point[1]+1] in self.coos: #short end look up
                return 35
            else:
                return 36
        #error if code reaches here
        print "unreachable code reached"

    def hashP(self,ref_point):
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref is taken
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 41
            else:
                return 42
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref is taken
            if [ref_point[0]+1,ref_point[1]-1] in self.coos:
                return 43
            else:
                return 44
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref is taken
            if [ref_point[0]-1,ref_point[1]+1] in self.coos:
                return 45
            else:
                return 46
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref is taken
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 47
            else:
                return 48

    def hashT(self,ref_point):
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right to ref is taken
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 52
            else:
                return 51
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left to ref is taken
            if [ref_point[0]-1,ref_point[1]-1] in self.coos:
                return 51
            else:
                return 52
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref is taken
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 53
            else:
                return 54
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref is taken
            if [ref_point[0]-1,ref_point[1]-1] in self.coos:
                return 54
            else:
                return 53
        #error if code is reached
        print "unreachable code reached"

    def hashU(self,ref_point):
        if [ref_point[0]+2,ref_point[1]] in self.coos: #field two right from ref is taken
            if [ref_point[0],ref_point[1]+1] in self.coos:
                return 61
            else:
                return 62
        if [ref_point[0]-2,ref_point[1]] in self.coos: #field two left from ref is taken
            if [ref_point[0],ref_point[1]+1] in self.coos:
                return 61
            else:
                return 62
        if [ref_point[0],ref_point[1]+2] in self.coos: #field two above ref is taken
            if [ref_point[0]+1,ref_point[1]] in self.coos:
                return 63
            else:
                return 64
        if [ref_point[0],ref_point[1]-2] in self.coos: #field two below ref is taken
            if [ref_point[0]+1,ref_point[1]] in self.coos:
                return 63
            else:
                return 64
        #error if code is reached
        print "unreachable code reached"

    def hashV(self,ref_point):
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref
            if [ref_point[0]+2,ref_point[1]+1] in self.coos: #V goes up
                return 71
            else:
                return 74
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref
            if [ref_point[0]-2,ref_point[1]+1] in self.coos: #V goes up
                return 72
            else:
                return 73
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref
            if [ref_point[0]+1,ref_point[1]+2] in self.coos: #V goes right
                return 73
            else:
                return 74
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref
            if [ref_point[0]+1,ref_point[1]-2] in self.coos: #V goes right
                return 72
            else:
                return 71
        #error if code is reached
        print "unreachable code reached"

    def hashW(self,ref_point):
        if [ref_point[0],ref_point[1]+1] in self.coos: #taken field over ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 83
            else:
                return 84
        if [ref_point[0],ref_point[1]-1] in self.coos: #taken field under ref
            if [ref_point[0]+1,ref_point[1]-1] in self.coos:
                return 82
            else:
                return 81
        if [ref_point[0]+1,ref_point[1]] in self.coos: #taken field right of ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 81
            else:
                return 84
        if [ref_point[0]-1,ref_point[1]] in self.coos: #taken field left of ref
            if [ref_point[0]-1,ref_point[1]-1] in self.coos:
                return 83
            else:
                return 82
        #error if code is reached
        print "unreachable code reached"

    def hashZ(self,ref_point):
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos: #Z goes up
                return 112
            else:
                return 111
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref
            if [ref_point[0]-1,ref_point[1]+1] in self.coos: #Z goes up
                return 111
            else:
                return 112
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos: #Z goes right
                return 113
            else:
                return 114
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref
            if [ref_point[0]+1,ref_point[1]-1] in self.coos: #Z goes right
                return 113
            else:
                return 114

    def hashY(self,ref_point):
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref
            if [ref_point[0]+2,ref_point[1]+1] in self.coos: #Y goes up
                return 101
            else:
                return 102
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref
            if [ref_point[0]-2,ref_point[1]+1] in self.coos: #Y goes up
                return 103
            else:
                return 104
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref
            if [ref_point[0]+1,ref_point[1]+2] in self.coos: #Y goes right
                return 106
            else:
                return 105
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref
            if [ref_point[0]+1,ref_point[1]-2] in self.coos: #Y goes right
                return 108
            else:
                return 107

    def hashN(self,ref_point):
        if [ref_point[0]+1,ref_point[1]] in self.coos: #field right of ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 128
            else:
                return 126
        if [ref_point[0]-1,ref_point[1]] in self.coos: #field left of ref
            if [ref_point[0]-1,ref_point[1]-1] in self.coos:
                return 125
            else:
                return 127
        if [ref_point[0],ref_point[1]+1] in self.coos: #field over ref
            if [ref_point[0]+1,ref_point[1]+1] in self.coos:
                return 121
            else:
                return 122
        if [ref_point[0],ref_point[1]-1] in self.coos: #field under ref
            if [ref_point[0]-1,ref_point[1]-1] in self.coos:
                return 123
            else:
                return 124

    #two different pentominos are equal iff they have same name and orientation
    def __eq__(self, other):
        return self.__hash__()==other.__hash__()
        # equal = 1
        # if self.name != other.name:
        #     equal = 0
        # diff_coo_x = self.coos[0][0]-other.coos[0][0]
        # diff_coo_y = self.coos[0][1]-other.coos[0][1]
        # for i in [0,len(self.coos)-1]:
        #     c = self.coos[i]
        #     o = self.coos[i]
        #     if c[0]-o[0] != diff_coo_x:
        #         equal = 0
        #     if c[1]-o[1] != diff_coo_y:
        #         equal = 0
        # return equal == 1

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

def fixed_pentominos_of(p):
    pent = TileSet()
    f= F()
    pent.add(f)
    pent.add(f.turn90())
    pent.add(f.turn90())
    pent.add(f.turn90())
    f.turn90()
    pent.add(f.flip(0))
    pent.add(f.turn90())
    pent.add(f.turn90())
    pent.add(f.turn90())
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
            if p.__eq__(q):
                present = 1
        if present == 0:
            self.set.add(p)
        # if p.__hash__() not in self.set:
        #     self.set.add(p.__hash__())
        # else:
        #     pass

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



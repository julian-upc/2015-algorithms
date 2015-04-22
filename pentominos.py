import copy

#nontested
class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])

    #the comments are the version i would prefer, without input coo
    def normalize_coo(self, coo):
        if ~self.consistent():
            print "polyomino non consistent"
        if coo >=self.dim | coo<0:
            print "Invalid argument for coo"
        selbst = copy.deepcopy(self)
        for c in selbst.coos:
            #for i in range(self.dim):
            #    c[i]*=-1
            c[coo]*=-1

        self.translate_coo(coo,max(selbst)[coo])
        #self.translate_by(max(selbst))
        
    def normalize(self):
        if ~self.consistent():
            print "polyomino non consistent"
        self=nameInit[self.name]

    def flip(self, coo):
        if ~self.consistent():
            print "polyomino non consistent"
        if coo >=self.dim | coo<0:
            print "Invalid argument for coo"
        else:
            for c in self.coos:
                c[coo]*=-1

    
    def translate_one(self, coo):
        translate_coo(self,coo,1)
            
    #this method translates all coordinates in direction no. coo (starting with 0) by amount
    #(negative amount yields the opposite direction)
    def translate_coo(self, coo, amount):
        if ~self.consistent():
            print "polyomino non consistent"
        if coo >=self.dim | coo<0:
            print "Invalid argument for coo"
        else:
            for c in self.coos:
                c[coo]+=amount

    #this method translates all coordinates of the pentomino by the vector by_vector
    def translate_by(self, by_vector):
        if ~self.consistent():
            print "polyomino non consistent"
        if len(by_vector)!=self.dim:
            print "Invalid argument for by_vector"
        else:
            for c in self.coos:
                for i in range(len(c)):
                    c[i]+=by_vector[i]                    
                #c= map(int.__add__,c,by_vector)
        
    #Turn 90 degrees around midpoint: coos[2] for pentominos, coos[3] for hexominos, etc.
    def turn90(self):
        if ~self.consistent():
            print "polyomino non consistent"
        if self.dim!=2:
            print "rotation only possible in 2D"
        else:
            vec=copy.deepcopy(self.coos[len(self.coos)//2])
            for i in range(self.dim):
                vec[i]=-vec[i]
            translate_by(vec)
            for c in self.coos:
                tmp = c[0]
                c[0]= -c[1]
                c[1]= tmp
            translate_by(self.coos[len(self.coos)//2])

    def max(self):
        if ~self.consistent():
            print "polyomino non consistent"
        maxi = [0] * self.dim
        for c in self.coos:
            for i in range(self.dim):
                maxi[i] = max(c[i],maxi[i])
        return maxi
        
    # The hashfunction asserts that dimension is less or equal than 16, whilst strictly bigger than 0
    # It furtherly asserts that the coordinates are not greater than 255, and nonnegative.
    def __hash__(self):
        if ~self.consistent():
            return -1
        hashcode = 0
        hashcode += hashName(self.name)
        hashcode += (self.dim-1)<<4
        e=8
        for c in self.coos:
            for i in range(self.dim):
                hashcode += c[i]<<e
                e+=8
        return hashcode

    #this method returns true iff two pentominos (self, other) of the same kind lie in the same place
    def __eq__(self, other):
        if ~self.consistent():
            print "polyomino non consistent"
        elif ~other.consistent():
            print "polyomino non consistent"
        elif self.name!=other.name:
            return False
        elif self.dim!=other.dim:
            return False
        # self.coos == other.coos would compare pointers, not entries,
        # so we choose the difficult version
        elif len(self.coos)!=len(other.coos):
            return False
        else:
            for i in range(len(self.coos)):
                if self.dim!=len(other.coos[i]):
                    return False
                elif len(self.coos[i])!=self.dim:
                    return False
                else:
                    for j in range(self.dim):
                        if self.coos[i][j]!=other.coos[i][j]:
                            return False
            return True

    def representation(self):
        if ~self.consistent():
            print "polyomino non consistent"
        return "[" + self.name + ":" + str(self.coos) + "]"

    def consistent(self):
        try:
            selbst = copy.deepcopy(self)
            selbstnorm=nameInit(self.name)
            if len(self.coos)!=5:
                return False
            else:
                for c in self.coos:
                    if len(c) != self.dim:
			return False
                for i in range(1,5):
                    selbst.coos[i][0]=selbst.coos[i][0]-selbst.coos[0][0]
                    selbst.coos[i][1]=selbst.coos[i][1]-selbst.coos[0][1]
                selbst.coos[0][0]=0
                selbst.coos[0][1]=0

                #normalize selbst "by hand"
                if coo2X(self.name):
                    i=0
                    while selbst.coos[1][0]!=1:
                        i+=1
                        if i>4 :
                            return False
                        for c in selbst.coos:
                            tmp = c[0]
                            c[0]= -c[1]
                            c[1]= tmp
                    for j in range(self.dim):
                        selbst.coos[0][j]+=switchy(self.name)
                else:
                    while selbst.coos[1][1]!=1:
                        i+=1
                        if i>4 :
                            return False
                        for c in selbst.coos:
                            tmp = c[0]
                            c[0]= -c[1]
                            c[1]= tmp
                #selbst should now be the same as selbstnorm. We check that:
                if selbst.name!=selbstnorm.name:
                    return False
                elif selbst.dim!=selbstnorm.dim:
                    return False
                # selbst.coos == selbstnorm.coos would compare pointers, not entries,
                # so we choose the difficult version
                elif len(selbst.coos)!=len(selbstnorm.coos):
                    return False
                else:
                    for i in range(len(selbst.coos)):
                        if selbst.dim!=len(selbstnorm.coos[i]):
                            return False
                        else:
                            for j in range(selbst.dim):
                                if selbst.coos[i][j]!=selbstnorm.coos[i][j]:
                            return False
                    return True
        except:
            return False

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

nameInit= {
    "F":F
    "I":I
    "L":L
    "P":P
    "N":N
    "T":T
    "U":U
    "V":V
    "W":W
    "X":X
    "Y":Y
    "Z":Z
}

hashName = {
    "F":0
    "I":1
    "L":2
    "P":3
    "N":4
    "T":5
    "U":6
    "V":7
    "W":8
    "X":9
    "Y":10
    "Z":11
}

switchy = {
    "F":1
    "T":2
    "V":0
    "W":0
    "X":1
    "Y":0
    "Z":2
}

coo2X = {
    "F":True
    "I":False
    "L":False
    "P":False
    "N":False
    "T":True
    "U":False
    "V":True
    "W":True
    "X":True
    "Y":True
    "Z":True
}


class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        tmp = copy.deepcopy(p)
        vec = tmp.max()
        for i in range(tmp.dim):
            vec[i]=-vec[i]
        tmp.translate_by(vec)
        for i in range(tmp.dim):
            tmp.normalize_coo(i)
        append = True
        for pp in self.set:
            if pp.__eq__(tmp):
                append = False
        if append:
            self.set.append(tmp)

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

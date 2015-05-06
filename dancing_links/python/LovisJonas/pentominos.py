import copy

class Pentomino(object):
    def __init__(self, name, coos):
        self.name = name
        self.coos = coos
        self.dim = len(coos[0])
        
    def normalize_coo(self, coo):
        a=self.coos[0][coo]        
        for i in self.coos :
            if a > self.coos[i][coo] :
                a = self.coos[i][coo]             
        for i in self.coos :
            self.coos[i][coo] = self.coos[i][coo] - [a]

    def normalize(self):
        self.coos.sort()
        a=self.coos[0][0]
        b=self.coos[0][1]        
        for i in self.coos :
            if a > i[0] :
                a = i[0]
            if b > i[1] :
                b = i[1]
        for i in range(5) :
            self.coos[i][0] = self.coos[i][0] - a
            self.coos[i][1] = self.coos[i][1] - b 
        return self
                
    def flip(self, coo):
        right = -100
        left = 100
        for i in self.coos :
            if right < i[coo] :
                right = i[coo]
            if left > i[coo] :
                left = i[coo]
            
        if right-left == 1 :
            for i in range(5) :
                if self.coos[i][coo] == left :
                    self.coos[i][coo] = right
                else :
                    self.coos[i][coo] = left
        elif right-left == 2 :
                for i in range(5) :
                    if self.coos[i][coo] == left :
                        self.coos[i][coo] = right
                    elif self.coos[i][coo] == right :
                        self.coos[i][coo] = left
        elif right-left == 3 :
            for i in range(5) :
                    if self.coos[i][coo] == left :
                        self.coos[i][coo] = right
                    elif self.coos[i][coo] == right :
                        self.coos[i][coo] = left
                    elif self.coos[i][coo] == right-1 :
                        self.coos[i][coo] = right-2
                    else :
                        self.coos[i][coo] = right-1
        return self
        
    def translate_one(self, coo):
        for i in range(5) :
            self.coos[i][coo] = self.coos[i][coo] + 1
        return self

    def translate_coo(self, coo, amount):
        for i in self.coos :
            self.coos[i][coo] = self.coos[i][coo] + amount 
        return self

    def translate_by(self, by_vector):
        for i in range(5) :
            self.coos[i][0] = self.coos[i][0] + by_vector[0] 
            self.coos[i][1] = self.coos[i][1] + by_vector[1]
        return self

    def turn90(self):
        for i in range(5) :
            coord = self.coos[i][1]
            self.coos[i][1]=self.coos[i][0]
            self.coos[i][0]=coord
        self.flip(1)
        return self

    def legal(self):
        for p in self.coos:
            if p[0]<0:
                return False
            if p[0]>7:
                return False
            if p[1]<0:
                return False
            if p[1]>7:
                return False
        for p in [[3,3],[3,4],[4,3],[4,4]]:
            if p in self.coos:
                return False
        return True

    def max(self):
        maxx=-1
        maxy=-1
        maximum=list()
        for i in self.coos:
            if maxx<i[0]:
                maxx=i[0]
        for i in self.coos:
            if maxx==i[0]:
                maximum.append(i)
        for i in maximum:
            if maxy<i[1]:
                maxy=i[1]
        return [maxx,maxy]

    def __hash__(self):
        c0 = self.normalize()
        h = 100**len(self.coos)
        x=0
        for i in range(5) :
            x = c0.coos[i][0]*100+c0.coos[i][1]
            h = h+x*100**(i*2)
            x=0
        return h
    
    def __eq__(self, other):
        if self.name != other.name :
            return False
        else :
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

def all_pentominos_names():
    list=[]
    for p in all_pentominos():
        list.append(p.name)
    return list

def all_positions():
    return ["00","01","02","03","04","05","06","07",
            "10","11","12","13","14","15","16","17",
            "20","21","22","23","24","25","26","27",
            "30","31","32",          "35","36","37",
            "40","41","42",          "45","46","47",
            "50","51","52","53","54","55","56","57",
            "60","61","62","63","64","65","66","67",
            "70","71","72","73","74","75","76","77",]

    
def all_fixed_pentominos():
    s = TileSet()
    for i in all_pentominos() :
        if i.name == "X" :
            s.add(i)
        elif  i.name == "I": 
            s.add(I())
            s.add(I().turn90())
        else :
            for k in range(4):
                s.add(i.normalize())
                s.add(i.flip(0).normalize())
                s.add(i.flip(1).normalize())
                s.add(i.flip(0).normalize())
                i.flip(1).normalize()
                i.turn90().normalize()
                k+=1
    return s

def fixed_pentominos_of(p):
    s = TileSet()
    for i in all_pentominos() :
        if p.name == i.name :
            for k in range(4):
                s.add(i.normalize())
                s.add(i.flip(0).normalize())
                s.add(i.flip(1).normalize())
                s.add(i.flip(0).normalize())
                i.flip(1).normalize()
                i.turn90().normalize()
                k+=1
    return s


    
class TileSet(object):
    def __init__(self, plist=[]):
        self.set = set()
        for p in plist:
            self.add(p)

    def __iter__(self):
        return iter(self.set)
        
    def add(self, p):
        c = copy.deepcopy(p)
        value = True
        for i in self.set :
            if i.__eq__(c) :
                value = False
        if value :
            self.set.add(c)
            
        
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
    
    
                
        

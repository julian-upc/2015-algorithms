import incidence_matrix
import pentominos
import copy

class Board(object):
    def __init__(self, size, capacities = None):
        self.size = size
        self.dim = len(size)
	fields = [[]]
	for i in range(len(size)):
	    oldFields = copy.deepcopy(fields)
	    newFields = []
	    for j in range(size[i]):
		newFields.extend([f + [j] for f in oldFields])
	    fields = newFields
	self.capacities = dict.fromkeys([str(f) for f in fields],1)
	if capacities != None:
	    for cap in capacities:
		self.capacities[cap] = capacities[cap]
        
    def valid_tile_placement(self, coos):
	for c in coos:
	    if str(c) not in self.capacities:
		return False
	    else: 
		if self.capacities[str(c)] == 0:
		    return False
	return True
    
    def representation(self):
	return str(self.size), ', ' , str(self.capacities)  

        
class Covering(object):
    def __init__(self, board, tileSet, fixedTiles=dict()):
	self.board = board
	self.tileSet = tileSet
	self.fixedTiles = fixedTiles
	
    def get_size(self, c):
        return c.size

    def n_solutions(self):
	#initialize the appropriate incidence matrix
	fields = [str(c[1])+str(c[4]) for c in self.board.capacities if self.board.capacities[c] > 0]
	I = incidence_matrix.IncidenceMatrix([t.name for t in self.tileSet.set] + fields + ['constraint'])	#name collisions for tiles which are more than once available
        for p in self.tileSet.set:
	    if p.name in self.fixedTiles:
		for c in [coos for coos in self.fixedTiles[p.name] if self.board.valid_tile_placement(coos)]:
		    I.appendRow(p.name,[str(coo[0])+str(coo[1]) for coo in c])
                    #if c == [[1,2],[2,2],[2,1],[2,3],[3,2]]:
                        #constraintCell = incidence_matrix.IncidenceCell(I.columnObjectOfName['X'].up.left,I.columnObjectOfName['X'].up,I.columnObjectOfName['constraint'].up,I.columnObjectOfName['constraint'], I.columnObjectOfName['constraint'],I.columnObjectOfName['X'].up.name + "_constraint")
                        #constraintCell.left.right = constraintCell.right.left = constraintCell.up.down = constraintCell.down.up = constraintCell 
	    else:
		for q in pentominos.fixed_pentominos_of(p):
		    #m = q.max()
		    for i in range(8):#self.board.size[0]-m[0]-1):
			for j in range(8):#self.board.size[1]-m[1]-1):
			    if self.board.valid_tile_placement(q.coos):
				I.appendRow(p.name,[str(c[0])+str(c[1]) for c in q.coos])
                                #if q in [pentominos.P().flip(0), pentominos.P().flip(0).turn90(), pentominos.P().flip(0).turn90().turn90(), pentominos.P().flip(0).turn90().turn90().turn90()]:
                                   #constraintCell = incidence_matrix.IncidenceCell(I.columnObjectOfName['P'].up.left,I.columnObjectOfName['P'].up,I.columnObjectOfName['constraint'].up,I.columnObjectOfName['constraint'], I.columnObjectOfName['constraint'],I.columnObjectOfName['P'].up.name + "_constraint")
                                   #constraintCell.left.right = constraintCell.right.left = constraintCell.up.down = constraintCell.down.up = constraintCell
			    q.translate_one(1)
			q.normalize_coo(1)
			q.translate_one(0)
        I.h.size = float("inf")
        I.columnObjectOfName['constraint'].size = float("inf")
	return self.solve(I, 0)
      
    def solve(self, incidences, counter):
	""" recursively add a tile to a partial solution until the whole board is covered """
	#breaking point
	if incidences.h.right == incidences.h or incidences.h.right == incidences.columnObjectOfName['constraint']:
	    return counter + 1
	#determine the column object according to the selection rule
	s = float("inf")
	c = incidences.h.right
	j = incidences.h.right
	while j != incidences.h:
	    if j.size < s:
		c = j
		s = j.size
	    j = j.right
        #c = min(incidences.columnObjectOfName.values(),key=self.get_size)
        
	#recursive calls
	incidences.coverColumn(c)
	r = c.down
	while r != c:
	    j = r.right
	    while j != r:
		incidences.coverColumn(j.listHeader)
		j = j.right
	    counter = self.solve(incidences, counter)
	    j = r.left
	    while j != r:
		incidences.uncoverColumn(j.listHeader)
		j = j.left
            r = r.down
	incidences.uncoverColumn(c)
	return counter

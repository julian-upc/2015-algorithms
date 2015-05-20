import IncidenceMatrix

class Table(object):
    def __init__(self, rows, columns, blocked):
        self.rows = rows
        self.columns = columns
        self.blocked = blocked
        
    def validTilePlacement(self,coos):
	for c in coos:
	    if c in self.blocked:
		return 0
	return 1

    def representation(self):
        rep = []
        for i in range(self.rows):
            for j in range(self.columns):
		if [i,j] not in self.blocked:
		    rep.append([i,j])
        return str(rep)

        
class Covering(object):
    def __init__(self, table, tiles, tileStock, fixedTiles):
	self.table = table
	self.tiles = tiles
	self.tileStock = tileStock
	self.fixedTiles = fixedTiles

    def allSolutions():
	#initialize the appropriate incidence matrix
	I = IncidenceMatrix([t.name for t in self.tiles] + [t[0] + t[1] for t in table.representation()])
	#for tile in [t[0] for t in self.tileStock]:
	  #  for 



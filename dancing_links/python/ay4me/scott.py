import pentominos
import incidence_matrix
import sys

class Problem(object):
	"""The problem gets a TileSet of pentominos to work with. The range of the field to cover. 
	A function legal() that tests whether a set of coordinates is legal and a number how often each single tile is allowed to be used.
	This number is -1 if the tiles may be used arbitrary often."""
	def __init__(self,WorkingSet,FRange,legal,usgNr):
		self.WorkingSet = WorkingSet
		# self.tiles = []
		# for p in self.WorkingSet:
		# 	self.tiles.extend(pentominos.fixed_pentominos_of(p))
		# self.tileNames = {}
		# for t in self.tiles:
		# 	n = t.name + "1"
		# 	while n in self.tileNames.values():
		# 		x = n[-1]
		# 		n = n[:-1]
		# 		num = int(x)+1
		# 		n += str(num)
		# 	self.tileNames[t] = n
		self.FRange = FRange
		self.usgNr = usgNr
		self.legal = legal
		self.IncMatrix = self.createMatrix()
		#self.usgNr = usgNr
		#print "created new problem"


	def createMatrix(self):
		"""creates the columns for the matrix"""
		#names = [p.name for p in WorkingSet]
		
		names = []
		# for p in self.tiles:
		for p in self.WorkingSet:
			# names.append(self.tileNames[p])
			names.append(p.name)
		for i in range(self.FRange):
			for j in range(self.FRange):
				if self.legal([i,j]):
					names.append(str(i)+str(j))
		return incidence_matrix.IncidenceMatrix(names)

	def completeMatrix(self):
		"""creates all rows"""
		for p in self.WorkingSet:
			tiles = pentominos.fixed_pentominos_of(p)
			#print tiles.representation()
			for t in tiles:
				for i in range(self.FRange):
					for j in range(self.FRange):
						#print "test coordinates " + str(i) + " and "+str(j)
						t.translate_by([i,j])
						l = True
						for x in t.coos:
							if not self.legal(x):
								l = False
								break
						if l:
							# self.IncMatrix.appendRow(self.tileNames[t],self.placement(t))
							self.IncMatrix.appendRow(t.name,self.placement(t))
						t.translate_by([-i,-j])


	def placement(self,tile):
		coos = tile.coos
		placement = []
		for c in coos:
			placement.append(str(c[0])+str(c[1]))
		return placement

	def solve(self):
		O = {}
		O = self.search(0,O)
		print "solution found:" + O

	def search(self,k,O):
		if self.IncMatrix.h.right is self.IncMatrix.h:
			return O
		else:
			c = self.IncMatrix.h
			s = sys.maxint
			j = self.IncMatrix.h.right
			while j is not self.IncMatrix.h:
				if j.size < s:
					c = j
					s = j.size
			self.IncMatrix.coverColumn(c)
			currentRow = c.down #r
        	while currentRow is not c:
        		O[k] = currentRow
        		currentColumn = currentRow.right
        		while currentColumn is not r:
        			self.IncMatrix.coverColumn(currentColumn.listHeader)
        			currentColumn = currentColumn.right
        		self.search(k+1,O)
        		currentRow = O[k]
        		c = currentRow.listHeader #necessary?
        		currentColumn = currentRow.left #necessary?
        		while currentColumn is not r:
        			self.IncMatrix.uncoverColumn(currentColumn.listHeader)
        			currentColumn = currentColumn.left
        		currentRow = currentRow.down
        	self.IncMatrix.uncoverColumn(c)
        	return {}
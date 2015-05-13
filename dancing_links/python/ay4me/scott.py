import pentominos
import incidence_matrix
import sys

class Problem(object):
	"""The problem gets a TileSet of pentominos to work with. The range of the field to cover. 
	A function legal() that tests whether a set of coordinates is legal and a number how often each single tile is allowed to be used.
	This number is -1 if the tiles may be used arbitrary often."""
	def __init__(self,WorkingSet,FRange,legal,usgNr,pFlip):
		self.WorkingSet = WorkingSet
		self.FRange = FRange
		self.usgNr = usgNr
		self.legal = legal
		self.pFlip = pFlip
		self.IncMatrix = self.createMatrix()
		self.solutionList = []
		self.searchNodes = 0

	def createMatrix(self):
		"""creates the columns for the matrix"""
		
		names = []
		for p in self.WorkingSet:
			names.append(p.name)
		for i in range(self.FRange):
			for j in range(self.FRange):
				if self.legal([i,j]):
					names.append(str(i)+str(j))
		return incidence_matrix.IncidenceMatrix(names)

	def completeMatrix(self):
		"""creates all rows"""
		for p in self.WorkingSet:
			if self.pFlip and p.name == "P":
				tiles = pentominos.TileSet()
				tiles.add(p)
				p.turn90()
				tiles.add(p)
				p.turn90()
				tiles.add(p)
				p.turn90()
				tiles.add(p)
				p.turn90()
			else:
				tiles = pentominos.fixed_pentominos_of(p)
			for t in tiles:
				for i in range(self.FRange):
					for j in range(self.FRange):
						t.translate_by([i,j])
						l = True
						for x in t.coos:
							if not self.legal(x):
								l = False
								break
						if l:
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
		self.search(0,O)
		if self.solutionList != []:
			print "solutions found:" + str(self.solutionList)
			print "number of searchNodes:" + str(self.searchNodes)
		else:
			print "no solution"

	def search(self,k,O):
		self.searchNodes += 1
		if self.IncMatrix.h.right is self.IncMatrix.h:
			solution = ""
			for i in range(k):
				currentRow = O[i]
				solution += "(" + currentRow.listHeader.name + ","
				currentColumn = currentRow.right
				while currentColumn is not currentRow:
					solution += "[" + currentColumn.listHeader.name + "],"
					currentColumn = currentColumn.right
				solution += ")"
			self.solutionList.append(solution)
			return solution
		else:
			c = self.IncMatrix.h
			s = sys.maxint
			j = self.IncMatrix.h.right
			while j is not self.IncMatrix.h:
				if j.size < s:
					c = j
					s = j.size
				j = j.right
			self.IncMatrix.coverColumn(c)
			currentRow = c.down #r
			while currentRow is not c:
				O[k] = currentRow
				currentColumn = currentRow.right
				while currentColumn is not currentRow:
					self.IncMatrix.coverColumn(currentColumn.listHeader)
					currentColumn = currentColumn.right
				self.search(k+1,O)
				currentRow = O[k]
				c = currentRow.listHeader
				currentColumn = currentRow.left
				while currentColumn is not currentRow:
					self.IncMatrix.uncoverColumn(currentColumn.listHeader)
					currentColumn = currentColumn.left
				currentRow = currentRow.down
			self.IncMatrix.uncoverColumn(c)
			return {}
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
		self.IncMatrixX12 = self.createMatrix()
		self.IncMatrixX13 = self.createMatrix()
		self.IncMatrixX22 = self.createMatrix()
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
				if t.name == "X":
					self.IncMatrix.appendRow("X", ["02", "11", "12", "13", "22"])#12
					self.IncMatrix.appendRow("X", ["03", "12", "13", "14", "23"])#13
					self.IncMatrix.appendRow("X", ["12", "21", "22", "23", "32"])#22 (21 and 32 unique to this case)
				else:
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
		# #find X column
		# currentColumn = h
		# while currentColumn.name != "X":
		# 	currentColumn = currentColumn.right
		# self.IncMatrix.coverColumn(currentColumn) #cover X column
		# for pos in [12,13,22]:
		# 	currentRow = currentColumn.down
		# 	while not has(pos,currentRow):#find row that has the position
		# 		currentRow = currentRow.down
		# 	O[0] = currentRow #add this row to solution
		# 	currentColumn = currentRow.right
		# 	while currentColumn is not currentRow:
		# 		self.IncMatrix.coverColumn(currentColumn.listHeader)
		# 		currentColumn = currentColumn.right
		# 	if pos == 22:
		# 		#remove flipped P
		# 	sol = self.search(1,O)
		# 	if sol != {}:
		# 	print "solution found:" + sol
		# 	currentRow = O[0]
		# 	c = currentRow.listHeader #necessary?
		# 	currentColumn = currentRow.left #necessary?
		# 	while currentColumn is not currentRow:
		# 		self.IncMatrix.uncoverColumn(currentColumn.listHeader)
		# 		currentColumn = currentColumn.left
		sol = self.search(0,O)
		if sol != {}:
			print "solution found:" + sol
		else:
			print "no solution"
		return sol

	def has(self,value,currentRow):
		isin = False
		row = currentRow.right
		while row is not currentRow:
			if row.listHeader.name == str(value):
				isin = True
			row = row.right
		return isin

	def search(self,k,O):
		if self.IncMatrix.h.right is self.IncMatrix.h:
			#return solution as string
			solution = ""
			for i in range(k):
				currentRow = O[i]
				solution += currentRow.listHeader.name
				currentColumn = currentRow.right
				while currentColumn is not currentRow:
					solution += currentColumn.listHeader.name
					currentColumn = currentColumn.right
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
				if c.name == "X" and self.has(21,currentRow):
					#remove all flipped P's
					#self.removeFlippedP(self)
					pass
				self.search(k+1,O)
				currentRow = O[k]
				c = currentRow.listHeader #necessary?
				if c.name == "X" and self.has(21,currentRow):
					#remove all flipped P's
					#self.restoreFlippedP(self)
					pass
				currentColumn = currentRow.left #necessary?
				while currentColumn is not currentRow:
					self.IncMatrix.uncoverColumn(currentColumn.listHeader)
					currentColumn = currentColumn.left
				currentRow = currentRow.down
			self.IncMatrix.uncoverColumn(c)
			return {}

	def removeFlippedP(self):
		#find P column
		currentColumn = h
		while currentColumn.name != "P":
			currentColumn = currentColumn.right


	def restoreFlippedP(self):
		pass
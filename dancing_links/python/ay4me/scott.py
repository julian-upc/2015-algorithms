import pentominos
import incidence_matrix

class Problem(object):
	"""The problem gets a TileSet of pentominos to work with. The range of the field to cover. 
	A taboolist of forbidden coordinates and a number how often each single tile is allowed to be used.
	This number is -1 if the tiles may be used arbitrary often."""
	def __init__(self,WorkingSet,FRange,legal,usgNr):
		self.IncMatrix = createMatrix(WorkingSet,FRange,taboo)
		self.usgNr = usgNr
		return self


	def AllowTabooCoos(c,taboo):
		if c not in taboo:
			return True
		else:
			return False

	def createMatrix(WorkingSet,FRange,taboo):
		#names = [p.name for p in WorkingSet]
		names = []
		for p in WorkingSet:
			names.append(p.name)
		for i in range(FRange):
			for j in range(FRange):
				if legal([i,j]):
					names.append(str(i)+str(j))
		return incidence_matrix.IncidenceMatrix(names)

import scott
import unittest
import incidence_matrix
import pentominos
import copy

class TestScottProblem(unittest.TestCase):

#["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"]

	def testSetup(self):
		TSet = pentominos.TileSet([pentominos.F(),pentominos.I(),pentominos.L(),pentominos.P(),pentominos.N(),pentominos.T(),pentominos.U(),pentominos.V(),pentominos.W(),pentominos.X(),pentominos.Y(),pentominos.Z()])
		names = [p.name for p in TSet]
		for n in ["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"]:
			self.assertTrue(n in names)
		for n in names:
			self.assertTrue(n in ["F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z"])
		prob = scott.Problem(TSet,8,self.legal,1)
		# IM = copy.deepcopy(prob.IncMatrix)
		# IM.appendRow("I", ["00", "01", "02", "03", "04"])
		# IM.appendRow("I", ["01", "02", "03", "04", "05"])
		# rep = [IM.columnObjectOfName[i].representation() for i in ["I", "00", "01", "02", "03", "04"]]
		# self.assertEqual([[[['h(2)', 'I', 'root', 'F', 'I[1]', 'I[0]'], ['c', 'I[0]', 'I04', 'I00', 'I', 'I[1]'], ['c', 'I[1]', 'I05', 'I01', 'I[0]', 'I']]], 
		# 	[[['h(1)', '00', 'V', '01', 'I00', 'I00'], ['c', 'I00', 'I[0]', 'I01', '00', '00']]], [[['h(2)', '01', '00', '02', 'I01', 'I01'], ['c', 'I01', 'I00', 'I02', '01', 'I01'], 
		# 	['c', 'I01', 'I[1]', 'I02', 'I01', '01']]], [[['h(2)', '02', '01', '03', 'I02', 'I02'], ['c', 'I02', 'I01', 'I03', '02', 'I02'], ['c', 'I02', 'I01', 'I03', 'I02', '02']]], 
		# 	[[['h(2)', '03', '02', '04', 'I03', 'I03'], ['c', 'I03', 'I02', 'I04', '03', 'I03'], ['c', 'I03', 'I02', 'I04', 'I03', '03']]], [[['h(2)', '04', '03', '05', 'I04', 'I04'], 
		# 	['c', 'I04', 'I03', 'I[0]', '04', 'I04'], ['c', 'I04', 'I03', 'I05', 'I04', '04']]]], rep)
		# #print IM.representation()

	def testMatrix(self):
		TSet = pentominos.TileSet([pentominos.F(),pentominos.I(),pentominos.L(),pentominos.P(),pentominos.N(),pentominos.T(),pentominos.U(),pentominos.V(),pentominos.W(),pentominos.X(),pentominos.Y(),pentominos.Z()])
		names = [p.name for p in TSet]
		prob = scott.Problem(TSet,8,self.legal,1)
		str1 = prob.IncMatrix.representation()
		prob.completeMatrix()
		str2 = prob.IncMatrix.representation()
		self.assertFalse(str1 == str2)
		print prob.solve()

	def legal(self,coos):
		if coos in [[3,3],[3,4],[4,3],[4,4]] or coos[0]<0 or coos[0]>7 or coos[1]<0 or coos[1]>7:
			return False
		return True


suite = unittest.TestLoader().loadTestsFromTestCase(TestScottProblem)

if __name__ == '__main__':
    unittest.main()
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
		prob = scott.Problem(TSet,8,self.legal,1,0)
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
		TSet = pentominos.TileSet([pentominos.F(),pentominos.I(),pentominos.L(),pentominos.P(),pentominos.N(),pentominos.T(),pentominos.U(),pentominos.V(),pentominos.W(),pentominos.Y(),pentominos.Z()])
		names = [p.name for p in TSet]
		probX12 = scott.Problem(TSet,8,self.legal1,1,0)
		probX13 = scott.Problem(TSet,8,self.legal2,1,0)
		probX22 = scott.Problem(TSet,8,self.legal3,1,1)
		str1 = probX12.IncMatrix.representation()
		probX12.completeMatrix()
		str2 = probX12.IncMatrix.representation()
		self.assertFalse(str1 == str2)

		str1 = probX13.IncMatrix.representation()
		probX13.completeMatrix()
		str2 = probX13.IncMatrix.representation()
		self.assertFalse(str1 == str2)

		str1 = probX22.IncMatrix.representation()
		probX22.completeMatrix()
		str2 = probX22.IncMatrix.representation()
		self.assertFalse(str1 == str2)

		probX12.solve()
		sol12 = probX12.solutionList
		self.assertEqual(len(sol12),19)
		probX13.solve()
		sol13 = probX13.solutionList
		self.assertEqual(len(sol13),24)
		probX22.solve()
		sol22 = probX22.solutionList
		self.assertEqual(len(sol22),33)
		if sol12 != {}:
			sol12 += "(X,[02,11,12,13,22])" #12
		if sol13 != {}:
			sol13 += "(X,[03,12,13,14,23])" #13
		if sol22 != {}:
			sol22 += "(X,[12,21,22,23,32])" #22
		print sol12
		print sol13
		print sol22

	def legal(self,coos):
		if coos in [[3,3],[3,4],[4,3],[4,4]] or coos[0]<0 or coos[0]>7 or coos[1]<0 or coos[1]>7:
			return False
		return True

	def legal1(self,coos):
		if coos in [[3,3],[3,4],[4,3],[4,4],[0,2],[1,1],[1,2],[1,3],[2,2]] or coos[0]<0 or coos[0]>7 or coos[1]<0 or coos[1]>7:
			return False
		return True

	def legal2(self,coos):
		if coos in [[3,3],[3,4],[4,3],[4,4],[0,3],[1,2],[1,3],[1,4],[2,3]] or coos[0]<0 or coos[0]>7 or coos[1]<0 or coos[1]>7:
			return False
		return True

	def legal3(self,coos):
		if coos in [[3,3],[3,4],[4,3],[4,4],[1,2],[2,1],[2,2],[2,3],[3,2]] or coos[0]<0 or coos[0]>7 or coos[1]<0 or coos[1]>7:
			return False
		return True


suite = unittest.TestLoader().loadTestsFromTestCase(TestScottProblem)

if __name__ == '__main__':
    unittest.main()
import unittest
import incidence_matrix
import pentominos
import examples
import copy
import scott_matrix

class TestScottMatrixMethods(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_creating_scott_matrix(self):
        IM = scott_matrix.Scott_matrix(8,8)
        IM.create_scott_matrix(IM.scott_legal)
        #IM = scott_matrix.create_matrix()
        #I.appendRow("I", ["00", "01", "02", "03", "04"])
        #I.appendRow("I", ["01", "02", "03", "04", "05"])
        #rep = [I.columnObjectOfName[i].representation() for i in ["I", "00", "01", "02", "03", "04"]]
        #self.assertEqual([[[['h(2)', 'I', 'F', 'L', 'I[1]', 'I[0]'], ['c', 'I[0]', 'I04', 'I00', 'I', 'I[1]'], ['c', 'I[1]', 'I05', 'I01', 'I[0]', 'I']]], [[['h(1)', '00', 'Z', '01', 'I00', 'I00'], ['c', 'I00', 'I[0]', 'I01', '00', '00']]], [[['h(2)', '01', '00', '02', 'I01', 'I01'], ['c', 'I01', 'I00', 'I02', '01', 'I01'], ['c', 'I01', 'I[1]', 'I02', 'I01', '01']]], [[['h(2)', '02', '01', '03', 'I02', 'I02'], ['c', 'I02', 'I01', 'I03', '02', 'I02'], ['c', 'I02', 'I01', 'I03', 'I02', '02']]], [[['h(2)', '03', '02', '04', 'I03', 'I03'], ['c', 'I03', 'I02', 'I04', '03', 'I03'], ['c', 'I03', 'I02', 'I04', 'I03', '03']]], [[['h(2)', '04', '03', '05', 'I04', 'I04'], ['c', 'I04', 'I03', 'I[0]', '04', 'I04'], ['c', 'I04', 'I03', 'I05', 'I04', '04']]]], rep)

    def test_construct_running_example(self):
        I = examples.running_example()
        origRep = [[['h(0)', 'root', 'G', 'A', 'root', 'root']], [['h(2)', 'A', 'root', 'B', 'A[1]', 'A[0]'], ['c', 'A[0]', 'AG', 'AD', 'A', 'A[1]'], ['c', 'A[1]', 'AD', 'AD', 'A[0]', 'A']], [['h(2)', 'B', 'A', 'C', 'B[1]', 'B[0]'], ['c', 'B[0]', 'BF', 'BC', 'B', 'B[1]'], ['c', 'B[1]', 'BG', 'BG', 'B[0]', 'B']], [['h(2)', 'C', 'B', 'D', 'BC', 'C[0]'], ['c', 'C[0]', 'CF', 'CE', 'C', 'BC'], ['c', 'BC', 'B[0]', 'BF', 'C[0]', 'C']], [['h(3)', 'D', 'C', 'E', 'D[0]', 'AD'], ['c', 'AD', 'A[0]', 'AG', 'D', 'AD'], ['c', 'AD', 'A[1]', 'A[1]', 'AD', 'D[0]'], ['c', 'D[0]', 'DG', 'DE', 'AD', 'D']], [['h(2)', 'E', 'D', 'F', 'DE', 'CE'], ['c', 'CE', 'C[0]', 'CF', 'E', 'DE'], ['c', 'DE', 'D[0]', 'DG', 'CE', 'E']], [['h(2)', 'F', 'E', 'G', 'BF', 'CF'], ['c', 'CF', 'CE', 'C[0]', 'F', 'BF'], ['c', 'BF', 'BC', 'B[0]', 'CF', 'F']], [['h(3)', 'G', 'F', 'root', 'DG', 'AG'], ['c', 'AG', 'AD', 'A[0]', 'G', 'BG'], ['c', 'BG', 'B[1]', 'B[1]', 'AG', 'DG'], ['c', 'DG', 'DE', 'D[0]', 'BG', 'G']]]
        self.assertEqual(origRep, I.representation())

    def test_cover_3_running_example(self):
        I = examples.running_example()
        origRep = I.representation()
        for n in ["A", "D", "G"]:
            I.coverColumn(I.columnObjectOfName[n])
        self.assertEqual([[['h(0)', 'root', 'F', 'B', 'root', 'root']], [['h(1)', 'B', 'root', 'C', 'B[0]', 'B[0]'], ['c', 'B[0]', 'BF', 'BC', 'B', 'B']], [['h(2)', 'C', 'B', 'E', 'BC', 'C[0]'], ['c', 'C[0]', 'CF', 'CE', 'C', 'BC'], ['c', 'BC', 'B[0]', 'BF', 'C[0]', 'C']], [['h(1)', 'E', 'C', 'F', 'CE', 'CE'], ['c', 'CE', 'C[0]', 'CF', 'E', 'E']], [['h(2)', 'F', 'E', 'root', 'BF', 'CF'], ['c', 'CF', 'CE', 'C[0]', 'F', 'BF'], ['c', 'BF', 'BC', 'B[0]', 'CF', 'F']]], I.representation())
        for n in ["G", "D", "A"]:
            I.uncoverColumn(I.columnObjectOfName[n])

        self.assertEqual(origRep, I.representation())


suite = unittest.TestLoader().loadTestsFromTestCase(TestScottMatrixMethods)

if __name__ == '__main__':
    unittest.main()

import unittest
import pentominos

class TestSaSyb(unittest.TestCase):

    def test_SaSyb(self):
        x = pentominos.X()
        print(x.representation())
        """
        i = pentominos.I()
        print(i.representation())
        i.translate_by([2,1])
        print(i.representation())
        
        print(i.turn90().representation())
        """
        print(x.turn90().representation())
        
suite = unittest.TestLoader().loadTestsFromTestCase(TestSaSyb)

if __name__ == '__main__':
    unittest.main()

import unittest
import pentominos
import copy

class TestPentominoMethods(unittest.TestCase):

#    def setUp(self):

    def test_normalize(self):
        for p in pentominos.all_pentominos():
            self.assertEqual(p.coos, p.normalize().coos, "test_normalize failed for polyomino " + p.name)

    def test_translate(self):
        self.assertEqual([[c[0]+1,c[1]] for c in pentominos.I().coos], pentominos.I().translate_one(0).coos)
        self.assertEqual([[c[0],c[1]+1] for c in pentominos.I().coos], pentominos.I().translate_one(1).coos)

    def test_TileSet(self):
        s = pentominos.TileSet([pentominos.I(), pentominos.I()])
        self.assertEqual(s.size(), 1)

        reps = pentominos.TileSet()
        p = pentominos.Y()
        reps.add(p)
        p.flip(0)
        reps.add(p)
        p.flip(1)
        reps.add(p)
        p.flip(0)
        reps.add(p)
        self.assertEqual(reps.size(), 4)

        reps = pentominos.TileSet()
        p = pentominos.Y()
        reps.add(p)
        p.turn90()
        reps.add(p)
        p.turn90()
        reps.add(p)
        p.turn90()
        reps.add(p)
        self.assertEqual(reps.size(), 4)
        

    def test_turn90(self):
        c0 = copy.deepcopy(pentominos.I().coos)
        self.assertEqual(c0, pentominos.I().turn90().turn90().coos)

        p = pentominos.Y()
        s = pentominos.TileSet()
        for i in range(4):
            s.add(p)
            p.turn90()
        self.assertEqual(4, s.size())
        

    def test_max(self):
        self.assertEqual([0,4], pentominos.I().max())
        self.assertEqual([2,2], pentominos.F().max())

    def test_set(self):
        s = set([pentominos.I(), pentominos.I()])
        self.assertEqual(len(s), 1)

    def test_fixed_pentominos(self):
        orbitSize = dict()
        for p in pentominos.all_pentominos():
            orbitSize[p.name] = pentominos.fixed_pentominos_of(p).size()

        self.assertEqual(dict({'F': 8, 'I': 2, 'L': 8, 'N': 8, 'P': 8, 'U': 4, 'T': 4, 'W': 4, 'V': 4, 'Y': 8, 'X': 1, 'Z': 4}), orbitSize)
        self.assertEqual(pentominos.all_fixed_pentominos().size(), 63)

suite = unittest.TestLoader().loadTestsFromTestCase(TestPentominoMethods)

if __name__ == '__main__':
    unittest.main()

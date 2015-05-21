struct pentomino_fixture {
   pentomino_fixture() : I("I") {}
   pentominos::Pentomino I;
};

BOOST_FIXTURE_TEST_CASE( constructor_test, pentomino_fixture )
{
   BOOST_CHECK_EQUAL(I.coos.size(), (size_t)5);
}

BOOST_FIXTURE_TEST_CASE( coordinate_test, pentomino_fixture )
{
   const std::vector<pentominos::CooType> expected_I_coos{{0,0},{0,1},{0,2},{0,3},{0,4}};
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 expected_I_coos.begin(), expected_I_coos.end());
}

BOOST_FIXTURE_TEST_CASE( representation_test, pentomino_fixture )
{
   std::ostringstream oss;
   oss << I;
   std::string I_expected{"[I:{{0,0},{0,1},{0,2},{0,3},{0,4}}]"};
   BOOST_CHECK_EQUAL(oss.str(), I_expected);
}

BOOST_FIXTURE_TEST_CASE( translation_test_x, pentomino_fixture )
{
   I.translate_one(0);
   const std::vector<pentominos::CooType> expected_I_coos{{1,0},{1,1},{1,2},{1,3},{1,4}};
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 expected_I_coos.begin(), expected_I_coos.end());
}

BOOST_FIXTURE_TEST_CASE( translation_test_y, pentomino_fixture )
{
   I.translate_one(1);
   const std::vector<pentominos::CooType> expected_I_coos{{0,1},{0,2},{0,3},{0,4},{0,5}};
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 expected_I_coos.begin(), expected_I_coos.end());
}

BOOST_FIXTURE_TEST_CASE( flip_test_I, pentomino_fixture )
{
   const std::vector<pentominos::CooType> expected_I_coos{I.coos};
   I.flip(0);
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 expected_I_coos.begin(), expected_I_coos.end());
}

BOOST_AUTO_TEST_CASE( flip_test_F )
{
   pentominos::Pentomino F("F");
   F.flip(0);
   const std::vector<pentominos::CooType> expected_F_coos{{0, 2}, {1, 0}, {1, 1}, {1, 2}, {2, 1}};
   BOOST_CHECK_EQUAL_COLLECTIONS(F.coos.begin(), F.coos.end(),
                                 expected_F_coos.begin(), expected_F_coos.end());
}

BOOST_FIXTURE_TEST_CASE( turn_test_I, pentomino_fixture )
{
   const std::vector<pentominos::CooType> expected_I_coos{{0,0},{1,0},{2,0},{3,0},{4,0}};
   I.turn90();
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 expected_I_coos.begin(), expected_I_coos.end());
}

BOOST_FIXTURE_TEST_CASE( turn_test_I_2, pentomino_fixture )
{
   pentominos::Pentomino Ip(I);
   Ip.turn90().turn90();
   BOOST_CHECK_EQUAL_COLLECTIONS(I.coos.begin(), I.coos.end(),
                                 Ip.coos.begin(), Ip.coos.end());
}

BOOST_AUTO_TEST_CASE( turn_test_Y )
{
   std::set<pentominos::Pentomino> s;
   pentominos::Pentomino Y{"Y"};
   for (int i=0; i<4; ++i) {
      s.insert(Y);
      Y.turn90();
   }
   BOOST_CHECK_EQUAL(s.size(), (size_t)4);
}

BOOST_FIXTURE_TEST_CASE( max_test_I, pentomino_fixture )
{
   const pentominos::CooType
      m(I.max()),
      expected{0,4};
   BOOST_CHECK_EQUAL_COLLECTIONS(m.begin(), m.end(),
                                 expected.begin(), expected.end());
}

BOOST_AUTO_TEST_CASE( max_test_F )
{
   pentominos::Pentomino F{"F"};
   const pentominos::CooType
      m(F.max()),
      expected{2,2};
   BOOST_CHECK_EQUAL_COLLECTIONS(m.begin(), m.end(),
                                 expected.begin(), expected.end());
}

BOOST_FIXTURE_TEST_CASE( set_test_I, pentomino_fixture )
{
   std::set<pentominos::Pentomino> s;
   s.insert(I);
   s.insert(I);
   BOOST_CHECK_EQUAL(s.size(), (size_t)1);
}

BOOST_AUTO_TEST_CASE( test_fixed_pentominos )
{
   std::map<std::string,int> orbit_size;
   for (const auto& P : pentominos::all_pentominos()) {
      orbit_size[P.name] = pentominos::fixed_pentominos_of(P).size();
   }
   std::map<std::string,int> expected{{"F", 8}, {"I", 2}, {"L", 8}, {"N", 8}, {"P", 8}, {"U", 4}, {"T", 4}, {"W", 4}, {"V", 4}, {"Y", 8}, {"X", 1}, {"Z", 4}};
   BOOST_CHECK_EQUAL_COLLECTIONS(orbit_size.begin(), orbit_size.end(),
                                 expected.begin(), expected.end());
}

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

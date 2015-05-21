/* Copyright (c) 2015
   Julian Pfeifle
   julian.pfeifle@upc.edu

   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the
   Free Software Foundation; either version 3, or (at your option) any
   later version: http://www.gnu.org/licenses/gpl.txt.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
--------------------------------------------------------------------------------
*/

#include "dancing_links.h"
#include "stl_wrappers.h"

using namespace pentominos;
using namespace incidence_matrix;

struct running_example_fixture {
   IncidenceMatrix<std::string> I;

   running_example_fixture() 
      : I( { "A", "B", "C", "D", "E", "F", "G" } )
   {
      I.append_row("C", {"E", "F"});
      I.append_row("A", {"D", "G"});
      I.append_row("B", {"C", "F"});
      I.append_row("A", {"D"});
      I.append_row("B", {"G"});
      I.append_row("D", {"E", "G"});
   }
};

BOOST_FIXTURE_TEST_CASE( algorithm_X_running, running_example_fixture )
{
   std::vector<dancing_links::Solution> 
      solutions = dancing_links::Algorithm_X(I),
      expected {
      {{{"A", "D"}, {"E", "F", "C"}, {"B", "G"}}}
   };
   
   BOOST_CHECK_EQUAL_COLLECTIONS(solutions.begin(), solutions.end(),
                                 expected.begin(), expected.end());   
}   

struct scott_example_fixture {
   static std::set<CooType> holes;
   IncidenceMatrix<CooType> I;

   scott_example_fixture() 
      : I(scott_names()) {};

   static bool allow_outside_hole(const CooType& c) {
      return holes.find(c) == holes.end();
   }

   std::vector<std::string> scott_names() {
      std::vector<std::string> scott_names { "F", "I", "L", "P", "N", "T", "U", "V", "W", "X", "Y", "Z" };
      for (int i=0; i<8; ++i) 
         for (int j=0; j<8; ++j) 
            if (allow_outside_hole({i,j})) 
               scott_names.push_back(to_string(CooType{i,j}));
      return scott_names;
   }
};

std::set<CooType> scott_example_fixture::holes { {3,3}, {3,4}, {4,3}, {4,4 } };

BOOST_FIXTURE_TEST_CASE( scott_type_a, scott_example_fixture )
{
   const std::set<Pentomino> reps { all_fixed_pentominos() };
   Pentomino P("X");
   P.translate_by({ 0, 1 });
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { {P.name, { P.coos } } };
   I.append_translates_2d(reps,
                          CooType { 8, 8 },
                          allow_outside_hole,
                          required_placements);
   std::vector<dancing_links::Solution> 
      solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 19);
}

BOOST_FIXTURE_TEST_CASE( scott_type_b, scott_example_fixture )
{
   const std::set<Pentomino> reps { all_fixed_pentominos() };
   Pentomino P("X");
   P.translate_by({ 0, 2 });
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { { P.name, { P.coos } } };
   I.append_translates_2d(reps,
                          CooType { 8, 8 },
                          allow_outside_hole,
                          required_placements);
   std::vector<dancing_links::Solution> 
      solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 20);
}


BOOST_FIXTURE_TEST_CASE( scott_type_c, scott_example_fixture )
{
   std::vector<Pentomino> reps;
   for (const auto& p : all_pentominos()) {
      if (p.name != "P") {
         for (const auto& q : fixed_pentominos_of(p)) {
            reps.push_back(q);
         }
      } else {
         for (const auto& q : rotated_pentominos_of(p)) {
            reps.push_back(q);
         }
      }
   }
   Pentomino P("X");
   P.translate_by({ 1, 1 });
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { { P.name, { P.coos } } };
   I.append_translates_2d(reps,
                          CooType { 8, 8 },
                          allow_outside_hole,
                          required_placements);
   std::vector<dancing_links::Solution> 
      solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 26);
}

BOOST_AUTO_TEST_CASE( y_pentomino_0 )
{
   Pentomino 
      Y0("Y0", { {0,0},{0,1},{1,1},{0,2},{0,3} }),
      Y1("Y1", { {1,0},{0,1},{1,1},{1,2},{1,3} }),
      Y2("Y2", { {0,0},{0,1},{0,2},{1,2},{0,3} }),
      Y3("Y3", { {1,0},{1,1},{0,2},{1,2},{1,3} });
   Y2.translate_by({ 0, 11 });
   Y3.translate_by({ 11, 11 });
   IncidenceMatrix<CooType>::RequiredPlacementType required_placements { 
      { Y0.name, { Y0.coos } },
      { Y1.name, { Y1.coos } },
      { Y2.name, { Y2.coos } },
      { Y3.name, { Y3.coos } }
   };
   const std::set<Pentomino> tiles(fixed_pentominos_of(Y1));
   std::vector<std::string> names;
   for (unsigned int i=0; i<tiles.size(); ++i) {
      names.push_back("Y" + std::to_string(i));
   }
   for (int i=0; i<15; ++i) 
      for (int j=0; j<15; ++j) 
         names.push_back(to_string(CooType{i,j}));
   IncidenceMatrix<CooType> I(names);
   I.append_translates_2d(tiles,
                          CooType { 15, 15 },
                          [](const CooType&) -> bool { return true; },
                          required_placements);
   std::vector<dancing_links::Solution> 
      solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 0);
}

BOOST_AUTO_TEST_CASE( chess_square )
{
   const std::set<Pentomino> tiles { Pentomino("S", { {0,0}, {0,1}, {1,0}, {1,1} }) };
   const int board_size = 2;
   std::vector<std::string> names;
   for (const auto& tile : tiles) {
      names.push_back(tile.name);
   }
   for (int i=0; i<board_size; ++i) 
      for (int j=0; j<board_size; ++j) 
         names.push_back(to_string(CooType{i,j}));
   IncidenceMatrix<CooType> I(names);
   I.append_translates_2d(tiles,
                          CooType { board_size, board_size });
   BOOST_CHECK_EQUAL(I.rows, 1);

   std::vector<dancing_links::Solution> solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 1);
}

BOOST_AUTO_TEST_CASE( chess_4_square )
{
   std::vector<Pentomino> tiles;
   for (int i=0; i<4; ++i) { 
      tiles.push_back(Pentomino("S" + std::to_string(i), { {0,0}, {0,1}, {1,0}, {1,1} }) );
   }
   const int board_size = 4;
   std::vector<std::string> names;
   for (const auto& tile : tiles) {
      names.push_back(tile.name);
   }
   for (int i=0; i<board_size; ++i) 
      for (int j=0; j<board_size; ++j) 
         names.push_back(to_string(CooType{i,j}));
   IncidenceMatrix<CooType> I(names);
   I.append_translates_2d(tiles,
                          CooType { board_size, board_size });
   BOOST_CHECK_EQUAL(I.rows, 36); // 4 squares * 9 positions
   std::vector<dancing_links::Solution> solutions = dancing_links::Algorithm_X(I);
   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 24); // 4! placements of four 2x2 squares on a 4x4 grid
}


BOOST_AUTO_TEST_CASE( y_pentominos_45 )
{
   const std::set<Pentomino> Ys(fixed_pentominos_of(Pentomino("Y")));
   std::vector<Pentomino> tiles; 
   for (int i=0; i<45; ++i) {
      int j(0);
      for (const auto& _Y : Ys) {
         Pentomino Y(_Y);
         Y.name = "Y_" + std::to_string(i) + "_" + std::to_string(j++);
         tiles.push_back(Y);
      }
   }
   BOOST_CHECK_EQUAL(tiles.size(), (size_t) 360);
   std::vector<std::string> names;
   for (const auto& tile : tiles) {
      names.push_back(tile.name);
   }
   const int board_size = 15;
   for (int i=0; i<board_size; ++i) 
      for (int j=0; j<board_size; ++j) 
         names.push_back(to_string(CooType{i,j}));

   const std::vector<std::string> expected_names {
      "Y_0_0","Y_0_1","Y_0_2","Y_0_3","Y_0_4","Y_0_5","Y_0_6","Y_0_7","Y_1_0","Y_1_1","Y_1_2","Y_1_3","Y_1_4","Y_1_5","Y_1_6","Y_1_7","Y_2_0","Y_2_1","Y_2_2","Y_2_3","Y_2_4","Y_2_5","Y_2_6","Y_2_7","Y_3_0","Y_3_1","Y_3_2","Y_3_3","Y_3_4","Y_3_5","Y_3_6","Y_3_7","Y_4_0","Y_4_1","Y_4_2","Y_4_3","Y_4_4","Y_4_5","Y_4_6","Y_4_7","Y_5_0","Y_5_1","Y_5_2","Y_5_3","Y_5_4","Y_5_5","Y_5_6","Y_5_7","Y_6_0","Y_6_1","Y_6_2","Y_6_3","Y_6_4","Y_6_5","Y_6_6","Y_6_7","Y_7_0","Y_7_1","Y_7_2","Y_7_3","Y_7_4","Y_7_5","Y_7_6","Y_7_7","Y_8_0","Y_8_1","Y_8_2","Y_8_3","Y_8_4","Y_8_5","Y_8_6","Y_8_7","Y_9_0","Y_9_1","Y_9_2","Y_9_3","Y_9_4","Y_9_5","Y_9_6","Y_9_7","Y_10_0","Y_10_1","Y_10_2","Y_10_3","Y_10_4","Y_10_5","Y_10_6","Y_10_7","Y_11_0","Y_11_1","Y_11_2","Y_11_3","Y_11_4","Y_11_5","Y_11_6","Y_11_7","Y_12_0","Y_12_1","Y_12_2","Y_12_3","Y_12_4","Y_12_5","Y_12_6","Y_12_7","Y_13_0","Y_13_1","Y_13_2","Y_13_3","Y_13_4","Y_13_5","Y_13_6","Y_13_7","Y_14_0","Y_14_1","Y_14_2","Y_14_3","Y_14_4","Y_14_5","Y_14_6","Y_14_7","Y_15_0","Y_15_1","Y_15_2","Y_15_3","Y_15_4","Y_15_5","Y_15_6","Y_15_7","Y_16_0","Y_16_1","Y_16_2","Y_16_3","Y_16_4","Y_16_5","Y_16_6","Y_16_7","Y_17_0","Y_17_1","Y_17_2","Y_17_3","Y_17_4","Y_17_5","Y_17_6","Y_17_7","Y_18_0","Y_18_1","Y_18_2","Y_18_3","Y_18_4","Y_18_5","Y_18_6","Y_18_7","Y_19_0","Y_19_1","Y_19_2","Y_19_3","Y_19_4","Y_19_5","Y_19_6","Y_19_7","Y_20_0","Y_20_1","Y_20_2","Y_20_3","Y_20_4","Y_20_5","Y_20_6","Y_20_7","Y_21_0","Y_21_1","Y_21_2","Y_21_3","Y_21_4","Y_21_5","Y_21_6","Y_21_7","Y_22_0","Y_22_1","Y_22_2","Y_22_3","Y_22_4","Y_22_5","Y_22_6","Y_22_7","Y_23_0","Y_23_1","Y_23_2","Y_23_3","Y_23_4","Y_23_5","Y_23_6","Y_23_7","Y_24_0","Y_24_1","Y_24_2","Y_24_3","Y_24_4","Y_24_5","Y_24_6","Y_24_7","Y_25_0","Y_25_1","Y_25_2","Y_25_3","Y_25_4","Y_25_5","Y_25_6","Y_25_7","Y_26_0","Y_26_1","Y_26_2","Y_26_3","Y_26_4","Y_26_5","Y_26_6","Y_26_7","Y_27_0","Y_27_1","Y_27_2","Y_27_3","Y_27_4","Y_27_5","Y_27_6","Y_27_7","Y_28_0","Y_28_1","Y_28_2","Y_28_3","Y_28_4","Y_28_5","Y_28_6","Y_28_7","Y_29_0","Y_29_1","Y_29_2","Y_29_3","Y_29_4","Y_29_5","Y_29_6","Y_29_7","Y_30_0","Y_30_1","Y_30_2","Y_30_3","Y_30_4","Y_30_5","Y_30_6","Y_30_7","Y_31_0","Y_31_1","Y_31_2","Y_31_3","Y_31_4","Y_31_5","Y_31_6","Y_31_7","Y_32_0","Y_32_1","Y_32_2","Y_32_3","Y_32_4","Y_32_5","Y_32_6","Y_32_7","Y_33_0","Y_33_1","Y_33_2","Y_33_3","Y_33_4","Y_33_5","Y_33_6","Y_33_7","Y_34_0","Y_34_1","Y_34_2","Y_34_3","Y_34_4","Y_34_5","Y_34_6","Y_34_7","Y_35_0","Y_35_1","Y_35_2","Y_35_3","Y_35_4","Y_35_5","Y_35_6","Y_35_7","Y_36_0","Y_36_1","Y_36_2","Y_36_3","Y_36_4","Y_36_5","Y_36_6","Y_36_7","Y_37_0","Y_37_1","Y_37_2","Y_37_3","Y_37_4","Y_37_5","Y_37_6","Y_37_7","Y_38_0","Y_38_1","Y_38_2","Y_38_3","Y_38_4","Y_38_5","Y_38_6","Y_38_7","Y_39_0","Y_39_1","Y_39_2","Y_39_3","Y_39_4","Y_39_5","Y_39_6","Y_39_7","Y_40_0","Y_40_1","Y_40_2","Y_40_3","Y_40_4","Y_40_5","Y_40_6","Y_40_7","Y_41_0","Y_41_1","Y_41_2","Y_41_3","Y_41_4","Y_41_5","Y_41_6","Y_41_7","Y_42_0","Y_42_1","Y_42_2","Y_42_3","Y_42_4","Y_42_5","Y_42_6","Y_42_7","Y_43_0","Y_43_1","Y_43_2","Y_43_3","Y_43_4","Y_43_5","Y_43_6","Y_43_7","Y_44_0","Y_44_1","Y_44_2","Y_44_3","Y_44_4","Y_44_5","Y_44_6","Y_44_7","<0,0>","<0,1>","<0,2>","<0,3>","<0,4>","<0,5>","<0,6>","<0,7>","<0,8>","<0,9>","<0,10>","<0,11>","<0,12>","<0,13>","<0,14>","<1,0>","<1,1>","<1,2>","<1,3>","<1,4>","<1,5>","<1,6>","<1,7>","<1,8>","<1,9>","<1,10>","<1,11>","<1,12>","<1,13>","<1,14>","<2,0>","<2,1>","<2,2>","<2,3>","<2,4>","<2,5>","<2,6>","<2,7>","<2,8>","<2,9>","<2,10>","<2,11>","<2,12>","<2,13>","<2,14>","<3,0>","<3,1>","<3,2>","<3,3>","<3,4>","<3,5>","<3,6>","<3,7>","<3,8>","<3,9>","<3,10>","<3,11>","<3,12>","<3,13>","<3,14>","<4,0>","<4,1>","<4,2>","<4,3>","<4,4>","<4,5>","<4,6>","<4,7>","<4,8>","<4,9>","<4,10>","<4,11>","<4,12>","<4,13>","<4,14>","<5,0>","<5,1>","<5,2>","<5,3>","<5,4>","<5,5>","<5,6>","<5,7>","<5,8>","<5,9>","<5,10>","<5,11>","<5,12>","<5,13>","<5,14>","<6,0>","<6,1>","<6,2>","<6,3>","<6,4>","<6,5>","<6,6>","<6,7>","<6,8>","<6,9>","<6,10>","<6,11>","<6,12>","<6,13>","<6,14>","<7,0>","<7,1>","<7,2>","<7,3>","<7,4>","<7,5>","<7,6>","<7,7>","<7,8>","<7,9>","<7,10>","<7,11>","<7,12>","<7,13>","<7,14>","<8,0>","<8,1>","<8,2>","<8,3>","<8,4>","<8,5>","<8,6>","<8,7>","<8,8>","<8,9>","<8,10>","<8,11>","<8,12>","<8,13>","<8,14>","<9,0>","<9,1>","<9,2>","<9,3>","<9,4>","<9,5>","<9,6>","<9,7>","<9,8>","<9,9>","<9,10>","<9,11>","<9,12>","<9,13>","<9,14>","<10,0>","<10,1>","<10,2>","<10,3>","<10,4>","<10,5>","<10,6>","<10,7>","<10,8>","<10,9>","<10,10>","<10,11>","<10,12>","<10,13>","<10,14>","<11,0>","<11,1>","<11,2>","<11,3>","<11,4>","<11,5>","<11,6>","<11,7>","<11,8>","<11,9>","<11,10>","<11,11>","<11,12>","<11,13>","<11,14>","<12,0>","<12,1>","<12,2>","<12,3>","<12,4>","<12,5>","<12,6>","<12,7>","<12,8>","<12,9>","<12,10>","<12,11>","<12,12>","<12,13>","<12,14>","<13,0>","<13,1>","<13,2>","<13,3>","<13,4>","<13,5>","<13,6>","<13,7>","<13,8>","<13,9>","<13,10>","<13,11>","<13,12>","<13,13>","<13,14>","<14,0>","<14,1>","<14,2>","<14,3>","<14,4>","<14,5>","<14,6>","<14,7>","<14,8>","<14,9>","<14,10>","<14,11>","<14,12>","<14,13>","<14,14>"
         };
   BOOST_CHECK_EQUAL_COLLECTIONS(names.begin(), names.end(),
                                 expected_names.begin(), expected_names.end());

   IncidenceMatrix<CooType> I(names);
   I.append_translates_2d(tiles,
                          CooType { board_size, board_size });
   BOOST_CHECK_EQUAL(I.rows, 60480);
   //   std::vector<dancing_links::Solution> solutions = dancing_links::Algorithm_X(I);
   //   BOOST_CHECK_EQUAL(solutions.size(), (size_t) 212);
}

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

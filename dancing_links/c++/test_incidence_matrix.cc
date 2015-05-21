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

#include "incidence_matrix.h"

using namespace pentominos;
using namespace incidence_matrix;

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

BOOST_AUTO_TEST_CASE( constructor_test )
{
   IncidenceMatrix<CooType> I ({"0", "1", "2"});
   const std::vector<ColRepType> rep { I.representation() },
      expected { 
         // h(size), name, left,  right,     up,     down
         { {"r(0)", "root", "2",    "0",    "root", "root"} }, 
         { {"h(0)", "0",    "root", "1",    "0",    "0"} },
         { {"h(0)", "1",    "0",    "2",    "1",    "1"} },
         { {"h(0)", "2",    "1",    "root", "2",    "2"} }
      };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());
}

BOOST_FIXTURE_TEST_CASE( append_one_row, scott_example_fixture )
{
   I.append_row("I", { {0,0}, {0,1}, {0,2}, {0,3}, {0,4} } );
   std::vector<ColRepType> rep;
   for (const auto& i : { "I", "<0,0>", "<0,1>", "<0,2>", "<0,3>", "<0,4>" }) {
      rep.push_back(I.column_object_of_name[i]->representation());
   }
   std::vector<ColRepType> expected {
      {{"h(1)", "I", "F", "L", "I{0}", "I{0}"}, {"c", "I{0}", "I<0,4>", "I<0,0>", "I", "I" }}, 
      {{"h(1)", "<0,0>", "Z", "<0,1>", "I<0,0>", "I<0,0>"}, {"c", "I<0,0>", "I{0}", "I<0,1>", "<0,0>", "<0,0>" }}, 
      {{"h(1)", "<0,1>", "<0,0>", "<0,2>", "I<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I<0,0>", "I<0,2>", "<0,1>", "<0,1>" }}, 
      {{"h(1)", "<0,2>", "<0,1>", "<0,3>", "I<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "<0,2>", "<0,2>" }}, 
      {{"h(1)", "<0,3>", "<0,2>", "<0,4>", "I<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "<0,3>", "<0,3>" }}, 
      {{"h(1)", "<0,4>", "<0,3>", "<0,5>", "I<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I{0}", "<0,4>", "<0,4>" }}
   };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( append_two_rows, scott_example_fixture )
{
   I.append_row("I", { {0,0}, {0,1}, {0,2}, {0,3}, {0,4} } );
   I.append_row("I", { {0,1}, {0,2}, {0,3}, {0,4}, {0,5} } );
   std::vector<ColRepType> rep;
   for (const auto& i : { "I", "<0,0>", "<0,1>", "<0,2>", "<0,3>", "<0,4>" }) {
      rep.push_back(I.column_object_of_name[i]->representation());
   }
   std::vector<ColRepType> expected {
      {{"h(2)", "I", "F", "L", "I{1}", "I{0}"}, {"c", "I{0}", "I<0,4>", "I<0,0>", "I", "I{1}"}, {"c", "I{1}", "I<0,5>", "I<0,1>", "I{0}", "I"}},
      {{"h(1)", "<0,0>", "Z", "<0,1>", "I<0,0>", "I<0,0>"}, {"c", "I<0,0>", "I{0}", "I<0,1>", "<0,0>", "<0,0>" }}, 
      {{"h(2)", "<0,1>", "<0,0>", "<0,2>", "I<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I<0,0>", "I<0,2>", "<0,1>", "I<0,1>" }, {"c", "I<0,1>", "I{1}", "I<0,2>", "I<0,1>", "<0,1>"}}, 
      {{"h(2)", "<0,2>", "<0,1>", "<0,3>", "I<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "<0,2>", "I<0,2>" }, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "I<0,2>", "<0,2>" }}, 
      {{"h(2)", "<0,3>", "<0,2>", "<0,4>", "I<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "<0,3>", "I<0,3>" }, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "I<0,3>", "<0,3>" }}, 
      {{"h(2)", "<0,4>", "<0,3>", "<0,5>", "I<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I{0}", "<0,4>", "I<0,4>" }, {"c", "I<0,4>", "I<0,3>", "I<0,5>", "I<0,4>", "<0,4>" }}
   };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( append_allow_none, scott_example_fixture )
{
   I.append_translates_2d(std::array<Pentomino, 1> { Pentomino("I") },
                          CooType { 6, 3 },
                          [](const CooType&)->bool { return false; });
   BOOST_CHECK_EQUAL(I.rows, 0);
}

BOOST_FIXTURE_TEST_CASE( append_translates, scott_example_fixture )
{
   Pentomino P("I");
   I.append_translates_2d(std::array<Pentomino, 1> { Pentomino("I") },
                          CooType { 3, 6 });
   std::vector<ColRepType> rep;
   for (const auto& i : { "I", "<0,0>", "<0,1>", "<0,2>", "<0,3>", "<0,4>", "<0,5>", "<1,0>", "<1,1>", "<1,2>", "<1,3>", "<1,4>", "<1,5>", "<2,0>", "<2,1>", "<2,2>", "<2,3>", "<2,4>", "<2,5>" }) {
      rep.push_back(I.column_object_of_name[i]->representation());
   }

   std::vector<ColRepType> expected {
      {{"h(6)", "I", "F", "L", "I{5}", "I{0}"}, {"c", "I{0}", "I<0,4>", "I<0,0>", "I", "I{1}"}, {"c", "I{1}", "I<0,5>", "I<0,1>", "I{0}", "I{2}"}, {"c", "I{2}", "I<1,4>", "I<1,0>", "I{1}", "I{3}"}, {"c", "I{3}", "I<1,5>", "I<1,1>", "I{2}", "I{4}"}, {"c", "I{4}", "I<2,4>", "I<2,0>", "I{3}", "I{5}"}, {"c", "I{5}", "I<2,5>", "I<2,1>", "I{4}", "I"}}, 
      {{"h(1)", "<0,0>", "Z", "<0,1>", "I<0,0>", "I<0,0>"}, {"c", "I<0,0>", "I{0}", "I<0,1>", "<0,0>", "<0,0>"}}, 
      {{"h(2)", "<0,1>", "<0,0>", "<0,2>", "I<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I<0,0>", "I<0,2>", "<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I{1}", "I<0,2>", "I<0,1>", "<0,1>"}},
      {{"h(2)", "<0,2>", "<0,1>", "<0,3>", "I<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "I<0,2>", "<0,2>"}}, 
      {{"h(2)", "<0,3>", "<0,2>", "<0,4>", "I<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "I<0,3>", "<0,3>"}}, 
      {{"h(2)", "<0,4>", "<0,3>", "<0,5>", "I<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I{0}", "<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I<0,5>", "I<0,4>", "<0,4>"}},
      {{"h(1)", "<0,5>", "<0,4>", "<0,6>", "I<0,5>", "I<0,5>"}, {"c", "I<0,5>", "I<0,4>", "I{1}", "<0,5>", "<0,5>"}}, 
      {{"h(1)", "<1,0>", "<0,7>", "<1,1>", "I<1,0>", "I<1,0>"}, {"c", "I<1,0>", "I{2}", "I<1,1>", "<1,0>", "<1,0>"}}, 
      {{"h(2)", "<1,1>", "<1,0>", "<1,2>", "I<1,1>", "I<1,1>"}, {"c", "I<1,1>", "I<1,0>", "I<1,2>", "<1,1>", "I<1,1>"}, {"c", "I<1,1>", "I{3}", "I<1,2>", "I<1,1>", "<1,1>"}},
      {{"h(2)", "<1,2>", "<1,1>", "<1,3>", "I<1,2>", "I<1,2>"}, {"c", "I<1,2>", "I<1,1>", "I<1,3>", "<1,2>", "I<1,2>"}, {"c", "I<1,2>", "I<1,1>", "I<1,3>", "I<1,2>", "<1,2>"}}, 
      {{"h(2)", "<1,3>", "<1,2>", "<1,4>", "I<1,3>", "I<1,3>"}, {"c", "I<1,3>", "I<1,2>", "I<1,4>", "<1,3>", "I<1,3>"}, {"c", "I<1,3>", "I<1,2>", "I<1,4>", "I<1,3>", "<1,3>"}}, 
      {{"h(2)", "<1,4>", "<1,3>", "<1,5>", "I<1,4>", "I<1,4>"}, {"c", "I<1,4>", "I<1,3>", "I{2}", "<1,4>", "I<1,4>"}, {"c", "I<1,4>", "I<1,3>", "I<1,5>", "I<1,4>", "<1,4>"}},
      {{"h(1)", "<1,5>", "<1,4>", "<1,6>", "I<1,5>", "I<1,5>"}, {"c", "I<1,5>", "I<1,4>", "I{3}", "<1,5>", "<1,5>"}}, 
      {{"h(1)", "<2,0>", "<1,7>", "<2,1>", "I<2,0>", "I<2,0>"}, {"c", "I<2,0>", "I{4}", "I<2,1>", "<2,0>", "<2,0>"}}, 
      {{"h(2)", "<2,1>", "<2,0>", "<2,2>", "I<2,1>", "I<2,1>"}, {"c", "I<2,1>", "I<2,0>", "I<2,2>", "<2,1>", "I<2,1>"}, {"c", "I<2,1>", "I{5}", "I<2,2>", "I<2,1>", "<2,1>"}},
      {{"h(2)", "<2,2>", "<2,1>", "<2,3>", "I<2,2>", "I<2,2>"}, {"c", "I<2,2>", "I<2,1>", "I<2,3>", "<2,2>", "I<2,2>"}, {"c", "I<2,2>", "I<2,1>", "I<2,3>", "I<2,2>", "<2,2>"}}, 
      {{"h(2)", "<2,3>", "<2,2>", "<2,4>", "I<2,3>", "I<2,3>"}, {"c", "I<2,3>", "I<2,2>", "I<2,4>", "<2,3>", "I<2,3>"}, {"c", "I<2,3>", "I<2,2>", "I<2,4>", "I<2,3>", "<2,3>"}}, 
      {{"h(2)", "<2,4>", "<2,3>", "<2,5>", "I<2,4>", "I<2,4>"}, {"c", "I<2,4>", "I<2,3>", "I{4}", "<2,4>", "I<2,4>"}, {"c", "I<2,4>", "I<2,3>", "I<2,5>", "I<2,4>", "<2,4>"}},
      {{"h(1)", "<2,5>", "<2,4>", "<2,6>", "I<2,5>", "I<2,5>"}, {"c", "I<2,5>", "I<2,4>", "I{5}", "<2,5>", "<2,5>"}}
   };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( append_one_with_hole, scott_example_fixture )
{
   Pentomino P("I");
   P.translate_coo(1,3);
   I.append_translates_2d(std::array<Pentomino, 1> { Pentomino("I") },
                          CooType { 6, 4 },
                          allow_outside_hole);
   BOOST_CHECK_EQUAL(I.rows, 0);
}

BOOST_FIXTURE_TEST_CASE( append_with_hole, scott_example_fixture )
{
   const std::set<Pentomino> reps { all_fixed_pentominos() };
   I.append_translates_2d(reps,
                          CooType { 8, 8 },
                          allow_outside_hole);
   BOOST_CHECK_EQUAL(I.rows, 1568);
}

BOOST_FIXTURE_TEST_CASE( query_required_placements_1, scott_example_fixture )
{
   Pentomino P("I");
   P.translate_coo(0,3);
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { { P.name, { P.coos } } };
   std::vector<bool> allowed;
   for (const auto& coo : P.coos) {
      allowed.push_back(allow_outside_hole(coo));
   }
   const std::vector<bool> expected { true, true, true, false, false };
   BOOST_CHECK_EQUAL_COLLECTIONS(allowed.begin(), allowed.end(),
                                 expected.begin(), expected.end());
}

BOOST_FIXTURE_TEST_CASE( query_required_placements_2, scott_example_fixture )
{
   Pentomino P("I");
   P.translate_coo(0,3);
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { { P.name, { P.coos } } };
   BOOST_CHECK_EQUAL(I.is_legal(P.coos, allow_outside_hole, { 5, 5 }), false);
}

BOOST_FIXTURE_TEST_CASE( required_placements, scott_example_fixture )
{
   Pentomino P("I");
   P.translate_coo(0,3);
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { {P.name, { P.coos } } };
   BOOST_CHECK_THROW(I.append_translates_2d(std::array<Pentomino, 1> { P },
                                            CooType { 8, 8 },
                                            allow_outside_hole,
                                            required_placements), 
                     ForbiddenPlacementException);
}

BOOST_FIXTURE_TEST_CASE( append_translates_with_hole, scott_example_fixture )
{
   Pentomino P("I");
   I.append_translates_2d(std::array<Pentomino, 1> { P },
                          CooType { 3, 6 });
   std::vector<ColRepType> rep;
   for (const auto& i : { "I", "<0,0>", "<0,1>", "<0,2>", "<0,3>", "<0,4>", "<0,5>", "<1,0>", "<1,1>", "<1,2>", "<1,3>", "<1,4>", "<1,5>", "<2,0>", "<2,1>", "<2,2>", "<2,3>", "<2,4>", "<2,5>" }) {
      rep.push_back(I.column_object_of_name[i]->representation());
   }
   std::vector<ColRepType> expected {
      {{"h(6)", "I", "F", "L", "I{5}", "I{0}"}, {"c", "I{0}", "I<0,4>", "I<0,0>", "I", "I{1}"}, {"c", "I{1}", "I<0,5>", "I<0,1>", "I{0}", "I{2}"}, {"c", "I{2}", "I<1,4>", "I<1,0>", "I{1}", "I{3}"}, {"c", "I{3}", "I<1,5>", "I<1,1>", "I{2}", "I{4}"}, {"c", "I{4}", "I<2,4>", "I<2,0>", "I{3}", "I{5}"}, {"c", "I{5}", "I<2,5>", "I<2,1>", "I{4}", "I"}}, 
      {{"h(1)", "<0,0>", "Z", "<0,1>", "I<0,0>", "I<0,0>"}, {"c", "I<0,0>", "I{0}", "I<0,1>", "<0,0>", "<0,0>"}}, 
      {{"h(2)", "<0,1>", "<0,0>", "<0,2>", "I<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I<0,0>", "I<0,2>", "<0,1>", "I<0,1>"}, {"c", "I<0,1>", "I{1}", "I<0,2>", "I<0,1>", "<0,1>"}},
      {{"h(2)", "<0,2>", "<0,1>", "<0,3>", "I<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "<0,2>", "I<0,2>"}, {"c", "I<0,2>", "I<0,1>", "I<0,3>", "I<0,2>", "<0,2>"}}, 
      {{"h(2)", "<0,3>", "<0,2>", "<0,4>", "I<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "<0,3>", "I<0,3>"}, {"c", "I<0,3>", "I<0,2>", "I<0,4>", "I<0,3>", "<0,3>"}}, 
      {{"h(2)", "<0,4>", "<0,3>", "<0,5>", "I<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I{0}", "<0,4>", "I<0,4>"}, {"c", "I<0,4>", "I<0,3>", "I<0,5>", "I<0,4>", "<0,4>"}},
      {{"h(1)", "<0,5>", "<0,4>", "<0,6>", "I<0,5>", "I<0,5>"}, {"c", "I<0,5>", "I<0,4>", "I{1}", "<0,5>", "<0,5>"}}, 
      {{"h(1)", "<1,0>", "<0,7>", "<1,1>", "I<1,0>", "I<1,0>"}, {"c", "I<1,0>", "I{2}", "I<1,1>", "<1,0>", "<1,0>"}}, 
      {{"h(2)", "<1,1>", "<1,0>", "<1,2>", "I<1,1>", "I<1,1>"}, {"c", "I<1,1>", "I<1,0>", "I<1,2>", "<1,1>", "I<1,1>"}, {"c", "I<1,1>", "I{3}", "I<1,2>", "I<1,1>", "<1,1>"}},
      {{"h(2)", "<1,2>", "<1,1>", "<1,3>", "I<1,2>", "I<1,2>"}, {"c", "I<1,2>", "I<1,1>", "I<1,3>", "<1,2>", "I<1,2>"}, {"c", "I<1,2>", "I<1,1>", "I<1,3>", "I<1,2>", "<1,2>"}}, 
      {{"h(2)", "<1,3>", "<1,2>", "<1,4>", "I<1,3>", "I<1,3>"}, {"c", "I<1,3>", "I<1,2>", "I<1,4>", "<1,3>", "I<1,3>"}, {"c", "I<1,3>", "I<1,2>", "I<1,4>", "I<1,3>", "<1,3>"}}, 
      {{"h(2)", "<1,4>", "<1,3>", "<1,5>", "I<1,4>", "I<1,4>"}, {"c", "I<1,4>", "I<1,3>", "I{2}", "<1,4>", "I<1,4>"}, {"c", "I<1,4>", "I<1,3>", "I<1,5>", "I<1,4>", "<1,4>"}},
      {{"h(1)", "<1,5>", "<1,4>", "<1,6>", "I<1,5>", "I<1,5>"}, {"c", "I<1,5>", "I<1,4>", "I{3}", "<1,5>", "<1,5>"}}, 
      {{"h(1)", "<2,0>", "<1,7>", "<2,1>", "I<2,0>", "I<2,0>"}, {"c", "I<2,0>", "I{4}", "I<2,1>", "<2,0>", "<2,0>"}}, 
      {{"h(2)", "<2,1>", "<2,0>", "<2,2>", "I<2,1>", "I<2,1>"}, {"c", "I<2,1>", "I<2,0>", "I<2,2>", "<2,1>", "I<2,1>"}, {"c", "I<2,1>", "I{5}", "I<2,2>", "I<2,1>", "<2,1>"}},
      {{"h(2)", "<2,2>", "<2,1>", "<2,3>", "I<2,2>", "I<2,2>"}, {"c", "I<2,2>", "I<2,1>", "I<2,3>", "<2,2>", "I<2,2>"}, {"c", "I<2,2>", "I<2,1>", "I<2,3>", "I<2,2>", "<2,2>"}}, 
      {{"h(2)", "<2,3>", "<2,2>", "<2,4>", "I<2,3>", "I<2,3>"}, {"c", "I<2,3>", "I<2,2>", "I<2,4>", "<2,3>", "I<2,3>"}, {"c", "I<2,3>", "I<2,2>", "I<2,4>", "I<2,3>", "<2,3>"}}, 
      {{"h(2)", "<2,4>", "<2,3>", "<2,5>", "I<2,4>", "I<2,4>"}, {"c", "I<2,4>", "I<2,3>", "I{4}", "<2,4>", "I<2,4>"}, {"c", "I<2,4>", "I<2,3>", "I<2,5>", "I<2,4>", "<2,4>"}},
      {{"h(1)", "<2,5>", "<2,4>", "<2,6>", "I<2,5>", "I<2,5>"}, {"c", "I<2,5>", "I<2,4>", "I{5}", "<2,5>", "<2,5>"}}
   };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());
}

BOOST_FIXTURE_TEST_CASE( restricted_scott_construction, scott_example_fixture )
{
   const std::set<Pentomino> reps { all_fixed_pentominos() };
   Pentomino P("X");
   P.translate_by({ 0, 1 });
   const IncidenceMatrix<CooType>::RequiredPlacementType required_placements { { P.name, { P.coos } } };
   I.append_translates_2d(reps,
                          CooType { 8, 8 },
                          allow_outside_hole,
                          required_placements);
   BOOST_CHECK_EQUAL(I.rows, 1545);
}

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

BOOST_FIXTURE_TEST_CASE( construct_running_example, running_example_fixture )
{
   const std::vector<ColRepType> 
      rep { I.representation() },
      expected {
      {{"r(0)", "root", "G", "A", "root", "root"}}, 
      {{"h(2)", "A", "root", "B", "A{1}", "A{0}"}, {"c", "A{0}", "AG", "AD", "A", "A{1}"}, {"c", "A{1}", "AD", "AD", "A{0}", "A"}},
      {{"h(2)", "B", "A", "C", "B{1}", "B{0}"}, {"c", "B{0}", "BF", "BC", "B", "B{1}"}, {"c", "B{1}", "BG", "BG", "B{0}", "B"}}, 
      {{"h(2)", "C", "B", "D", "BC", "C{0}"}, {"c", "C{0}", "CF", "CE", "C", "BC"}, {"c", "BC", "B{0}", "BF", "C{0}", "C"}}, 
      {{"h(3)", "D", "C", "E", "D{0}", "AD"}, {"c", "AD", "A{0}", "AG", "D", "AD"}, {"c", "AD", "A{1}", "A{1}", "AD", "D{0}"}, {"c", "D{0}", "DG", "DE", "AD", "D"}}, 
      {{"h(2)", "E", "D", "F", "DE", "CE"}, {"c", "CE", "C{0}", "CF", "E", "DE"}, {"c", "DE", "D{0}", "DG", "CE", "E"}}, 
      {{"h(2)", "F", "E", "G", "BF", "CF"}, {"c", "CF", "CE", "C{0}", "F", "BF"}, {"c", "BF", "BC", "B{0}", "CF", "F"}}, 
      {{"h(3)", "G", "F", "root", "DG", "AG"}, {"c", "AG", "AD", "A{0}", "G", "BG"}, {"c", "BG", "B{1}", "B{1}", "AG", "DG"}, {"c", "DG", "DE", "D{0}", "BG", "G"}}
   };
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( cover_running_example, running_example_fixture )
{
   I.cover_column(I.column_object_of_name["A"]);
   const std::vector<ColRepType> 
      rep { I.representation() },
      expected {
        {{"r(0)", "root", "G", "B", "root", "root"}}, 
        {{"h(2)", "B", "root", "C", "B{1}", "B{0}"},{"c", "B{0}", "BF", "BC", "B", "B{1}"},{"c", "B{1}", "BG", "BG", "B{0}", "B"}}, 
        {{"h(2)", "C", "B", "D", "BC", "C{0}"}, {"c", "C{0}", "CF", "CE", "C", "BC"}, {"c", "BC", "B{0}", "BF", "C{0}", "C"}}, 
        {{"h(1)", "D", "C", "E", "D{0}", "D{0}"}, {"c", "D{0}", "DG", "DE", "D", "D"}}, 
        {{"h(2)", "E", "D", "F", "DE", "CE"}, {"c", "CE", "C{0}", "CF", "E", "DE"}, {"c", "DE", "D{0}", "DG", "CE", "E"}}, 
        {{"h(2)", "F", "E", "G", "BF", "CF"}, {"c", "CF", "CE", "C{0}", "F", "BF"}, {"c", "BF", "BC", "B{0}", "CF", "F"}}, 
        {{"h(2)", "G", "F", "root", "DG", "BG"}, {"c", "BG", "B{1}", "B{1}", "G", "DG"}, {"c", "DG", "DE", "D{0}", "BG", "G"}}
      };
      BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                    expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( cover_and_uncover_running_example, running_example_fixture )
{
   const auto expected = I.representation();
   I.cover_column(I.column_object_of_name["A"]);
   I.uncover_column(I.column_object_of_name["A"]);
   const auto rep = I.representation();
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_FIXTURE_TEST_CASE( cover_3_running_example, running_example_fixture )
{
   for (const auto& n : { "A", "D", "G" }) {
      I.cover_column(I.column_object_of_name[n]);      
   }
   const std::vector<ColRepType> 
      rep { I.representation() },
      expected {
         {{"r(0)", "root", "F", "B", "root", "root"}}, 
         {{"h(1)", "B", "root", "C", "B{0}", "B{0}"}, {"c", "B{0}", "BF", "BC", "B", "B"}},
         {{"h(2)", "C", "B", "E", "BC", "C{0}"}, {"c", "C{0}", "CF", "CE", "C", "BC"}, {"c", "BC", "B{0}", "BF", "C{0}", "C"}}, 
         {{"h(1)", "E", "C", "F", "CE", "CE"}, {"c", "CE", "C{0}", "CF", "E", "E"}}, 
         {{"h(2)", "F", "E", "root", "BF", "CF"}, {"c", "CF", "CE", "C{0}", "F", "BF"}, {"c", "BF", "BC", "B{0}", "CF", "F"}}
      };
      BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                    expected.begin(), expected.end());   
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

   const std::vector<ColRepType> 
      rep { I.representation() },
      expected {
         {{"r(0)", "root", "<1,1>", "S", "root", "root"}},
         {{"h(1)", "S", "root", "<0,0>", "S{0}", "S{0}"}, {"c", "S{0}", "S<1,1>", "S<0,0>", "S", "S"}},
         {{"h(1)", "<0,0>", "S", "<0,1>", "S<0,0>", "S<0,0>"}, {"c", "S<0,0>", "S{0}", "S<0,1>", "<0,0>", "<0,0>"}},
         {{"h(1)", "<0,1>", "<0,0>", "<1,0>", "S<0,1>", "S<0,1>"}, {"c", "S<0,1>", "S<0,0>", "S<1,0>", "<0,1>", "<0,1>"}},
         {{"h(1)", "<1,0>", "<0,1>", "<1,1>", "S<1,0>", "S<1,0>"}, {"c", "S<1,0>", "S<0,1>", "S<1,1>", "<1,0>", "<1,0>"}},
         {{"h(1)", "<1,1>", "<1,0>", "root", "S<1,1>", "S<1,1>"}, {"c", "S<1,1>", "S<1,0>", "S{0}", "<1,1>", "<1,1>"}}
      };
      BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                    expected.begin(), expected.end());   
}

BOOST_AUTO_TEST_CASE( chess_square_row_rep )
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

   const std::vector<RowRepType>
      rep { I.row_representation() },
      expected {{"S{0}","<0,0>","<0,1>","<1,0>","<1,1>"}};
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_AUTO_TEST_CASE( chess_square_2_row_rep )
{
   const std::set<Pentomino> tiles { Pentomino("S", { {0,0}, {0,1}, {1,0}, {1,1} }) };
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
   BOOST_CHECK_EQUAL(I.rows, 9);
   const std::vector<RowRepType>
      rep { I.row_representation() },
      expected {{{"S{0}", "<0,0>", "<0,1>", "<1,0>", "<1,1>"}, {"S{1}", "<0,1>", "<0,2>", "<1,1>", "<1,2>"}, {"S{2}", "<0,2>", "<0,3>", "<1,2>", "<1,3>"}, {"S{3}", "<1,0>", "<1,1>", "<2,0>", "<2,1>"}, {"S{4}", "<1,1>", "<1,2>", "<2,1>", "<2,2>"}, {"S{5}", "<1,2>", "<1,3>", "<2,2>", "<2,3>"}, {"S{6}", "<2,0>", "<2,1>", "<3,0>", "<3,1>"}, {"S{7}", "<2,1>", "<2,2>", "<3,1>", "<3,2>"}, {"S{8}", "<2,2>", "<2,3>", "<3,2>", "<3,3>"}}};
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}

BOOST_AUTO_TEST_CASE( chess_4_square_with_dummy_copy )
{
   const std::set<Pentomino> tiles { 
      Pentomino("Sa", { {0,0}, {0,1}, {1,0}, {1,1} }), 
      Pentomino("Sb", { {0,0}, {0,1}, {1,0}, {1,1} }) };
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
   BOOST_CHECK_EQUAL(I.rows, 18);
   const std::vector<RowRepType>
      rep { I.row_representation() },
      expected {{"Sa{0}", "<0,0>", "<0,1>", "<1,0>", "<1,1>"}, {"Sa{1}", "<0,1>", "<0,2>", "<1,1>", "<1,2>"}, {"Sa{2}", "<0,2>", "<0,3>", "<1,2>", "<1,3>"}, {"Sa{3}", "<1,0>", "<1,1>", "<2,0>", "<2,1>"}, {"Sa{4}", "<1,1>", "<1,2>", "<2,1>", "<2,2>"}, {"Sa{5}", "<1,2>", "<1,3>", "<2,2>", "<2,3>"}, {"Sa{6}", "<2,0>", "<2,1>", "<3,0>", "<3,1>"}, {"Sa{7}", "<2,1>", "<2,2>", "<3,1>", "<3,2>"}, {"Sa{8}", "<2,2>", "<2,3>", "<3,2>", "<3,3>"}, {"Sb{0}", "<0,0>", "<0,1>", "<1,0>", "<1,1>"}, {"Sb{1}", "<0,1>", "<0,2>", "<1,1>", "<1,2>"}, {"Sb{2}", "<0,2>", "<0,3>", "<1,2>", "<1,3>"}, {"Sb{3}", "<1,0>", "<1,1>", "<2,0>", "<2,1>"}, {"Sb{4}", "<1,1>", "<1,2>", "<2,1>", "<2,2>"}, {"Sb{5}", "<1,2>", "<1,3>", "<2,2>", "<2,3>"}, {"Sb{6}", "<2,0>", "<2,1>", "<3,0>", "<3,1>"}, {"Sb{7}", "<2,1>", "<2,2>", "<3,1>", "<3,2>"}, {"Sb{8}", "<2,2>", "<2,3>", "<3,2>", "<3,3>"}};
   BOOST_CHECK_EQUAL_COLLECTIONS(rep.begin(), rep.end(),
                                 expected.begin(), expected.end());   
}




// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

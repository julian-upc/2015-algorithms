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

#define BOOST_TEST_MODULE orbits
#include <boost/test/included/unit_test.hpp>

#include "orbit.h"
#include "stl_wrappers.h"

BOOST_AUTO_TEST_CASE( generators )
{
   std::ostringstream oss;
   oss << simple_roots_type_A(4) << std::endl
       << simple_roots_type_B(4) << std::endl
       << simple_roots_type_C(4) << std::endl
       << simple_roots_type_D(4) << std::endl
       << simple_roots_type_E6() << std::endl
       << simple_roots_type_E7() << std::endl
       << simple_roots_type_E8() << std::endl
       << simple_roots_type_F4() << std::endl
       << simple_roots_type_H3() << std::endl
       << simple_roots_type_H4() << std::endl;

   BOOST_CHECK_EQUAL(oss.str(), 
                     "{{1,-1,0,0,0},{0,1,-1,0,0},{0,0,1,-1,0},{0,0,0,1,-1}}\n"
                     "{{1,-1,0,0},{0,1,-1,0},{0,0,1,-1},{0,0,0,1}}\n"
                     "{{1,-1,0,0},{0,1,-1,0},{0,0,1,-1},{0,0,0,2}}\n"
                     "{{1,-1,0,0},{0,1,-1,0},{0,0,1,-1},{0,0,1,1}}\n"
                     "{{1,-1,0,0,0,0},{0,1,-1,0,0,0},{0,0,1,-1,0,0},{0,0,0,1,-1,0},{0,0,0,1,1,0},{-0.5,-0.5,-0.5,-0.5,-0.5,0.866025}}\n"
                     "{{1,-1,0,0,0,0,0},{0,1,-1,0,0,0,0},{0,0,1,-1,0,0,0},{0,0,0,1,-1,0,0},{0,0,0,0,1,-1,0},{0,0,0,0,1,1,0},{-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,0.707107}}\n"
                     "{{1,-1,0,0,0,0,0,0},{0,1,-1,0,0,0,0,0},{0,0,1,-1,0,0,0,0},{0,0,0,1,-1,0,0,0},{0,0,0,0,1,-1,0,0},{0,0,0,0,0,1,-1,0},{0,0,0,0,0,1,1,0},{-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5}}\n"
                     "{{1,-1,0,0},{0,1,-1,0},{0,0,1,0},{-0.5,-0.5,-0.5,-0.5}}\n"
                     "{{2,0,0},{-1.61803,0.618034,-1},{0,0,2}}\n"
                     "{{1.30902,-0.309017,-0.309017,-0.309017},{-1,1,0,0},{0,-1,1,0},{0,0,-1,1}}\n"
                     );
}

struct b3_fixture {
  b3_fixture() 
    : generators(simple_roots('B', 3)) 
  {}
  GeneratorList generators;
};

BOOST_FIXTURE_TEST_CASE( b3_orbit_012, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 2, 3}).size(), (size_t) 48);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_12, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 1, 3}).size(), (size_t) 24);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_02, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 2, 2}).size(), (size_t) 24);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_01, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 2, 0}).size(), (size_t) 24);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_0, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 0, 0}).size(), (size_t) 6);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_1, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 1, 0}).size(), (size_t) 12);
}

BOOST_FIXTURE_TEST_CASE( b3_orbit_2, b3_fixture )
{
  BOOST_CHECK_EQUAL(orbit(generators, {1, 1, 1}).size(), (size_t) 8);
}


// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

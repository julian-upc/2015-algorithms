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

#define BOOST_TEST_MODULE dancing_links
#include <boost/test/included/unit_test.hpp>
#include <map>
#include <set>
#include "pentominos.h"
#include "boost_cout_wrappers.h"


BOOST_AUTO_TEST_SUITE( pentominos )

#include "test_pentominos.cc"

BOOST_AUTO_TEST_SUITE_END()

BOOST_AUTO_TEST_SUITE( incidence_matrix )

#include "test_incidence_matrix.cc"

BOOST_AUTO_TEST_SUITE_END()

BOOST_AUTO_TEST_SUITE( dancing_links )

#include "test_algorithm_x.cc"

BOOST_AUTO_TEST_SUITE_END()


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

//#define BOOST_TEST_MODULE orbits
//#include <boost/test/included/unit_test.hpp>

#include <time.h>
#include <stdio.h>
#include "orbit.h"

/*
struct b3_fixture {
  b3_fixture() 
    : generators(simple_roots('B', 3)) 
  {}
  GeneratorList generators;
};
*/
//int main( int size, int[] args )
int main()
{
	time_t start,end;
	FILE* outfile = fopen ("coxeter_neosonea.out","w");

	fprintf( outfile, "B3 tests: (bools)\n" );
	time (&start);
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 2, 3}).size() == (size_t) 48 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 1, 3}).size() == (size_t) 24 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 2, 2}).size() == (size_t) 24 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 2, 0}).size() == (size_t) 24 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 0, 0}).size() == (size_t) 6 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 1, 0}).size() == (size_t) 12 );
	fprintf( outfile, " %d", orbit(simple_roots('B', 3), {1, 1, 1}).size() == (size_t) 8 );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "B4 tests:\n" );
	time (&start);
	fprintf( outfile, "384 %d", orbit(simple_roots('B', 4), {1, 2, 3, 4}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "B5 tests:\n" );
	time (&start);
	fprintf( outfile, "3840 %d", orbit(simple_roots('B', 5), {1, 2, 3, 4, 5}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "B6 tests:\n" );
	time (&start);
	fprintf( outfile, "46080 %d", orbit(simple_roots('B', 6), {1, 2, 3, 4, 5, 6}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "B7 tests:\n" );
	time (&start);
	fprintf( outfile, "645120 %d", orbit(simple_roots('B', 7), {1, 2, 3, 4, 5, 6, 7}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	/*fprintf( outfile, "B8 tests:\n" );
	time (&start);
	fprintf( outfile, "10321920 %d", orbit(simple_roots('B', 8), {1, 2, 3, 4, 5, 6, 7, 8}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );
*/
	fprintf( outfile, "E6 tests:\n" );
	time (&start);
	fprintf( outfile, "51840 %d", orbit(simple_roots('E', 6), {0, 0, 0, 0, 0, 0}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "E7 tests:\n" );
	time (&start);
	fprintf( outfile, "2903040 %d", orbit(simple_roots('E', 7), {0, 0, 0, 0, 0, 0, 0}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "F4 tests:\n" );
	time (&start);
	fprintf( outfile, "1152 %d", orbit(simple_roots('F', 4), {1, 2, 3, 4}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fprintf( outfile, "H4 tests:\n" );
	time (&start);
	fprintf( outfile, "14400 %d", orbit(simple_roots('H', 4), {0, 0, 0, 0}).size() );
	time (&end);
	fprintf( outfile, "\n(in %.3lf sec)\n\n", difftime(end,start) );

	fclose(outfile);
}

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

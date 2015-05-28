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

#ifndef __ORBIT_H_
#define __ORBIT_H_

#include <vector>
#include <numeric>
#include <set>
#include <math.h>

class NotImplementedException : public std::exception {};

typedef double NumberType;  // this probably isn't going to work
typedef std::vector<NumberType> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;
//class Orbit : std::set<VectorType>{
//	bool operator<(const Orbit& other) const {
		//Pento: return coos < other.coos || name < other.name;
//		return this. < other.;
//	}
//};


GeneratorList simple_roots(char type, int dim)
{
	if (dim <= 1) throw new std::exception();//"dim has to be larger than 1");
	const float PI = 3.14159265359;
	switch(type) {
		case 'a':
		case 'A':{
			GeneratorList gens (dim, VectorType (dim+1, 0));
			for( int i=0; i < dim; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
			}
			return gens;
			}
		case 'b':
		case 'c':
		case 'C':
		case 'B':{
			GeneratorList gens (dim, VectorType (dim, 0));
			for( int i=0; i < dim-1; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
			}
			gens[dim-1][dim-1] = 1;
			return gens;
			}
		case 'd':
		case 'D':{
			GeneratorList gens (dim, VectorType (dim, 0));
			for( int i=0; i < dim-1; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
			}
			gens[dim-1][dim-1] = 1;
			gens[dim-1][dim-2] = 1;
			return gens;
			}
		case 'e':
		case 'E':{
			if (dim < 6 || dim > 8) throw new std::exception();
			GeneratorList gens (dim, VectorType (dim, 0));
			const double a = -2. - sqrt(3);
			for( int i=0; i < dim-1; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
				gens[dim-1][i] = i < 3? a : 1;
			}
			gens[dim-1][dim-1] = 1;
			return gens;
			}
		case 'f':
		case 'F':
			if (dim != 4) throw new NotImplementedException();
			return { {1,-1,0,0}, {0,1,-1,0}, {0,0,1,-1}, {-1,-1,-1,-1} };
		case 'g':
		case 'G':
			if (dim != 2) throw new NotImplementedException();
			return { {1,0}, {1,-1} };
		case 'h':
		case 'H':{//TODO
			if (dim < 2 || dim > 4) throw new std::exception();
			GeneratorList gens (dim, VectorType (dim, 0));
			const double a = -2. - sqrt(3);
			for( int i=0; i < dim-1; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
			}
			gens[dim-1][dim-1] = a;
			return gens;
			}
		case 'i':
		case 'I':{
			GeneratorList gens (2, VectorType (dim, 0));
			for( int i=0; i < dim-1; i++ ){
				gens[0][0] = 1;
				gens[1][0] = -cos(PI/dim);
				gens[1][1] = sin(PI/dim);
			}
			return gens;
			}

		default:
			throw new NotImplementedException();
	}
}

VectorType times( double factor, VectorType& vector ){
	VectorType result(vector);
	for( int i=0; i < vector.size(); i++ )
		result[i] *= factor;
	return result;
}
double scalar_prod( VectorType& vector1, VectorType& vector2 ){
	double sum = 0;
	for( int i=0; i < vector1.size(); i++ )
		sum += vector1[i] * vector2[i];
	return sum;
}
VectorType add( VectorType& vector1, VectorType& vector2 ){
	VectorType sum(vector1);
	for( int i=0; i < vector1.size(); i++ )
		sum[i] += vector2[i];
	return sum;
}

Orbit orbit(const GeneratorList& generators, const VectorType& v)
{
	if ( v.size() != generators[0].size() ) throw new NotImplementedException();
	Orbit mapped;
	mapped.insert(v);
	for( const auto& g : generators ){
		//mapped.insert( times( -2. * (*scalar_prod(g,v)), g)  );
	}
	return mapped;
}


#endif // __ORBIT_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

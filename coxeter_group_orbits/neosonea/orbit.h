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

#include <stdio.h>
#include <vector>
#include <numeric>
#include <set>
#include <list>
#include <queue>
#include <math.h>
//#include <stl_wrappers.h>

class NotImplementedException : public std::exception {};

const double eps = 10e-100;

typedef double NumberType;  // this probably isn't going to work
/*class NumberType
{
	private:
		double value;
	public:
	bool operator<(const NumberType& other) const override
	{		//Pento: return coos < other.coos || name < other.name;
		return abs( this - other ) < 0;
	}
};*/

typedef std::vector<NumberType> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;

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
			const double a = -2. - sqrt(3);//???
			for( int i=0; i < dim-1; i++ ){
				gens[i][i] = 1;
				gens[i][i+1] = -1;
				gens[dim-1][i] = 1;
			}
			gens[dim-1][dim-1] = a;
			return gens;
			}
		case 'i':
		case 'I':{
			GeneratorList gens (2, VectorType (dim, 0));
			gens[0][0] = 1;
			gens[1][0] = -cos(PI/dim);
			gens[1][1] = sin(PI/dim);
			return gens;
			}

		default:
			throw new NotImplementedException();
	}
}

VectorType times( double factor, const VectorType& vector ){
	VectorType result(vector);
	for( unsigned int i=0; i < vector.size(); i++ )
		result[i] *= factor;
	return result;
}
double operator *( const VectorType& vector1, const VectorType& vector2 ){
	double sum = 0;
	for( unsigned int i=0; i < vector1.size(); i++ )
		sum += vector1[i] * vector2[i];
	return sum;
}
VectorType operator +( const VectorType& vector1, const VectorType& vector2 ){
	VectorType sum(vector1);
	for( unsigned int i=0; i < vector1.size(); i++ )
		sum[i] += vector2[i];
	return sum;
}

void rec( const int i, const GeneratorList& gens, Orbit& orbit, Orbit& orbit_i ){
	if( i == 0 ) return;
	Orbit orbit_i1;
	for( const auto& g : gens ){
		for( const auto& v : orbit_i ){
			orbit.insert( v + times( -2.*(g*v)/(g*g), g ) );
			orbit_i1.insert( v + times( -2.*(g*v)/(g*g), g ) );
			rec( i-1, gens, orbit, orbit_i1 );
		}
	}
}

Orbit orbit_rec(const GeneratorList& generators, const VectorType& v)
{
	if ( v.size() != generators[0].size() ) throw new NotImplementedException();
	Orbit mapped;
	Orbit orbit_i0;
	mapped.insert(v);
	orbit_i0.insert(v);
	rec( 7, generators, mapped, orbit_i0 );
	printf("\n\n\n %i",mapped.size());
	for( const auto& m : mapped ){
		printf("\n\t %i  {%f,%f,%f}",m.size(), m[0],m[1],m[2]);
	}
	return mapped;
}

Orbit orbit(const GeneratorList& generators, const VectorType& v)
{
	if ( v.size() != generators[0].size() ) throw new NotImplementedException();
	Orbit orbit;
	orbit.insert(v);

	std::queue<VectorType,std::deque<VectorType> > queue;
	queue.push(v);

	VectorType curr;
	VectorType refl;

	while( ! queue.empty() )
	{
		curr = queue.front();
		queue.pop();

		for( const auto g : generators )
		{
			refl = curr + times( -2.*(g*curr)/(g*g), g );
			//insert returns std::pair<iterator,bool>
			if( orbit.insert(refl).second ){
				queue.push(refl);
			}
		}
	}
	return orbit;
}


#endif // __ORBIT_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

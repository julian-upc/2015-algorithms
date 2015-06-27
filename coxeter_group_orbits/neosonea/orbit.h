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

//#include <stdio.h>
#include <vector>
#include <queue>
#include "generators.h"
#include "types.h"
//#include <stl_wrappers.h>


VectorType times( const double factor, const VectorType& vector ){
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
//quicker
VectorType reflect( const VectorType& v, const VectorType& g )
{
	double gv = 0;
	double gg = 0;
	for( unsigned int i=0; i < v.size(); i++ )
	{
		gv += g[i] * v[i];
		gg += g[i] * g[i];
	}
	NumberType factor = -2.*gv/gg;
	VectorType sum(v);
	for( unsigned int i=0; i < v.size(); i++ )
		sum[i] += factor*g[i];
	return sum;
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
		//printf("\n%i", orbit.size());
		curr = queue.front();
		queue.pop();

		for( const auto g : generators )
		{
			refl = reflect(curr, g);
			//insert returns std::pair<iterator,bool>
			if( orbit.insert(refl).second )
				queue.push(refl);
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

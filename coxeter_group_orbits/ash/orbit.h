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
#include <set>

class NotImplementedException : public std::exception {};

typedef int NumberType;  // this probably isn't going to work
typedef std::vector<NumberType> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;

GeneratorList simple_roots(char type, int dim)
{
   switch(type) {
   case 'b':
   case 'B':
      if (dim != 3) throw new NotImplementedException();
      return {{1,-1,0},{0,1,-1},{0,0,1}};

   default:
      throw new NotImplementedException();
   }
}

Orbit orbit(const GeneratorList& generators, const VectorType& v)
{
   return std::set<VectorType>();
}


#endif // __ORBIT_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

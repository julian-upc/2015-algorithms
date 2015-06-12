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

#ifndef __TYPES_H_
#define __TYPES_H_

#include <set>
#include <vector>

class NotImplementedException : public std::exception {};
class InvalidGroupException : public std::exception {};

typedef long double NumberType;  // this might work
typedef std::vector<NumberType> VectorType;
typedef std::set<VectorType> Orbit;

class GeneratorList : public std::vector<VectorType> {
public:
   GeneratorList(int r, int c) 
      : std::vector<VectorType>(r)
   {
      for (int i=0; i<r; ++i)
         (*this)[i] = VectorType(c);
   }

   NumberType& operator ()(int i, int j) {
      return (*this)[i][j];
   }

   const NumberType& operator ()(int i, int j) const {
      return (*this)[i][j];
   }
};


#endif // __TYPES_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

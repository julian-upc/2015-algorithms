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
/*
class ImpreciseVector : std::vector<NumberType>
{
   ImpreciseVector(){}

   friend bool operator <(const ImpreciseVector& v1, const ImpreciseVector& v2 ){
      float epsilon = 0.00001;
      std::vector<T> tmp (v1);

      for (std::vector<int>::size_type i = 0; i != tmp.size(); i++){
         tmp[i] -= v2[i];
      }

      if((std::inner_product(begin(tmp), end(tmp), begin(tmp), 0.0) / (std::inner_product(begin(v1), end(v1), begin(v1), 0.0) * std::inner_product(begin(v2), end(v2), begin(v2), 0.0))) < epsilon) 
         return false;
      else
         return static_cast<std::vector<T>>(v1) < static_cast<std::vector<T>>(v2);
   }
};
*/
#endif // __TYPES_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

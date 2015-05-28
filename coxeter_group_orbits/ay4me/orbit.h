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
#include <fstream>
#include <string>

class NotImplementedException : public std::exception {};
class InvalidInputException : public std::exception {};

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

Void input(std::string filename,bool outputOrbit)
{
   std::ifstream input( filename );
   std::string line; 
   getline( input, line );
   if(line.length() != 2)
   {
      throw new InvalidInputException();
   }
   char letter = line[0]
   int number = int(line[1])
   switch(letter) { // because switch doesn't work on strings
      case 'A':
         coos = {{0,1},{1,0},{1,1},{1,2},{2,2}}; break;
      case 'B':
         coos = {{0,0},{0,1},{0,2},{0,3},{0,4}}; break;
      case 'D':
         coos = {{0,0},{0,1},{0,2},{0,3},{1,0}}; break;
      case 'E':
         coos = {{0,0},{0,1},{1,1},{1,2},{1,3}}; break;
      case 'F':
         coos = {{0,0},{0,1},{0,2},{1,1},{1,2}}; break;
      case 'G':
         coos = {{0,2},{1,0},{1,1},{1,2},{2,2}}; break;
      case 'H':
         coos = {{0,0},{0,1},{1,0},{2,0},{2,1}}; break;
      case 'I':
         coos = {{0,0},{1,0},{2,0},{2,1},{2,2}}; break;
      default:
         throw new InvalidInputException();
      }
   //process first line
   getline( input, line );
   //process second line
}



Orbit orbit(const GeneratorList& generators, const VectorType& v)
{
   return std::set<VectorType>();
}

Orbit recorbit(const GeneratorList& generators, const VectorType& v, int k)
{
   if (k==0)
   {
      return {};
   }  
   else
   {
      Orbit newVectors std::set<VectorType>();
      newVectors.add(v);
      for(const auto& plane : generators)
      {
         newVectors.add(recorbit(generators,mirror(v,plane),k-1));
      }
      return newVectors;
   }
}

VectorType mirror(const VectorType& v, VectorType generators)
{

}


#endif // __ORBIT_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

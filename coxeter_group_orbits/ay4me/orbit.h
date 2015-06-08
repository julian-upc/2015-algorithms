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
#include <sstream>
#include <iostream>
#include <string>
#include <numeric>
#include <boost/lexical_cast.hpp>

class NotImplementedException : public std::exception {};
class InvalidInputException : public std::logic_error {
public:
  InvalidInputException():std::logic_error("no error message") {};
  InvalidInputException(const std::string& s):std::logic_error(s) {};
};

typedef int NumberType;  // this probably isn't going to work
typedef std::vector<NumberType> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;

void out(std::ostream& file,const Orbit& solution, bool outputOrbit);

GeneratorList simple_roots(char type, std::size_t dim)
{
   switch(type) {
   case 'b':
   case 'B':
      if (dim != 3) throw NotImplementedException();
      return {{1,-1,0},{0,1,-1},{0,0,1}};

   default:
      throw NotImplementedException();
   }
}

void generateA(std::size_t dim, GeneratorList& generators)
{
  generators.resize(dim, VectorType(dim+1));
  for (std::size_t i=0; i<dim; ++i)
  {
    for (std::size_t j=0; j<dim+1; ++j)
    {
      if (i == j)
      {
        generators[i][j] = 1;
      }
      else if (i+1 == j)
      {
        generators[i][j] = -1;
      }
      else
      {
        generators[i][j] = 0;
      }
    }
  }
}

void generateB(std::size_t dim, GeneratorList& generators)
{
  generators.resize(dim, VectorType(dim));
  for (std::size_t i=0; i<dim; ++i)
  {
    for (std::size_t j=0; j<dim; ++j)
    {
      if (i == j)
      {
        generators[i][j] = 1;
      }
      else if (i+1 == j)
      {
        generators[i][j] = -1;
      }
      else
      {
        generators[i][j] = 0;
      }
    }
  }
}

void generateD(std::size_t dim, GeneratorList& generators)
{
  generators.resize(dim, VectorType(dim));
  for (std::size_t i=0; i<dim; ++i)
  {
    for (std::size_t j=0; j<dim; ++j)
    {
      if (i == j)
      {
        generators[i][j] = 1;
      }
      else if (i+1 == j)
      {
        generators[i][j] = -1;
      }
      else if (i == dim-1 && j == dim-2)
      {
        generators[i][j] = 1;
      }
      else
      {
        generators[i][j] = 0;
      }
    }
  }
}

void input(std::string filename, VectorType& point, GeneratorList& generators)
{
  std::ifstream input( filename );
  std::string line; 
  getline( input, line );
    //process first line
  if(line.length() != 2)
  {
    throw InvalidInputException("Wrong number of lines.");
  }
  char letter = line[0];
  std::size_t dim = line[1]-'0';
  point.resize(dim);
  switch(letter) {
    case 'A':
        generateA(dim, generators);
        break;
    case 'B':
        generateB(dim, generators);
        break;
    case 'D':
        generateD(dim, generators);
        break;
    case 'E':
        break;
    case 'F':
        break;
    case 'G':
        break;
    case 'H':
        break;
    case 'I':
        break;
    default:
       throw InvalidInputException("Infinite or unknown coxeter group.");
  }
  getline( input, line );
  //process second line
  if(line.length() < 2*dim+1) //at least one number per dimension and number of dimension minus one many spaces in between, 2 brackets
  {
    throw InvalidInputException("Point vector too short.");
  }
  if(line[0]!='{' || line[line.length()-1]!='}')
  {
    throw InvalidInputException("Malformed point vector.");
  }
  std::stringstream lineIn(line.substr(1,line.length()-2));
  for(std::size_t i = 0; i < dim; ++i)
  {
    lineIn >> point[i];
  }
}

VectorType mirror(const VectorType& v, const VectorType& plane)
{
  //mirror v on plane discribed by vector plane
  double init = 0;
  double init2 = 0;
  VectorType help(v.size());
  for (std::size_t i = 0; i<plane.size();++i)
  {
    help[i] = plane[i]*(2*std::inner_product(v.begin(), v.end(), plane.begin(), init)) /
      std::inner_product(plane.begin(), plane.end(), plane.begin(), init2);
  }
  VectorType newPoint(v.size());
  for(std::size_t i = 0; i<v.size();++i)
  {
    newPoint[i] = v[i] - help[i];
  }
  return newPoint;
}

void recorbit(const GeneratorList& generators, const VectorType& v, Orbit& history)
{
  if(history.find(v) != history.end())
  {
    return;
  }  
  history.insert(v);
  for(const auto& plane : generators)
  {
    VectorType newVector = mirror(v,plane);
    recorbit(generators,newVector,history);
  }
  return;
}

Orbit orbit(const GeneratorList& generators, const VectorType& v)
{
  Orbit solution = {};
  recorbit(generators, v, solution);
  return solution;
}


void out(std::ostream& file,const Orbit& solution, bool outputOrbit)
{
  if(outputOrbit)
  {
    file << "{\n";
    for (const auto& point:solution)
    {
      file << "  {";
      bool first = true;
      for (const auto& val: point)
      {
        if(!first)
        {
          file << " ";
        }
        file << val;
        first = false;
      }
      file << "}\n";
    }
    file << "}\n";
  }
  file << boost::lexical_cast<std::string>(solution.size());
}


#endif // __ORBIT_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

//out(std::cout, Orbit(generators.begin(),generators.end()),true);

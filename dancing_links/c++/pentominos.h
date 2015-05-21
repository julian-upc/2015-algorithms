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

#ifndef __PENTOMINOS_H__
#define __PENTOMINOS_H__

#include <array>
#include <vector>
#include <set>
#include <string>
#include <limits>
#include <iostream>

namespace pentominos {

class InvalidPentominoException: public std::exception {};

typedef std::array<int,2> CooType;

class Pentomino {

public:
   std::string name;
   std::vector<std::array<int, 2>> coos;

   int min_in_coo(int coo) const {
      int min(std::numeric_limits<int>::max());
      for (const auto& c : coos) {
         if (c[coo] < min) min = c[coo];
      }
      return min;
   }

   int max_in_coo(int coo) const {
      int max(std::numeric_limits<int>::min());
      for (const auto& c : coos) {
         if (c[coo] > max) max = c[coo];
      }
      return max;
   }

   void normalize_coo(int coo) {
      const int min = min_in_coo(coo);
      for (auto& c : coos) {
         c[coo] -= min;
      }
   }

public:
   Pentomino& normalize() {
      for (int i : {0, 1}) {
         normalize_coo(i);
      }
      std::sort(coos.begin(), coos.end());
      return *this;
   }

   Pentomino(const std::string& name,
             const std::vector<std::array<int, 2>>& coos)
      : name{name}
      , coos{coos}
   {
      normalize();
   }

   Pentomino(const std::string& x) 
      : name{x}
   {
      switch(x[0]) { // because switch doesn't work on strings
      case 'F':
         coos = {{0,1},{1,0},{1,1},{1,2},{2,2}}; break;
      case 'I':
         coos = {{0,0},{0,1},{0,2},{0,3},{0,4}}; break;
      case 'L':
         coos = {{0,0},{0,1},{0,2},{0,3},{1,0}}; break;
      case 'N':
         coos = {{0,0},{0,1},{1,1},{1,2},{1,3}}; break;
      case 'P':
         coos = {{0,0},{0,1},{0,2},{1,1},{1,2}}; break;
      case 'T':
         coos = {{0,2},{1,0},{1,1},{1,2},{2,2}}; break;
      case 'U':
         coos = {{0,0},{0,1},{1,0},{2,0},{2,1}}; break;
      case 'V':
         coos = {{0,0},{1,0},{2,0},{2,1},{2,2}}; break;
      case 'W':
         coos = {{0,0},{1,0},{1,1},{2,1},{2,2}}; break;
      case 'X':
         coos = {{0,1},{1,0},{1,1},{1,2},{2,1}}; break;
      case 'Y':
         coos = {{0,0},{1,0},{2,0},{2,1},{3,0}}; break;
      case 'Z':
         coos = {{0,2},{1,0},{1,1},{1,2},{2,0}}; break;
      default:
         throw new InvalidPentominoException();
      }
   }
   
   Pentomino& flip(int coo) {
      for (auto& c : coos) {
         c[coo] = -c[coo];
      }
      normalize();
      return *this;
   }

   Pentomino& translate_one(int coo) {
      for (auto& c : coos) {
         ++c[coo];
      }
      return *this;
   }

   Pentomino& translate_coo(int coo, int amount) {
      for (auto& c : coos) {
         c[coo] += amount;
      }
      return *this;
   }

   Pentomino& translate_by(const CooType& by_vector) {
      for (int i : {0,1}) {
         translate_coo(i, by_vector[i]);
      }
      return *this;
   }

   Pentomino& turn90() {
      for (auto& c : coos) {
         std::swap(c[0], c[1]);
         c[1] = -c[1];
      }
      normalize();
      return *this;
   }

   CooType max() const {
      return CooType{max_in_coo(0), max_in_coo(1)};
   }

   friend std::ostream& operator<<(std::ostream& os, 
                                   const Pentomino& P) {
      os << "[" << P.name << ":{";
      bool first_coo(true);
      for (const auto& c : P.coos) {
         if (first_coo) first_coo = false; else os << ",";
         os << "{";
         bool first(true);
         for (const auto& x : c) {
            if (first) first = false; else os << ",";
            os << x;
         }
         os << "}";
      }
      os << "}]";
      return os;
   }

   inline
   bool operator<(const Pentomino& other) const {
      return coos < other.coos || name < other.name;
   }

};

std::array<Pentomino, 12> all_pentominos() 
{
   return std::array<Pentomino, 12>{
      Pentomino{"F"},
      Pentomino{"I"},
      Pentomino{"L"},
      Pentomino{"P"},
      Pentomino{"N"},
      Pentomino{"T"},
      Pentomino{"U"},
      Pentomino{"V"},
      Pentomino{"W"},
      Pentomino{"X"},
      Pentomino{"Y"},
      Pentomino{"Z"}};
}

std::set<Pentomino> rotated_pentominos_of(const Pentomino& P) {
   std::set<Pentomino> rotated_pentominos_of;
   Pentomino R(P);
   for (int i=0; i<4; ++i) {
      rotated_pentominos_of.insert(R);
      R.turn90();
   }
   return rotated_pentominos_of;
}

std::set<Pentomino> fixed_pentominos_of(const Pentomino& P) {
   std::set<Pentomino> fixed_pentominos_of;
   for (const auto& RR : rotated_pentominos_of(P)) {
      Pentomino R(RR);
      fixed_pentominos_of.insert(R);
      R.flip(0);
      fixed_pentominos_of.insert(R);
   }
   return fixed_pentominos_of;
}

std::set<Pentomino> all_fixed_pentominos() {
   std::set<Pentomino> all_fixed_pentominos;
   for (const auto& P : all_pentominos()) {
      for (const auto& F : fixed_pentominos_of(P)) {
         all_fixed_pentominos.insert(F);
      }
   }
   return all_fixed_pentominos;
}

} // end namespace pentominos

#endif // __PENTOMINOS_H__


// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:


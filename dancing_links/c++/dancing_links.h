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

#ifndef __DANCING_LINKS_H__
#define __DANCING_LINKS_H__

#include <limits>
#include "incidence_matrix.h"

namespace dancing_links {

   using namespace incidence_matrix::incidence_matrix;

typedef std::vector<std::vector<std::string>> Solution;

Solution solution(const std::vector<IncidenceCell*>& OO,
                  int k)
{
   Solution solution;
   for (int i=0; i<k; ++i) {
      std::vector<std::string> row;
      IncidenceCell* cur = OO[i];
      row.push_back(cur->list_header->name);
      cur = cur->right;
      while (cur != OO[i]) {
         row.push_back(cur->list_header->name);
         cur = cur->right;
      }
      solution.push_back(row);
   }
   return solution;
}

ColumnObject* choose_column_object(ColumnObject* h)
{
   int s = std::numeric_limits<int>::max();
   ColumnObject* j = h->right, *c(nullptr);
   while (j != h) {
      if (j->size < s) {
         s = j->size;
         c = j;
      }
      j = j->right;
   }
   return c;
}

template<typename CooType>
void search (int k,
             IncidenceMatrix<CooType>& I,
             std::vector<IncidenceCell*>& OO,
             std::vector<Solution>& solutions)
{
   ColumnObject* h = I.column_object_of_name["root"];
   if (h->right == h) {
      solutions.push_back(solution(OO,k));
      return;
   }

   ColumnObject* c = choose_column_object(h);
   I.cover_column(c);
   IncidenceCell* r = static_cast<IncidenceCell*>(c->down);
   while (static_cast<IncidenceCellBase*>(r) != static_cast<IncidenceCellBase*>(c)) {
      OO.resize(k+1);
      OO[k] = static_cast<IncidenceCell*>(r);
      
      IncidenceCell* j = r->right;
      while(j != r) {
         I.cover_column(j->list_header);
         j = j->right;
      }

      search(k+1, I, OO, solutions);

      r = OO[k];
      c = r->list_header;

      j = r->left;
      while (j != r) {
         I.uncover_column(j->list_header);
         j = j->left;
      }

      r = static_cast<IncidenceCell*>(r->down);
   }
   I.uncover_column(c);
}

template<typename CooType>
std::vector<Solution> Algorithm_X(IncidenceMatrix<CooType>& I)
{
   std::vector<IncidenceCell*> OO;
   std::vector<Solution> solutions;
   search(0, I, OO, solutions);
   return solutions;
}

} // end namespace dancing_links

#endif // __DANCING_LINKS_H__


// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:



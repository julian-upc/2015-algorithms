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

#ifndef __INCIDENCE_MATRIX_H__
#define __INCIDENCE_MATRIX_H__

#include <array>
#include <vector>
#include <set>
#include <map>
#include <string>
#include "stl_wrappers.h"


  
namespace incidence_matrix {

std::string to_string(const std::array<int, 2ul>& p)
{
   std::string concat_p("<");
   bool first = true;
   for (const auto& x : p) {
      concat_p += (!first ? "," : "") + std::to_string(x);
      first = false;
   }
   concat_p += ">";
   return concat_p;
}

std::string to_string(const std::string& p)
{
   return p;
}

class ForbiddenPlacementException : public std::exception {};

typedef std::array<std::string, 6> CellRepType;
typedef std::vector<CellRepType> ColRepType;
typedef std::vector<std::string> RowRepType;

class IncidenceCellBase {
public:
   IncidenceCellBase* up;
   IncidenceCellBase* down;
   std::string name;

   IncidenceCellBase() {}

   IncidenceCellBase(IncidenceCellBase* up,
                     IncidenceCellBase* down,
                     const std::string& name)
      : up(up)
      , down(down)
      , name(name)
   {}

   IncidenceCellBase(const std::string& name)
      : up(this)
      , down(this)
      , name(name)
   {}
};

class ColumnObject;

class IncidenceCell : public IncidenceCellBase {
public:
   IncidenceCell* left;
   IncidenceCell* right; 
   ColumnObject* list_header;

   IncidenceCell() {}

   IncidenceCell(IncidenceCell* left, 
                 IncidenceCell* right, 
                 IncidenceCellBase* up,
                 IncidenceCellBase* down,
                 ColumnObject* list_header,
                 const std::string& name)
      : IncidenceCellBase(up, down, name)
      , left(left)
      , right(right)
      , list_header(list_header)
   {}

   CellRepType representation() const {
      return { "c", name, left->name, right->name, up->name, down->name };
   }

};

class ColumnObject : public IncidenceCellBase {
public:
   ColumnObject* left;
   ColumnObject* right; 
   int size;
   ColumnObject(ColumnObject* left, 
                ColumnObject* right, 
                IncidenceCellBase* up,
                IncidenceCellBase* down,
                const std::string& name)
      : IncidenceCellBase(up, down, name)
      , left(left)
      , right(right)
      , size(0) 
   {}

   ColumnObject(const std::string& name)
      : IncidenceCellBase(name) 
      , left(this)
      , right(this)
      , size(0) 
   {}

   ColRepType representation() const {
      ColRepType representation;
      representation.push_back( { "h(" + std::to_string(size) + ")", name, left->name, right->name, up->name, down->name } );
      IncidenceCellBase* current_cell(down);
      while (current_cell != this) {
         // We know that all cells except "this" are really IncidenceCells!
         representation.push_back(static_cast<IncidenceCell*>(current_cell)->representation());
         current_cell = current_cell->down;
      }
      return representation;
   }
};


template<typename CooType>
class IncidenceMatrix {
public:
   ColumnObject* h;
   int rows;
   std::map<std::string, ColumnObject*> column_object_of_name;
   std::map<std::string, int> index_of_piece_placement;

   IncidenceMatrix(const std::vector<std::string>& names)
      : h(new ColumnObject("root"))
      , rows(0)
      , column_object_of_name{ { "root", h } }
   {
      ColumnObject* current_column_object{h};
      for (const auto& n : names) {
         index_of_piece_placement[n] = 0;
         insert_column_object(current_column_object, h, n);
         current_column_object = current_column_object->right;
         column_object_of_name[n] = current_column_object;
      }
   }

   void insert_column_object(ColumnObject* left,
                             ColumnObject* right,
                             const std::string& name) {
      ColumnObject* x = new ColumnObject(name);
      x->left = left;
      x->right = right;
      x->up = x;
      x->down = x;
      right->left = x;
      left->right = x;
   }

   std::vector<ColRepType> representation() const {
      ColRepType root_rep;
      root_rep.push_back( { "r(0)", "root", h->left->name, h->right->name, h->up->name, h->down->name } );
      std::vector<ColRepType> representation;
      representation.push_back(root_rep);

      ColumnObject* current_column_object{h->right};
      while (current_column_object->name != "root") {
         representation.push_back(current_column_object->representation());
         current_column_object = current_column_object->right;
      }
      return representation;
   }

   std::vector<RowRepType> row_representation() const {
      std::vector<RowRepType> row_representation;
      ColumnObject* current_column_object{h->right};
      while (current_column_object->name != "root" &&
             current_column_object->name.find_first_of("{ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") != std::string::npos) {
         IncidenceCellBase* head_elt = current_column_object->down;
         while (head_elt != current_column_object) {
            const IncidenceCell* alias = static_cast<IncidenceCell*>(head_elt);
            RowRepType row_rep { alias->name };
            IncidenceCell* current_elt (alias->right);
            while (current_elt != alias) {
               row_rep.push_back(current_elt->list_header->name);
               current_elt = current_elt->right;
            }
            row_representation.push_back(row_rep);
            head_elt = head_elt->down;
         }
         current_column_object = current_column_object->right;
      }
      return row_representation;
   }
   
   void append_row(const std::string& tile_name,
                   const std::vector<CooType>& placement) {
      ColumnObject* row_header_col = column_object_of_name[tile_name];
      IncidenceCell* row_header = new IncidenceCell(nullptr,
                                                    nullptr,
                                                    row_header_col->up,
                                                    row_header_col,
                                                    row_header_col,
                                                    tile_name + "{" + std::to_string(index_of_piece_placement[tile_name]) + "}");
      row_header->left = row_header->right = row_header;
      row_header_col->up->down = row_header;
      row_header_col->up = row_header;
      ++row_header_col->size;
      ++index_of_piece_placement[tile_name];
      for (const auto& p : placement) {
         const std::string concat_p { to_string(p) };
         ColumnObject* pos_col = column_object_of_name[concat_p];
         IncidenceCell* x = new IncidenceCell(row_header->left, row_header, pos_col->up, pos_col, pos_col, tile_name + concat_p);
         x->up->down = x->down->up = x->right->left = x->left->right = x;
         ++pos_col->size;
      }
      ++rows;
   }

   typedef std::map<std::string, std::vector<std::vector<CooType>>> RequiredPlacementType;

   template<typename TileContainer>
   void append_translates_2d(const TileContainer& tiles,
                             const CooType& board_size,
                             std::function<bool(const CooType&)> is_allowed = [](const CooType&) -> bool { return true; },
                             const RequiredPlacementType& required_placements = RequiredPlacementType()) {
      for (const auto& tile : tiles) {
         typename RequiredPlacementType::const_iterator tit = required_placements.find(tile.name);
         if (tit != required_placements.end()) {
            append_required_placements(tile, tit->second, is_allowed, board_size);
         } else {
            append_unrestricted_translates_2d(tile, board_size, is_allowed);
         }
      }
   }

   template<typename Placement>
   bool is_legal(const Placement& placement,
                 std::function<bool (const CooType&)> is_allowed,
                 const CooType& board_size) {
      bool legal(true);
      for (typename Placement::const_iterator pit = placement.begin(), pend = placement.end(); legal && pit != pend; ++pit) {
         const CooType coo(*pit);
         if (!is_allowed(coo)) {
            legal = false; 
         }
         for (unsigned int i=0; legal && i<coo.size(); ++i) {
            if (coo[i] < 0 || coo[i] >= board_size[i]) {
               legal = false; 
            }
         }
      }
      return legal;
   }

   template<typename Tile, typename PlacementContainer>
   void append_required_placements(const Tile& tile,
                                   const PlacementContainer& placements,
                                   std::function<bool (const CooType&)> is_allowed,
                                   const CooType& board_size) {
      for (const auto& placement : placements) {
         if (!is_legal(placement, is_allowed, board_size)) {
            throw ForbiddenPlacementException();
         }
         append_row(tile.name, placement);
      }
   }

   template<typename Tile>
   void append_unrestricted_translates_2d(const Tile& _tile,
                                          const CooType& board_size,
                                          std::function<bool(const CooType&)> is_allowed)
   {
      Tile tile(_tile);
      const CooType infty_norm = tile.max();
      for (int i=0; i < board_size[0] - infty_norm[0]; ++i) {
         for (int j=0; j < board_size[1] - infty_norm[1]; ++j) {
            if (is_legal(tile.coos, is_allowed, board_size)) {
               append_row(tile.name, tile.coos);
            }
            tile.translate_one(1);
         }
         tile.translate_coo(1, infty_norm[1] - board_size[1]);
         tile.translate_one(0);
      }
   }
   
   void cover_column(ColumnObject* c) {
      c->right->left = c->left;
      c->left->right = c->right;
      IncidenceCellBase* i = c->down;
      while (i != c) {
         // we know that i points to an IncidenceCell, not a ColumnObject
         IncidenceCell* j = static_cast<IncidenceCell*>(i)->right;
         while (j != static_cast<IncidenceCell*>(i)) {
            j->down->up = j->up;
            j->up->down = j->down;
            --j->list_header->size;
            j = j->right;
         }
         i = i->down;
      }
   }

   void uncover_column(ColumnObject* c) {
      IncidenceCellBase* i = c->up;
      while (i != c) {
         // we know that i points to an IncidenceCell, not a ColumnObject
         IncidenceCell* j = static_cast<IncidenceCell*>(i)->left;
         while (j != static_cast<IncidenceCell*>(i)) {
            ++j->list_header->size;
            j->down->up = j;
            j->up->down = j;
            j = j->left;
         }
         i = i->up;
      }
      c->right->left = c;
      c->left->right = c;
   }

};

} // end namespace incidence_matrix

#endif // __INCIDENCE_MATRIX_H__


// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:


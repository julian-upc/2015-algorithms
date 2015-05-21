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

#ifndef __BOOST_COUT_WRAPPERS_H
#define __BOOST_COUT_WRAPPERS_H

#include <vector>
#include <array>

namespace boost
{

// teach Boost.Test how to print std::array
template <typename T, std::size_t k>
inline wrap_stringstream&
operator<<(wrap_stringstream& wrapped, const std::array<T, k>& item)
{
    wrapped << '{';
    bool first = true;
    for (auto const& element : item) {
        wrapped << (!first ? "," : "") << element;
        first = false;
    }
    return wrapped << '}';
}


// teach Boost.Test how to print std::vector
template <typename T>
inline wrap_stringstream&
operator<<(wrap_stringstream& wrapped, std::vector<T> const& item)
{
    wrapped << '{';
    bool first = true;
    for (auto const& element : item) {
        wrapped << (!first ? "," : "") << element;
        first = false;
    }
    return wrapped << '}';
}

// teach Boost.Test how to print std::pair
template <typename K, typename V>
inline wrap_stringstream&
operator<<(wrap_stringstream& wrapped, std::pair<const K, V> const& item)
{
    return wrapped << '<' << item.first << ',' << item.second << '>';
}


} // end namespace boost

namespace std {

inline
bool operator!=(const array<int,2>& left, const array<int,2>& right) {
   return 
      left[0] != right[0] ||
      left[1] != right[1];
}

} // end namespace std

#endif // __BOOST_COUT_WRAPPERS_H

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

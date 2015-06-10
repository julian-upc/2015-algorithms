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

//#ifndef __STL_WRAPPERS_H__
//#define __STL_WRAPPERS_H__

#include <array>
#include <vector>
#include <set>
#include <map>


template <typename T, std::size_t k>
inline std::ostream&
operator<<(std::ostream& wrapped, const std::array<T, k>& item)
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
inline std::ostream&
operator<<(std::ostream& wrapped, std::vector<T> const& item)
{
    wrapped << '{';
    bool first = true;
    for (auto const& element : item) {
        wrapped << (!first ? "," : "") << element;
        first = false;
    }
    return wrapped << '}';
}

template <typename K, typename V>
inline std::ostream&
operator<<(std::ostream& wrapped, std::pair<const K, V> const& item)
{
    return wrapped << '<' << item.first << ',' << item.second << '>';
}

template <typename K, typename V>
inline std::ostream&
operator<<(std::ostream& wrapped, std::map<K, V> const& item)
{
    wrapped << '{';
    bool first = true;
    for (auto const& element : item) {
        wrapped << (!first ? "," : "") << element;
        first = false;
    }
    return wrapped << '}';
}


//#endif // __STL_WRAPPERS_H__


// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:


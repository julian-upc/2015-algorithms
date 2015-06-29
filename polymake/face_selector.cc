/* Copyright (c) 2015
   Julian Pfeifle and Implementation Class at TU Berlin
   julian.pfeifle@upc.edu

   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the
   Free Software Foundation; either version 2, or (at your option) any
   later version: http://www.gnu.org/licenses/gpl.txt.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
--------------------------------------------------------------------------------
*/

#include "polymake/client.h"
#include "polymake/Rational.h"
#include "polymake/Matrix.h"
#include "polymake/Vector.h"
#include "polymake/IncidenceMatrix.h"
#include "polymake/linalg.h"

namespace polymake { namespace polytope {

template<typename Scalar>
Vector<Scalar> face_selector(perl::Object P, const Set<int>& S)
{
   const Matrix<Scalar> facets = P.give("FACETS");
   const int ambient_dim = facets.cols();

   Vector<Scalar> face_selector(unit_vector<Scalar>(ambient_dim, 0));

   const Matrix<Scalar> vertices = P.give("VERTICES");
   if (rank(vertices.minor(S, All)) == rank(vertices))
      return face_selector;

   const IncidenceMatrix<> VIF = P.give("VERTICES_IN_FACETS");

   for (Entire<Rows<IncidenceMatrix<> > >::const_iterator rit = entire(rows(VIF)); 
        !rit.at_end(); 
        ++rit) {
      if (incl(S, *rit) <= 0) {
         face_selector += facets[rit->index()];
      }
   }
   return face_selector;
}

UserFunctionTemplate4perl("# @category Other"
                          "# Given a subset S of the vertices of the input polytope, return a" 
                          "# linear form that selects the inclusion-minimal face of P containing S."
                          "# @param Polytope P the input polytope"
                          "# @param Set<Int> S subset of the indices of vertices of P"
                          "# @return Vector",
                          "face_selector<Scalar>(Polytope<Scalar>, Set)");

} }

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

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

#ifndef __GENERATORS_H_
#define __GENERATORS_H_

#include <math.h>
#include <string>
#include <sstream>
#include "types.h"

GeneratorList simple_roots_type_A (const int n)
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0 0 ... 0  0
     0  1 -1 0 ... 0  0
     ...
     0  0  0 0 ... 1 -1
     In particular, they lie in the plane (sum of coordinates = 0)
    */
   GeneratorList R(n, n+1);
   for (int i=0; i<n; ++i) {
      VectorType v(n+1);
      v[i] = 1; 
      v[i+1] = -1;
      R[i] = v;
   }
   return R;
}

GeneratorList simple_roots_type_B (const int n)
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0 0 ... 0  0
     0  1 -1 0 ... 0  0
     ...
     0  0  0 0 ... 1 -1
     0  0  0 0 ... 0  1

     The Dynkin diagram is:

     0 ---- 1 ---- ... ---- n-2 --(4)--> n-1,
    */
   VectorType v(n);
   v[n-1] = 1;
   GeneratorList G = simple_roots_type_A(n-1);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_C (const int n)
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0 0 ... 0  0
     0  1 -1 0 ... 0  0
     ...
     0  0  0 0 ... 1 -1
     0  0  0 0 ... 0  2

     The Dynkin diagram is:

     0 ---- 1 ---- ... ---- n-2 <--(4)-- n-1,
    */
   VectorType v(n);
   v[n-1] = 2;
   GeneratorList G = simple_roots_type_A(n-1);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_D (const int n)
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0 0 ... 0 0
     0  1 -1 0 ... 0 0
     ...
     0  0  0 0 ... 1 -1
     0  0  0 0 ... 1  1
     The indexing of the Dynkin diagram is

                           n-2
                           /
     0 - 1 - 2 - ... - n-3
                           \
                           n-1

   */
   VectorType v(n);
   v[n-2] = v[n-1] = 1;
   GeneratorList G = simple_roots_type_A(n-1);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_E6()
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0  0  0  0
     0  1 -1  0  0  0
     0  0  1 -1  0  0
     0  0  0  1 -1  0
     0  0  0  1  1  0
-1/2(1  1  1  1  1 -sqrt(3))  
 
     The indexing of the Dynkin diagram is


                   3
                   |
                   |
     0 ---- 1 ---- 2 ---- 4 ---- 5
     
   */
   VectorType v(6);
   for (int i=0; i<5; ++i)
      v[i] = -0.5;
   v[5] = 0.5 * sqrt(3);
   GeneratorList G = simple_roots_type_D(5);
   for (int i=0; i<5; ++i)
      G[i].push_back(0);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_E7()
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0  0  0  0  0
     0  1 -1  0  0  0  0
     0  0  1 -1  0  0  0
     0  0  0  1 -1  0  0
     0  0  0  0  1 -1  0
     0  0  0  0  1  1  0
-1/2(1  1  1  1  1  1 -sqrt(2))  
 
     The indexing of the Dynkin diagram is


                          4
                          |
                          |
     0 ---- 1 ---- 2 ---- 3 ---- 5 ---- 6
     
   */
   VectorType v(7);
   for (int i=0; i<6; ++i)
      v[i] = -0.5;
   v[6] = 0.5 * sqrt(2);
   GeneratorList G = simple_roots_type_D(6);
   for (int i=0; i<6; ++i)
      G[i].push_back(0);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_E8()
{
   /*
     Read rowwise, these simple root vectors are
     1 -1  0 0 0 0  0 0
     0  1 -1 0 0 0  0 0
     ...
     0  0  0 0 0 1 -1 0
     0  0  0 0 0 1  1 0
-1/2(1  1  1 1 1 1  1 1)  
 
     These are the coordinates in the even coordinate system.
     The indexing of the Dynkin diagram is


                                 5
                                 |
                                 |
     0 ---- 1 ---- 2 ---- 3 ---- 4 ---- 6 ---- 7 
     
   */
   VectorType v(8);
   for (int i=0; i<8; ++i)
      v[i] = -0.5;
   GeneratorList G = simple_roots_type_D(7);
   for (int i=0; i<7; ++i)
      G[i].push_back(0);
   G.push_back(v);
   return G;
}

GeneratorList simple_roots_type_F4()
{
   /*
     Read rowwise, these simple root vectors are
     1    -1     0    0
     0     1    -1    0
     0     0     1    0
     -1/2  -1/2  -1/2 -1/2

     The Dynkin diagram is:

     0 ---- 1 --(4)--> 2 ---- 3
   */
   GeneratorList R(4,4);
   R(0,0) = R(1,1) = R(2,2) = 1;
   R(0,1) = R(1,2) = -1;
   R(3,0) = R(3,1) = R(3,2) = R(3,3) = -0.5;
   return R;
}

GeneratorList simple_roots_type_G2()
{
   /*
     Read rowwise, these simple root vectors are
      1 -1  0
     -1  2 -1

     Notice that each row sums to zero.

     The Dynkin diagram is:

     0 <--(6)-- 1
   */
   GeneratorList R(2,3);
   R(0,0) = 1;
   R(0,1) = R(1,0) = R(1,2) = -1;
   R(1,1) = 2;
   return R;
}

GeneratorList simple_roots_type_H3()
{
   const NumberType tau(0.5 + 0.5 * sqrt(5)); // golden ratio
   
   /*
     For H_3, the Dynkin diagram is

     0 --(5)-- 1 ---- 2,

     and the simple root vectors are, 

      2 0 0
      a b -1
      0 0 2

      with a=-tau and b=1/tau. Notice they all have length 2.
                              
   */

   GeneratorList R(3,3);
   R(0,0) = R(2,2) = 2;
   R(1,0) = -tau; R(1,1) = tau - 1; R(1,2) = -1;
   return R;
}

GeneratorList simple_roots_type_H4()
{
   const NumberType tau(0.5 + 0.5 * sqrt(5)); // golden ratio

   /*
     For H_4, the Dynkin diagram is

     0 --(5)-- 1 ---- 2 ---- 3,

     and the simple root vectors are, according to 
     [John H. Stembridge, A construction of H_4 without miracles, 
      Discrete Comput. Geom. 22, No.3, 425-427 (1999)],

       a  b  b  b
      -1  1  0  0
       0 -1  1  0
       0  0 -1  1

      with a=(1+tau)/2 and b=(1-tau)/2, so that the length of each root is sqrt{2}.
                              
   */
   GeneratorList R(4, 4);
 
   R(0,0) = (1+tau) * 0.5;
   R(0,1) = R(0,2) = R(0,3) = (1-tau) * 0.5;
   
   for (int i=0; i<3; ++i) {
      R(i+1, i)   = -1;
      R(i+1, i+1) =  1;
   }
   return R;
}



GeneratorList simple_roots(char type, int dim)
{
   switch(type) {
   case 'a':
   case 'A':
      return simple_roots_type_A(dim);

   case 'b':
   case 'B':
      return simple_roots_type_B(dim);

   case 'c':
   case 'C':
      return simple_roots_type_C(dim);

   case 'd':
   case 'D':
      return simple_roots_type_D(dim);

   case 'e':
   case 'E':
      switch(dim) {
      case 6:
         return simple_roots_type_E6();
      case 7:
         return simple_roots_type_E7();
      case 8:
         return simple_roots_type_E8();
      default:
         throw InvalidGroupException();
      }

   case 'f':
   case 'F':
      switch(dim) {
      case 4:
         return simple_roots_type_F4();
      default:
         throw InvalidGroupException();
      }

   case 'g':
   case 'G':
      switch(dim) {
      case 2:
         return simple_roots_type_G2();
      default:
         throw InvalidGroupException();
      }

   case 'h':
   case 'H':
      switch(dim) {
      case 3:
         return simple_roots_type_H3();
      case 4:
         return simple_roots_type_H4();
      default:
         throw InvalidGroupException();
      }

   default:
      throw NotImplementedException();
   }
}

#endif // __GENERATORS_H_

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

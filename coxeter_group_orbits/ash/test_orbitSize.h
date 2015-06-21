#ifndef __ORBITSIZE_H_
#define __ORBITSIZE_H_

#include <numeric>
#include <vector>
#include <functional>
#include <set>
#include <initializer_list>
#include <iostream>
#include <assert.h>
#include "types.h"
#include "generators.h"
#include "orbit.h"

///////////////////////////////////////////////////////////////////////////////////////
//copied from http://www.cs.upc.edu/~jordicf/Teaching/programming/pdf4/MATH03_Gaussian-4slides.pdf
   VectorType BackSubstitution(const GeneratorList& A,const VectorType& b) {
      int n = A.size();
      VectorType x(n); 
      // Creates the vector for the solution
      // Calculates x from x[n-1] to x[0]
      for(int i= n-1; i>= 0; --i) {
      // The values x[i+1..n-1] have already been calculated
         NumberType s = 0;
         for(int j = i+ 1; j < n; ++j){ 
            s = s + A[i][j]*x[j];
         }
         x[i] = (b[i] - s) / A[i][i];
      }
      return x;
   }

   int find_max(const GeneratorList& A, int k) {
      int n = A.size();
      NumberType imax = k; 
   // index of the row with max pivot 
      NumberType max_pivot = abs(A[k][k]);
      for(int i = k + 1; i< n; ++i) {
         NumberType a = abs(A[i][k]);
         if(a > max_pivot) {
            max_pivot= a;
            imax = i;
         }
      }
      return imax;
   }

   bool GaussianElimination(GeneratorList& A, VectorType& b){
      const int n = A.size();
      const int m = b.size();
      assert(n == m);

      for(int k = 1; k < n-1; ++k){
         /*//Pivoting
         int imax = find_max(A,k);
         if(A[imax][k] == 0){return true;}

         swap(A[k], A[imax]);
         //swap numbers
         NumberType x = b[k];
         b[k] = b[imax];
         b[imax] = x; 
         */
         for(int i = k + 1; i < n; ++i) {
            NumberType c = A[i][k]/A[k][k]; // coefficient to scale row
            A[i][k] = 0;
            for(int j = k + 1; j < n; ++j){
               A[i][j] = A[i][j] - c*A[k][j];

            }
            b[i] = b[i] - c*b[k];
         }
      }
      return false; 
   }

   bool swap(VectorType& a, VectorType& b){
      VectorType x(a);
      for (VectorType::size_type i = 0; i != a.size(); i++){
            a[i] == b[i];
            b[i] == x[i];
         }
      return true;
   }

   VectorType SystemEquations(GeneratorList& A, VectorType& b) {
      bool singular = GaussianElimination(A, b);
      if(singular) return VectorType(0);
      // A is in row echelon form
      return BackSubstitution(A, b);
   }
/////////////////////////////////////////////////////////////////////////////////////////
void checkOrbitSize(char type, int dim1, int dim2){
   GeneratorList g1 = simple_roots(type, dim1);
   GeneratorList g2 = g1;
   GeneratorList g3 = g1;
   //GeneratorList g3 = simple_roots(type, dim1-dim2);
   
   VectorType x1(dim1);
   VectorType x2(dim1);

   for (VectorType::size_type i = 0; i != x1.size(); i++){
      if(i < (dim2)){
         x2[i] = 0.0;
      }else{
         x2[i] = 1.0;
      }
      x1[i] = 1.0;
   }
     
   Orbit o1 = orbit(g1, SystemEquations(g3, x1));
   Orbit o2 = orbit(g1, SystemEquations(g2, x2));
   std::cout << "Orbit "<< type << dim1 << ": \n vector on " << dim2 << " hyperplanes: " <<o2.size() << " \n vector in general positions: "<< o1.size() <<"\n"; 
  
} 

Orbit checkOrbitGeneralPosition(char type, int dim1){
   GeneratorList g1 = simple_roots(type, dim1);
   GeneratorList g2 = g1;
   //GeneratorList g3 = simple_roots(type, dim1-dim2);
   
   VectorType x1(dim1);

   for (VectorType::size_type i = 0; i != x1.size(); i++){
      x1[i] = 1.0;
   }
   return orbit(g1, SystemEquations(g2, x1));	
}

VectorType getVectorGeneralPosition(char type, int dim1){
   GeneratorList g1 = simple_roots(type, dim1);
   
   VectorType x1(dim1);

   for (VectorType::size_type i = 0; i != x1.size(); i++){
      x1[i] = 1.0;
   }
   return SystemEquations(g1, x1);	
}

#endif // __ORBITSIZE_H_

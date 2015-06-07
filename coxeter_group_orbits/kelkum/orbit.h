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
#include <sstream>
#include <cmath>


template<typename T> //only numeric types please
class ImperciseVector: public std::vector<T> {
    public:
        ImperciseVector() {}
        bool operator== (const ImperciseVector& v) { //does not work yet
            double epsilon = 0.0001;
            unsigned int k = this->size(); 
            for (unsigned int j = 0; j<k; j++) {
               if( abs((*this)[j]-v[j]) > epsilon) return false; 
            }
            return true;
        }

           
        //   T l1sq=0.0, l2sq=0.0, l3sq=0.0;

        //   if (this->size() != v.size() || this->size()==0 || v.size()==0) return false; 
        //   for (unsigned int j = 0; j<(this->size()); j++) {
        //       l1sq += (*this)[j]*(*this)[j];
        //       l2sq += v[j]*v[j];
        //       l3sq+= ((*this)[j]-v[j])*((*this)[j]-v[j]);
        //   }
        //   some estimate such that length of their their difference (relative to their size) is small enough
        //   if (l3sq/(l1sq*l2sq) <= 0.0001) return true; 
        //   return false;
        //}
};

typedef ImperciseVector<double> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;
enum errorTypes {NotImplemented, DimensionError, InputError, DotProdNotDefined};

void simple_roots(char type, int dim, GeneratorList& normals); //forward declaration of function
Orbit genorbit(const GeneratorList& generators, const VectorType& v); //forward declaration of function

Orbit processing(std::string& coxeterDiagram, VectorType& inputPoint) {
    std::stringstream ss; 
    ss << coxeterDiagram;

    char diagramType;
    int normalNumber;
    GeneratorList normalVectors;
    Orbit orbit; 

    ss >> diagramType >> normalNumber; //not sure but it seems to work
    int dimensionPoint = inputPoint.size(); 

    //checking/correcting input ambiguities
    if (dimensionPoint != normalNumber || normalNumber<=0) {
        throw DimensionError;
    }
    if (diagramType == 'A' || diagramType == 'a') { //make dimensions of normals and the point in this special case the same so one gets sensable dotproducts
        inputPoint.push_back(0.0);
    }
    simple_roots(diagramType, normalNumber, normalVectors); //modifies the normals Variable to get all the normals corresponding to a certain Coxeter diagram into the normals "matrix"
    orbit = genorbit(normalVectors, inputPoint);
    return orbit; 

}

void simple_roots(char type, int dim, GeneratorList& normals)
{
   VectorType tmpVector;
   double tmpEntry;
   normals.clear();
   
   switch(type) { 
       case 'a': case 'A':
           for (int vectorNr = 0; vectorNr<dim; vectorNr++) {
               tmpVector.clear();
               for (int vectorEntry = 0; vectorEntry<dim+1; vectorEntry++) {
                   if (vectorNr==vectorEntry) tmpEntry = 1.0; 
                   else if (vectorNr==vectorEntry-1) tmpEntry = -1.0;
                   else tmpEntry = 0.0;
                   tmpVector.push_back(tmpEntry);
               }
               normals.push_back(tmpVector);
           }
           break;

       case 'b': case 'B':
          for (int vectorNr = 0; vectorNr<dim; vectorNr++) {
               tmpVector.clear();
               for (int vectorEntry = 0; vectorEntry<dim; vectorEntry++) {
                   if (vectorNr==vectorEntry) tmpEntry = 1.0; 
                   else if (vectorNr==vectorEntry-1) tmpEntry = -1.0;
                   else tmpEntry = 0.0;
                   tmpVector.push_back(tmpEntry);
               }
               normals.push_back(tmpVector);
           }
           break;

           //other diagrams need to be implemented

       default:
          throw NotImplemented;
   }
}

double dotprod(const VectorType& v1, const VectorType& v2) {
    if (v1.size()!=v2.size()) {
        throw DotProdNotDefined;
        return 0.0;
    }
    double d = 0.0;
    for (unsigned int i = 0; i<v1.size(); i++) {
        d+=v1[i]*v2[i];
    }
    return d;
}

//requires a VectorType as input that it can write the result of the reflection to, to try to avoid copying and reassigning as this is the function used the most often
void reflect(const VectorType& normal, const VectorType& point, VectorType& result) {
    result=point;
    double pointDotNormal = dotprod(point, normal);
    double normalDotNormal = dotprod(normal, normal);
    for (unsigned int i = 0; i<point.size(); i++) {
        result[i]-=2*(pointDotNormal/normalDotNormal)*normal[i];
    }
}

Orbit genorbit(const GeneratorList& generators, const VectorType& v) {
    std::set<VectorType> pointOrbit;
    pointOrbit.insert(v);
    std::set<VectorType>::iterator it;

    VectorType tmpPoint;
    GeneratorList buffer1, buffer2; 
    buffer2.push_back(v);
    GeneratorList* writingBufferNewPoints = &buffer1;
    GeneratorList* readingBufferNewPoints = &buffer2;

    int compositionLength=50;

    for (int i = 0; i<compositionLength; i++) {
        if ((*readingBufferNewPoints).size() == 0) break;
        for (unsigned int j = 0; j<(*readingBufferNewPoints).size(); j++) { //iterate through all new points
            for (unsigned int k=0; k<generators.size(); k++) { //reflect each individual new point in all planes
                tmpPoint.clear(); 
                reflect(generators[k], (*readingBufferNewPoints)[j], tmpPoint);
                //now check if new creation is already in pointOrbit, if not add it to the pointOrbit and to writingBufferNewPoints that will be read from in the next iteration of i
                for (it=pointOrbit.begin(); it!=pointOrbit.end(); it++) {
                    if (tmpPoint==(*it)) break; //approximate comparison
                    pointOrbit.insert(tmpPoint);
                    for (unsigned int l=0; l<(*writingBufferNewPoints).size(); l++) {//reading from the writingbuffer but this is only to ensure I have not already written the point to it
                        if (tmpPoint==(*writingBufferNewPoints)[l]) goto escape;
                    }
                    (*writingBufferNewPoints).push_back(tmpPoint);
                    escape:;
                }
            }
        }
        (*readingBufferNewPoints).clear(); 
        std::swap(writingBufferNewPoints, readingBufferNewPoints);

    }
    return pointOrbit;
}


#endif // __ORBIT_H_
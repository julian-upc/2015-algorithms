/* This program is free software; you can redistribute it and/or modify it
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
const static double epsilon = 0.0001; 


template<typename T> //only numeric types please
class ImpreciseVector: public std::vector<T> {
    public:
        ImpreciseVector() {}
        bool operator== (const ImpreciseVector& v) { //does not work yet
           unsigned int k = this->size();          
           T l1sq=static_cast<T>(0.0), l2sq=static_cast<T>(0.0), l3sq=static_cast<T>(0.0);

           if (k != v.size() || k==0 || v.size()==0) return false; 
           for (unsigned int j = 0; j<k; j++) {
               l1sq += (*this)[j]*(*this)[j];
               l2sq += v[j]*v[j];
               l3sq+= ((*this)[j]-v[j])*((*this)[j]-v[j]);
           }
           //some estimate such that length of their their difference (relative to their size) is small enough
           if (l3sq/(l1sq*l2sq) <= epsilon) return true; 
           return false;
        }
};

typedef ImpreciseVector<double> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;
enum errorTypes {NotImplemented, DimensionError, InputError, DotProdNotDefined};

void simple_roots(char type, unsigned int dim, GeneratorList& normals); //forward declaration of function
Orbit genOrbit(const GeneratorList& generators, const VectorType& v); //forward declaration of function

Orbit giveOrbit(const std::string& coxeterDiagram, VectorType& inputPoint) {
    std::stringstream ss; 
    ss << coxeterDiagram;
    char diagramType;
    unsigned int normalNumber;

    ss >> diagramType >> normalNumber; //not sure but it seems to work
    int dimensionPoint = inputPoint.size(); 

    //checking/correcting input ambiguities
    if (dimensionPoint != normalNumber || normalNumber<=0) {
        throw DimensionError;
    }
    if (diagramType == 'A' || diagramType == 'a') { //make dimensions of normals and the point in this special case the same so one gets sensable dotproducts
        inputPoint.push_back(0.0);
    }

    GeneratorList normalVectors;
    simple_roots(diagramType, normalNumber, normalVectors); //modifies the normals Variable to get all the normals corresponding to a certain Coxeter diagram into the normals "matrix"
    return genOrbit(normalVectors, inputPoint);
}

void simple_roots(char type, unsigned int dim, GeneratorList& normals)
{
   double tmpEntry;
   normals.clear();
   VectorType tmpVector;

   switch(type) { 
       case 'a': case 'A':
           for (unsigned int i = 0; i<dim; i++) {
               tmpVector.clear();
               for (unsigned int j = 0; j<dim+1; j++) {
                   if (i==j) tmpEntry = 1.0; 
                   else if (i==j-1) tmpEntry = -1.0;
                   else tmpEntry = 0.0;
                   tmpVector.push_back(tmpEntry);
               }
               normals.push_back(tmpVector);
           }
           break;

       case 'b': case 'B':
          for (unsigned int i = 0; i<dim; i++) {
               tmpVector.clear();
               for (unsigned int j = 0; j<dim; j++) {
                   if (i==j) tmpEntry = 1.0; 
                   else if (i==j-1) tmpEntry = -1.0;
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
    const double pointDotNormal = dotprod(point, normal);
    const double normalDotNormal = dotprod(normal, normal);
    for (unsigned int i = 0; i<point.size(); i++) {
        result[i]-=2*(pointDotNormal/normalDotNormal)*normal[i];
    }
}

Orbit genOrbit(const GeneratorList& generators, const VectorType& v) {
    std::set<VectorType> pointOrbit;
    pointOrbit.insert(v);

    VectorType tmpPoint;
    GeneratorList buffer1, buffer2; 
    buffer2.push_back(v);
    GeneratorList* writingBufferNewPoints = &buffer1;
    GeneratorList* readingBufferNewPoints = &buffer2;

    unsigned int compositionLength=50;

    for (unsigned int i = 0; i<compositionLength; i++) {
        if ((*readingBufferNewPoints).size() == 0) break;
        for (unsigned int j = 0; j<(*readingBufferNewPoints).size(); j++) { //iterate through all new points
            for (unsigned int k=0; k<generators.size(); k++) { //reflect each individual new point in all planes
                tmpPoint.clear(); 
                reflect(generators[k], (*readingBufferNewPoints)[j], tmpPoint);
                //now check if new creation is already in pointOrbit, if not add it to the pointOrbit and to the newPointBuffer that will be read from in the next iteration of i
                bool inOrbit = false;
                bool inWritingBuffer=false;
                for (std::set<VectorType>::iterator it=pointOrbit.begin(); it!=pointOrbit.end(); it++) {
                    if (tmpPoint==(*it)) {//approximate comparison
                        inOrbit = true;
                        break; //I hope this breaks the lit loop and not the if statement
                    }
                }
                if (!inOrbit) { 
                    pointOrbit.insert(tmpPoint);
                    for (unsigned int l=0; l<(*writingBufferNewPoints).size(); l++) {//reading from the writingbuffer but this is only to ensure I have not already written the point to it
                        if (tmpPoint==(*writingBufferNewPoints)[l]) {
                            inWritingBuffer = true;
                            break;
                        }
                    }
                }

        
                if (!inWritingBuffer) (*writingBufferNewPoints).push_back(tmpPoint);
            }
            (*readingBufferNewPoints).clear(); 
            std::swap(writingBufferNewPoints, readingBufferNewPoints);
        }
    }
    return pointOrbit;
}


#endif // __ORBIT_H_
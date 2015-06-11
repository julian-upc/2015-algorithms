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
const static double epsilon = 0.00001; 


template<typename T> //only numeric types please
class ImpreciseVector: public std::vector<T> {
    public:
        ImpreciseVector() {}
        ImpreciseVector(unsigned int a, T iniValue) { //constructor not inherited...
            this->resize(a, iniValue);
        }
            bool operator== (const ImpreciseVector& v) { //does not work yet
                unsigned int k = this->size();
                T lsq=static_cast<T>(0.0), lsq2=static_cast<T>(0.0);
                if (k != v.size()) return false; 
                for (unsigned int j = 0; j<k; j++) {
                    lsq+= ((*this)[j]-v[j])*((*this)[j]-v[j]);
                    lsq2+= ((*this)[j])*((*this)[j]);
                }
                if (lsq/lsq2 > epsilon) {return false;}
                return true;
            }
};

typedef ImpreciseVector<double> VectorType;
typedef std::vector<VectorType> GeneratorList;
typedef std::set<VectorType> Orbit;
enum errorTypes {NotImplemented, DimensionError, InputError, DotProdNotDefined, RenderError};

void simple_roots(const char& type, const unsigned int& dim, GeneratorList& normals); //forward declaration of function
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

void simple_roots(const char& type, const unsigned int& dim, GeneratorList& normals)
{
   double tmpEntry;
   normals.clear();

   switch(type) { 
       case 'a': case 'A':
           for (unsigned int i = 0; i<dim; i++) {
               VectorType tmpVector (dim, 0.0);
               for (unsigned int j = 0; j<dim+1; j++) {
                   if (i==j) tmpVector[i]=1.0;
                   if (i==j-1) tmpVector[i]=-1;
               }
               normals.push_back(tmpVector);
           }
           break;

       case 'b': case 'B':
          for (unsigned int i = 0; i<dim; i++) {
              VectorType tmpVector(dim, 0.0); 
               for (unsigned int j = 0; j<dim; j++) {
                   if (i==j) tmpVector[j] = 1.0; 
                   else if (i==j-1) tmpVector[j] = -1.0;
               }
               normals.push_back(tmpVector);
           }
           break;

       case 'd': case 'D': 
           {
           for (unsigned int i = 0; i<dim-1; i++) {
              VectorType tmpVector(dim, 0.0); 
               for (unsigned int j = 0; j<dim; j++) {
                   if (i==j) tmpVector[j] = 1.0; 
                   else if (i==j-1) tmpVector[j] = -1.0;
               }
               normals.push_back(tmpVector);
           }
           VectorType tmpVector2 (dim, 0.0);
           tmpVector2[dim-1]=1;
           tmpVector2[dim-2]=1;
           normals.push_back(tmpVector2);
           break;
           }

           //other diagrams not yet implemented

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

    GeneratorList readingBufferNewPoints, writingBufferNewPoints; 
    readingBufferNewPoints.push_back(v);

    unsigned int compositionLength=1000;

    for (unsigned int i = 0; i<compositionLength; i++) {
        if (readingBufferNewPoints.size()==0) break;
        for (unsigned int j = 0; j<readingBufferNewPoints.size(); j++) { //iterate through all new points
            for (unsigned int k=0; k<generators.size(); k++) { //reflect each individual new point in all planes; having functions being called for comparison every iteration probably bad idea but it looks cleaner
                VectorType tmpPoint;
                reflect(generators[k], readingBufferNewPoints[j], tmpPoint);
                //now check if new creation is already in pointOrbit, if not add it to the pointOrbit and to the newPointBuffer that will be read from in the next iteration of i
                bool inOrbit = false;
                for (std::set<VectorType>::iterator it=pointOrbit.begin(); it!=pointOrbit.end(); it++) {
                    if (tmpPoint==(*it)) {//approximate comparison
                        inOrbit = true;
                        break; //I hope this breaks the lit loop and not the if statement
                    }
                }
                if (!inOrbit) { 
                    pointOrbit.insert(tmpPoint);
                    writingBufferNewPoints.push_back(tmpPoint);
                }
            }
        }
        std::swap(writingBufferNewPoints, readingBufferNewPoints);
        writingBufferNewPoints.clear();
    }
    return pointOrbit;
}


#endif // __ORBIT_H_
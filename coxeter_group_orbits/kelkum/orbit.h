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
#include <algorithm>
const static double epsilon = 0.0000001; 
//#include "generators.h"

template<typename T> //only numeric types please
class ImpreciseVector: public std::vector<T> {
    public:
        ImpreciseVector() {}
        ImpreciseVector(unsigned int a, T iniValue) { //constructor not inherited, need to write it again
            this->resize(a, iniValue);
        }
        bool operator== (const ImpreciseVector& v) { 
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

        bool operator< (const ImpreciseVector& v) const { 
            unsigned int k = this->size();
            T lsq=static_cast<T>(0.0), lsq2=static_cast<T>(0.0);
            for (unsigned int j = 0; j<k; j++) {
                if ((*this)[j] < v[j]-epsilon)
                    return true; 
                else
                    if ((*this)[j] > v[j]+epsilon)
                        return false;
            }
            return false;
        }
};

typedef ImpreciseVector<double> VectorType;
typedef std::vector<VectorType> GeneratorList; 
typedef std::set<VectorType> Orbit;

enum errorTypes {NotImplemented, DimensionError, InputError, DotProdNotDefined};

void simple_roots(const char& type, const int& dim, GeneratorList& normals); //forward declaration of function
Orbit genOrbit(const GeneratorList& generators, const VectorType& v); //forward declaration of function

Orbit giveOrbit(const std::string& coxeterDiagram, VectorType& inputPoint) {
    std::stringstream ss; 
    ss << coxeterDiagram;
    char diagramType;
    int normalNumber;

    ss >> diagramType >> normalNumber; //not sure but it seems to work
    int dimensionPoint = inputPoint.size(); 

    //checking/correcting input ambiguities
    if (dimensionPoint != normalNumber || normalNumber<=0) {
        throw DimensionError;
    }
    //dotproduct with normals needs to make sense
    if (diagramType == 'a' || diagramType == 'A' || (diagramType == 'G' & normalNumber == 2)) inputPoint.push_back(0.0); 

    GeneratorList normalVectors;
    simple_roots(diagramType, normalNumber, normalVectors); //modifies the normals Variable to get all 
                                                            //the normals corresponding to a certain 
                                                            //Coxeter diagram into the normals "matrix"
    return genOrbit(normalVectors, inputPoint);
}

//long function (architecture of the switch statement should probably not have the computations 
//in it for readability) the function clears and modifies the normals variable that it is 
//given as input
void simple_roots(const char& type, const int& dim, GeneratorList& normals)
{
   normals.clear();
   VectorType individualVector(dim, 0.0); //this is sometimes used instead of local declarations to avoid writing {}

   switch(type) { 

       case 'a': case 'A':

        //Read rowwise, these simple root vectors are
        //1 -1  0 0 ... 0  0
        //0  1 -1 0 ... 0  0
        //...
        //0  0  0 0 ... 1 -1
        //In particular, they lie in the plane (sum of coordinates = 0)
            
        for (int i = 0; i<dim; i++) {
            VectorType tmpVector (dim+1, 0.0);
            for (int j = 0; j<dim+1; j++) {
                if (i==j) tmpVector[i]=1.0;
                if (i==j-1) tmpVector[i]=-1;
            }
            normals.push_back(tmpVector);
        }
        break;

       case 'b': case 'B':

        //Read rowwise, these simple root vectors are
        //1 -1  0 0 ... 0  0
        //0  1 -1 0 ... 0  0
        //...
        //0  0  0 0 ... 1 -1
        //0  0  0 0 ... 0  1

        //The Dynkin diagram is:
          
        //0 ---- 1 ---- ... ---- n-2 --(4)--> n-1,

        for (int i = 0; i<dim; i++) {
            VectorType tmpVector(dim, 0.0); 
            for (int j = 0; j<dim; j++) {
                if (i==j) tmpVector[j] = 1.0; 
                else if (i==j-1) tmpVector[j] = -1.0;
            }
            normals.push_back(tmpVector);
        }
        break;

       case 'c': case 'C':
           //Read rowwise, these simple root vectors are
           //1 -1  0 0 ... 0  0
           //0  1 -1 0 ... 0  0
           //...
           //0  0  0 0 ... 1 -1
           //0  0  0 0 ... 0  2
           //The Dynkin diagram is:
           //0 ---- 1 ---- ... ---- n-2 <--(4)-- n-1,

           for (int i = 0; i<dim-1; i++) {
              VectorType tmpVector(dim, 0.0); 
               for (int j = 0; j<dim; j++) {
                   if (i==j) tmpVector[j] = 1.0; 
                   else if (i==j-1) tmpVector[j] = -1.0;
               }
               normals.push_back(tmpVector);
           }
           individualVector[dim-1]=2;
           normals.push_back(individualVector);
           break;

       case 'd': case 'D': 
           //Read rowwise, these simple root vectors are
           //1 -1  0 0 ... 0 0
           //0  1 -1 0 ... 0 0
           //...
           //0  0  0 0 ... 1 -1
           //0  0  0 0 ... 1  1
           //The indexing of the Dynkin diagram is

           //                      n-2
           //                      /
           //0 - 1 - 2 - ... - n-3
           //                      \
           //                      n-1

           for (int i = 0; i<dim-1; i++) {
              VectorType tmpVector(dim, 0.0); 
               for (int j = 0; j<dim; j++) {
                   if (i==j) tmpVector[j] = 1.0; 
                   else if (i==j-1) tmpVector[j] = -1.0;
               }
               normals.push_back(tmpVector);
           }
           if ((dim-1)>=0) individualVector[dim-1]=1; 
           if ((dim-2)>=0) individualVector[dim-2]=1; //for dim=1 the loop before is skipped completely but there is no individualVector[dim-2]
           normals.push_back(individualVector);
           break;

       case 'e': case 'E': 
           switch(dim) {
               case 6:
                    //Read rowwise, these simple root vectors are
                    //     1 -1  0  0  0  0
                    //     0  1 -1  0  0  0
                    //     0  0  1 -1  0  0
                    //     0  0  0  1 -1  0
                    //     0  0  0  1  1  0
                    //-1/2(1  1  1  1  1 -sqrt(3))  
                    // 
                    //     The indexing of the Dynkin diagram is
                    //                   3
                    //                   |
                    //                   |
                    //     0 ---- 1 ---- 2 ---- 4 ---- 5
                    for (int i = 0; i<dim-2; i++) {
                        VectorType tmpVector(dim, 0.0); 
                        for (int j = 0; j<dim; j++) {
                            if (i==j) tmpVector[j] = 1.0; 
                            else if (i==j-1) tmpVector[j] = -1.0;
                        }
                        normals.push_back(tmpVector);
                    }
                    individualVector[dim-2]=1;
                    individualVector[dim-3]=1;
                    normals.push_back(individualVector);
                    for (int i=0; i<dim-1;i++) individualVector[i]=-0.5;
                    individualVector[dim-1] = sqrt(3.0)/2;
                    normals.push_back(individualVector);
                   break;
               case 7: {
                    //Read rowwise, these simple root vectors are
                    //     1 -1  0  0  0  0  0
                    //     0  1 -1  0  0  0  0
                    //     0  0  1 -1  0  0  0
                    //     0  0  0  1 -1  0  0
                    //     0  0  0  0  1 -1  0
                    //     0  0  0  0  1  1  0
                    //-1/2(1  1  1  1  1  1 -sqrt(2))  
                    // 
                    //     The indexing of the Dynkin diagram is
                    //                          4
                    //                          |
                    //                          |
                    //     0 ---- 1 ---- 2 ---- 3 ---- 5 ---- 6
                   for (int i = 0; i<dim-2; i++) {
                        VectorType tmpVector(dim, 0.0); 
                        for (int j = 0; j<dim; j++) {
                            if (i==j) tmpVector[j] = 1.0; 
                            else if (i==j-1) tmpVector[j] = -1.0;
                        }
                        normals.push_back(tmpVector);
                    }
                    VectorType tmpVector1(dim,0.0);
                    tmpVector1[dim-2]=1;
                    tmpVector1[dim-3]=1;
                    normals.push_back(tmpVector1);
                    
                    VectorType tmpVector2(dim,-0.5);
                    tmpVector2[dim-1]=sqrt(2.0)/2.0;
                    normals.push_back(tmpVector2);
                   break;
               }

               case 8: {
                    /*Read rowwise, these simple root vectors are
                         1 -1  0 0 0 0  0 0
                         0  1 -1 0 0 0  0 0
                         ...
                         0  0  0 0 0 1 -1 0
                         0  0  0 0 0 1  1 0
                    -1/2(1  1  1 1 1 1  1 1) */ 
                   for (int i = 0; i<dim-2; i++) {
                        VectorType tmpVector(dim, 0.0); 
                        for (int j = 0; j<dim; j++) {
                            if (i==j) tmpVector[j] = 1.0; 
                            else if (i==j-1) tmpVector[j] = -1.0;
                        }
                        normals.push_back(tmpVector);
                    }
                   VectorType tmpVector1(dim,0.0);
                   tmpVector1[dim-1]=1.0;
                   tmpVector1[dim-2]=1.0;
                   normals.push_back(tmpVector1);
                   VectorType tmpVector2(dim, -0.5);
                   normals.push_back(tmpVector2);
                   break;
               }
               default:
                   throw NotImplemented;
           }
           break;

       case 'f': case 'F':
           switch(dim) {
            case 4:
                //Read rowwise, these simple root vectors are
                //1    -1     0    0
                //0     1    -1    0
                //0     0     1    0
                //-1/2  -1/2  -1/2 -1/2
                //The Dynkin diagram is:
                //0 ---- 1 --(4)--> 2 ---- 3
                normals.resize(4,individualVector); //4 4-component 0 vectors
                normals[0][0]=normals[1][1]=normals[2][2]=1.0;
                normals[0][1]=normals[1][2]=-1.0;
                normals[3][0]=normals[3][1]=normals[3][2]=normals[3][3]=-0.5;
                break;
            default: throw NotImplemented;
           }
           break;
           
       case 'g': case 'G':
           switch(dim) {
                case 2: {          
                     //Read rowwise, these simple root vectors are
                     // 1 -1  0
                     //-1  2 -1
                     //Notice that each row sums to zero.
                     //The Dynkin diagram is:
                     //0 <--(6)-- 1
                    VectorType tmpVector(3,0.0);
                    normals.resize(2,tmpVector); 
                    normals[0][0]=1.0;
                    normals[0][1]=normals[1][0]=normals[1][2]=-1.0;
                    normals[1][1]=2.0;
                }
                break;
                default: throw NotImplemented;
           }
           break;

       case 'h': case 'H':
           switch(dim) {
               case 3: {
                   const double tau=0.5+0.5*sqrt(5.0); //golden ratio
                     //For H_3, the Dynkin diagram is
                     //0 --(5)-- 1 ---- 2,
                     //and the simple root vectors are, 
                     // 2 0 0
                     // a b -1
                     // 0 0 2
                     // with a=-tau and b=1/tau. Notice they all have length 2.
                   normals.resize(3,individualVector); //3 times a 3 component 0 vector
                   normals[0][0]=normals[2][2]=2.0;
                   normals[1][0]=-tau;
                   normals[1][1]=1/tau;
                   normals[1][2]=-1.0;
                   break;
               }
               case 4: {           
                     //For H_4, the Dynkin diagram is
                     //0 --(5)-- 1 ---- 2 ---- 3,
                     //and the simple root vectors are, according to 
                     //[John H. Stembridge, A construction of H_4 without miracles, 
                     // Discrete Comput. Geom. 22, No.3, 425-427 (1999)],
                     //  a  b  b  b
                     // -1  1  0  0
                     //  0 -1  1  0
                     //  0  0 -1  1
                     // with a=(1+tau)/2 and b=(1-tau)/2, so that the length of each root is sqrt{2}.
                   const double tau=0.5+0.5*sqrt(5.0);
                   normals.resize(4,individualVector); //4 times a 4 component 0 vector
                   normals[0][0]=(1+tau)/2;
                   normals[0][1]=normals[0][2]=normals[0][3]=(1-tau)/2;
                   normals[1][0]=normals[2][1]=normals[3][2]=-1.0;
                   normals[1][1]=normals[2][2]=normals[3][3]=1.0;
                   break;
               }
               default: throw NotImplemented;
           }
           break;
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

//requires a VectorType as input that it can write the result of the reflection to, 
//to try to avoid copying and reassigning as this is the function used the most often
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
    //in this current version no advantage of the set (that its ordered, quick search) 
    //is used only the disadvantages (slow insertion) hence bad idea
    pointOrbit.insert(v);
    GeneratorList readingBufferNewPoints, writingBufferNewPoints; 
    readingBufferNewPoints.push_back(v);

    while(readingBufferNewPoints.size()!=0) {
        for (unsigned int j = 0; j<readingBufferNewPoints.size(); j++) { //iterate through all new points
            //reflect each individual new point in all planes
            for (unsigned int k=0; k<generators.size(); k++) {
                VectorType tmpPoint;
                reflect(generators[k], readingBufferNewPoints[j], tmpPoint);
                //now check if new creation is already in pointOrbit, if not add it to the pointOrbit and to 
                //newPointBuffer that will be read from in the next iteration of i
                bool inOrbit = false;

                //the following would yield better runtime but is not correct as it does not use the == operator in the class,
                //need to define a <(VectorType 1,VectorType v2) operator to use it

                std::set<VectorType>::iterator it = pointOrbit.find(tmpPoint);
                it = pointOrbit.find(tmpPoint);
                if (it != pointOrbit.end()) inOrbit = true;

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
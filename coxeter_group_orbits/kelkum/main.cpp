/* 
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
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <array>
#include <vector>
#include <iomanip> 
#include "orbit.h"

int main() {
    std::string coxeterDiagram = "";
    VectorType inputPoint; //see orbit.h for what this type exactly is
    Orbit pointOrbit;  //same
    double coord; 
    unsigned int orbitLength;
    bool showOrbit;  
    bool renderOrbit;

    try {
        //input
        //assumes file is in the right format eg "I5\n1.0,1.0,1.0,1.0,1.0", no checking if input is sensable and no real parsing over ambiguities is done
        std::fstream file ("input.txt"); 
        std::stringstream tmpss;
        std::string tmpLine;

        if (file.is_open()) {
            std::getline(file, tmpLine);
            coxeterDiagram = tmpLine;

            while(std::getline(file, tmpLine, ',')) {
                tmpss.clear();
                tmpss << tmpLine;
                tmpss >> coord;
                inputPoint.push_back(coord);
            }
            file.close();
        } else {
            throw InputError;
        }

        //processing
        //function is in orbit.h
        pointOrbit = giveOrbit(coxeterDiagram, inputPoint);
        orbitLength = pointOrbit.size(); 
    } catch(errorTypes& e) {
        std::cerr << "Errorcode " << e << '\n';
        return static_cast<int>(e);
    }

        //output
        std::cout << "Orbit size: " << orbitLength << "\n show orbit? Y=1, N=0: "; 
        std::cin >> showOrbit;
        if(showOrbit) {
            std::set<VectorType>::iterator iter; 
            for (iter=pointOrbit.begin(); iter!=pointOrbit.end(); iter++) {
                std::cout << "( ";
                for (unsigned int j=0; j<(*iter).size()-1; j++) {
                    int a=0;
                    a++;
                    std::cout << std::setprecision(5) << (*iter)[j] << ',';
                }
                std::cout << std::setprecision(5)  << (*iter).size()-1 << ")\n";
            }
            if (inputPoint.size() == 3 || inputPoint.size() == 2) {
                std::cout << "Render Orbit? Y=1, N=0: ";
                std::cin >> renderOrbit; 
                if (renderOrbit) {
                    //..
                }
            }
            int a;
            std::cin>>a;

        }
        return 0;
}


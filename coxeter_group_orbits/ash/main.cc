#include <fstream>
#include <stdio.h>
#include <time.h>
#include "orbit.h"
#include "test_orbitSize.h"

int main(int arg, const char* argv[]){
	time_t start;
	time_t end;
 
	std::ofstream f ("CoexeterCalculationTimes.txt");
////////////////////////////////////////////////////////////
//Coxeter Group B
	//B3
	GeneratorList g = simple_roots('B', 3);
	VectorType v = getVectorGeneralPosition('B',3);
	time(&start);
	Orbit o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B3: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B4
	g = simple_roots('B', 4);
	v = getVectorGeneralPosition('B',4);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B5
	g = simple_roots('B', 5);
	v = getVectorGeneralPosition('B',5);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B5: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B6
	g = simple_roots('B', 6);
	v = getVectorGeneralPosition('B',6);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B6: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B7
	g = simple_roots('B', 7);
	v = getVectorGeneralPosition('B',7);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B7: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B8
	g = simple_roots('B', 8);
	v = getVectorGeneralPosition('B',8);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group B8: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
/////////////////////////////////////////////////////////////////////
//Coxeter Group D
	//D3
	g = simple_roots('D', 3);
	v = getVectorGeneralPosition('D',3);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group D3: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//D4
	g = simple_roots('D', 4);
	v = getVectorGeneralPosition('D',4);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group D4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//D5
	g = simple_roots('D', 5);
	v = getVectorGeneralPosition('D',5);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group D5: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//D6
	g = simple_roots('D', 6);
	v = getVectorGeneralPosition('D',6);
	time(&start);
	o = orbit(g,v);
	time(&end);
	f << "Coxeter Group D6: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
////////////////////////////////////////////////////////////
//Coxeter Group E 
	//E6
	g = simple_roots('E', 6);
	v = getVectorGeneralPosition('E',6);
	time(&start);
	//Orbit o = orbit(g,v);
	o = orbit(g,{1.0,2.0,3.0,4.0,5.0,6.0});
	time(&end);
	f << "Coxeter Group E6: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//E7
	g = simple_roots('E', 7);
	v = getVectorGeneralPosition('E',7);
	time(&start);
	//o = orbit(g, v);
	o = orbit(g,{1.0,2.0,3.0,4.0,5.0,6.0,7.0});
	time(&end);
	f << "Coxeter Group E7: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	/*E8
	g = simple_roots('E', 8);
	time(&start);
	o = orbit(g, {1,2,3,4,5,6,7,8});
	time(&end);
	f1 << "Coxeter Group E8: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";*/
////////////////////////////////////////////////////////////
//Coxeter Group F
	//F4
	g = simple_roots('F', 4);
	v = getVectorGeneralPosition('F',4);
	time(&start);
	o = orbit(g, v);
	time(&end);
	f << "Coxeter Group F4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
//////////////////////////////////////////////////////////
//Coxeter Group H
	//H3
	g = simple_roots('H', 3);
        v = getVectorGeneralPosition('H',3);
	time(&start);
	o = orbit(g, v);
	time(&end);
	f << "Coxeter Group H3: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//H4
	g = simple_roots('H', 4);
        v = getVectorGeneralPosition('H',4);
	time(&start);
	o = orbit(g, v);
	time(&end);
	f << "Coxeter Group H4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
/////////////////////////////////////////////////////////
	f.close();
}

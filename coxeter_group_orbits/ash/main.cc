#include <fstream>
#include <stdio.h>
#include <time.h>
#include "orbit.h"
#include "test_orbitSize.h"

int main(int arg, const char* argv[]){
	time_t start;
	time_t end;
 

////////////////////////////////////////////////////////////
//Coxeter Group B
	/*std::ofstream f ("timesGroupB.txt");
	//B3
	GeneratorList g = simple_roots('B', 3);
	time(&start);
	Orbit o = orbit(g, {1,2,3});
	time(&end);
	f << "Coxeter Group B3: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B4
	g = simple_roots('B', 4);
	time(&start);
	o = orbit(g, {1,2,3,4});
	time(&end);
	f << "Coxeter Group B4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B4
	g = simple_roots('B', 5);
	time(&start);
	o = orbit(g, {1,2,3,4,5});
	time(&end);
	f << "Coxeter Group B5: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B5
	g = simple_roots('B', 6);
	time(&start);
	o = orbit(g, {1,2,3,4,5,6});
	time(&end);
	f << "Coxeter Group B6: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//B6
	g = simple_roots('B', 7);
	time(&start);
	o = orbit(g, {1,2,3,4,5,6,7});
	time(&end);
	f << "Coxeter Group B7: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	f.close();
////////////////////////////////////////////////////////////
//Coxeter Group E*/
	std::ofstream f1 ("timesGroupE.txt");
	//E6
	GeneratorList g = simple_roots('E', 6);
	VectorType v = getVectorGeneralPosition('E',6);
	time(&start);
	Orbit o = orbit(g,v);
	time(&end);
	f1 << "Coxeter Group E6: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	/*//E7
	g = simple_roots('E', 7);
	v = getVectorGeneralPosition('E',7);
	time(&start);
	o = orbit(g, v);
	time(&end);
	f1 << "Coxeter Group E7: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//E8
	g = simple_roots('E', 8);
	time(&start);
	o = orbit(g, {1,2,3,4,5,6,7,8});
	time(&end);
	f1 << "Coxeter Group E8: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	*/f1.close();
////////////////////////////////////////////////////////////
//Coxeter Group F
	/*std::ofstream f2 ("timesGroupF.txt");
	//F4
	g = simple_roots('F', 4);
	time(&start);
	o = orbit(g, {1,2,3,4});
	time(&end);
	f2 << "Coxeter Group F4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	f2.close();
////////////////////////////////////////////////////////////
//Coxeter Group H
	std::ofstream f3 ("timesGroupH.txt");
	//H3
	g = simple_roots('H', 3);
	time(&start);
	o = orbit(g, {1,2,3});
	time(&end);
	f3 << "Coxeter Group H3: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	//H4
	g = simple_roots('H', 4);
	time(&start);
	o = orbit(g, {1,2,3,4});
	time(&end);
	f3 << "Coxeter Group H4: " << difftime(end, start) << " sec - size: " << o.size() <<"\n";
	f3.close();*/
//////////////////////////////////////////////////////////
}

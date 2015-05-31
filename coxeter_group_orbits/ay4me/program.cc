#include "orbit.h"
#include <fstream>


int main()
{   
	GeneratorList generators;
	VectorType v;
	input("file.txt", v, generators);
	Orbit generatedOrbit = orbit(generators, v);
	std::ofstream file;
	file.open ("out.txt");
	out(file, generatedOrbit, true);

}

// Local Variables:
// mode:C++
// c-basic-offset:3
// indent-tabs-mode:nil
// End:

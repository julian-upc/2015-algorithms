#include <fstream>
#include <stdio.h>
#include <time.h>
#include "orbit.h"
#include "test_orbitSize.h"

int main(int arg, const char* argv[]){
	checkOrbitSize('B', 2, 2);
	checkOrbitSize('B', 3, 3);
	checkOrbitSize('B', 4, 2);
	checkOrbitSize('B', 4, 3);
	checkOrbitSize('B', 5, 2);
	checkOrbitSize('B', 5, 3);
	checkOrbitSize('B', 5, 4);
	checkOrbitSize('B', 6, 3);
	checkOrbitSize('B', 7, 2);
	checkOrbitSize('B', 7, 3);
}

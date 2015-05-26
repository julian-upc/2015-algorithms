#include <fstream>
#include <sstream>
#include <string>

int main()
{  
    std::ifstream input("data");
    std::ofstream output("result");
    std::string normalVector;
    
    if (input.is_open() && output.is_open()) {
	while (std::getline(input,normalVector)) {
	    output << normalVector << std::endl;
	}
    }
     
    return 0;   
}
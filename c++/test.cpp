#include <iostream>
#include <vector>
#include <string>
#include <fstream>

using namespace std;

int main(){
	vector <int> loVect(10);
	int loNumArray[5] = {4,23,34,12,11};
	loVect.insert(loVect.begin(),loNumArray,loNumArray+4);
	loVect.insert(loVect.begin()+5,44);

	cout<< loVect.at(5) <<endl;

	loVect.push_back(64);

	cout << "Final value "<<loVect.back();

	return 0;
}
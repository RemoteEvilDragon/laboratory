#include <iostream>
#include <string>

using namespace std;


class Employee{
	private:
		const int default_int = 11;
		const string default_name = "athen";

		string name;
		int id;
	public:
		Employee(const int &_id,const string &_name):name(_name),id(_id){
		};

		Employee():Employee(default_int,default_name)
		{  
		};

		Employee(const int &_id):Employee(_id,default_name)
		{  
		};

		Employee(const string &_name):Employee(default_int,_name)
		{  
		};

		void print(){
			cout<<"My id is "<<id<<"!\n";
			cout<<"My name is "<<name<<"!\n\n";
		};
};

int main(int argc,char* argv[])
{
	const int id = 689;
	 const string name = "alex";

	Employee e1;
	Employee e2(id);
	Employee e3(name);
	Employee e4(id,name);

	e1.print();
	e2.print();
	e3.print();
	e4.print();

    return 0;
}
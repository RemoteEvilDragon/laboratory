#include <iostream>
#include <string>

using namespace std;
 
 class simple{
    private:
        int _mean;
    public:
        simple(int value=2):_mean=value{

        };

        simple(Simple const && s){
            
        };


 };

 void printAnother(unsigned int & para){
    cout<<para<<endl;
 }

 void printSpecial(unsigned int && para){
    printAnother(para);
 }

int main()
{
    unsigned int a =3;

    unsigned int& b = a;

    unsigned int&& c = a;

    cout<<c<<endl;

    // unsigned int& c = b;

    // printSpecial(b);
    // printAnother(a);

    simple s1(3);

    return 0;
}
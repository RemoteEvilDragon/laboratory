#include <iostream>
#include <string>

using namespace std;

class Something
{
private:
    static int s_idGenerator;
    int m_id;
 
public:
    Something() { m_id = s_idGenerator++; } // grab the next value from the id generator
 
    int getID() const { return m_id; }

    int getValue() {return s_idGenerator;}
};
 
// Note that we're defining and initializing s_idGenerator even though it is declared as private above.
// This is okay since the definition isn't subject to access controls.
int Something::s_idGenerator = 1; // start our ID generator with value 1
 
int main()
{
    Something first;
    Something second;
    Something third;
 
    std::cout << first.getID() << '\n';
    std::cout << second.getID() << '\n';
    std::cout << third.getID() << '\n';

    cout<<first.getValue()<<endl;
    return 0;
}
#include <iostream>
#include <string>

using namespace std;

class Calculator{
	private:
		int m_value;
		

	public:
		Calculator(int value):m_value(value){
		};

		Calculator& add(int value){
			m_value += value;
			return *this;
		};

		Calculator& sub(int value){
			m_value -= value;
			return *this;
		};

		Calculator& multi(int value){
			m_value *= value;
			return *this;
		};

		Calculator& divide(int value);
		// {
		// 	m_value /= value;
		// 	return *this;
		// }

		inline int getResult()  {
			return m_value;
		};
};

Calculator& Calculator::divide(int value) {
	m_value /= value;
	return *this;
}

int main(int argc,char* argv[])
{
	Calculator cal(2);

	cout<< cal.add(4).sub(1).multi(4).divide(2).getResult() <<endl;

    return 0;
}
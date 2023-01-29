#include <iostream>

#include <string>
using namespace std;
int main()
{
    string a = "";
    for (int i = 0; i < 5; i++)
    {
        a += to_string(i);
    }
    cout << a << endl;
}
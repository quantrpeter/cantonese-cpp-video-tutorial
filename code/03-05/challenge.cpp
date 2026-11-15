#include <iostream>

int main() {
    int coins{3};
    int& a = coins;
    int& b = coins;
    a = a * 10;
    std::cout << coins << ' ' << a << ' ' << b << '\n';
}

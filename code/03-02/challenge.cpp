#include <iostream>

int cube(int x) {
    return x * x * x;
}

bool isEven(int n) {
    return n % 2 == 0;
}

int main() {
    std::cout << cube(3) << '\n';
    std::cout << isEven(10) << ' ' << isEven(7) << '\n';
}

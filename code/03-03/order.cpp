#include <iostream>

int square(int x);
int cube(int x);

int main() {
    std::cout << square(7) << '\n';
    std::cout << cube(3) << '\n';
}

int square(int x) {
    return x * x;
}

int cube(int x) {
    return x * square(x);
}

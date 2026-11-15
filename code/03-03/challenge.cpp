#include <iostream>

int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);

int main() {
    std::cout << add(6, 3) << ' ' << subtract(6, 3) << ' ' << multiply(6, 3) << '\n';
}

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

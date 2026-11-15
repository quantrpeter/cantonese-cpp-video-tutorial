#include <iostream>

int main() {
    int a{1};
    int b{2};
    double d{3.5};
    char c{'A'};
    std::cout << "a: " << &a << '\n';
    std::cout << "b: " << &b << '\n';
    std::cout << "d: " << &d << '\n';
    std::cout << "c: " << static_cast<void*>(&c) << '\n';
}

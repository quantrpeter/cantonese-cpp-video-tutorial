#include <iostream>

int main() {
    int a{1};
    int b{2};
    int& r = a;
    int* p = &a;
    std::cout << r << ' ' << *p << '\n';
    r = b;
    std::cout << "a: " << a << '\n';
    p = &b;
    *p = 20;
    std::cout << "b: " << b << '\n';
    p = nullptr;
    std::cout << (p == nullptr) << '\n';
}

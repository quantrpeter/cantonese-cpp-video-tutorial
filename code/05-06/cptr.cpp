#include <iostream>

int main() {
    int a{1};
    int b{2};
    const int* p = &a;
    p = &b;
    int* const q = &a;
    *q = 10;
    std::cout << *p << ' ' << a << '\n';
}

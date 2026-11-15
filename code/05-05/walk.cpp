#include <iostream>

int main() {
    int marks[5]{72, 85, 64, 91, 58};
    int* p = marks;
    std::cout << *p << ' ' << *(p + 2) << '\n';
    std::cout << p[3] << '\n';
    std::cout << p << ' ' << p + 1 << '\n';
    for (int* q = marks; q != marks + 5; q++) {
        std::cout << *q << ' ';
    }
    std::cout << '\n';
}

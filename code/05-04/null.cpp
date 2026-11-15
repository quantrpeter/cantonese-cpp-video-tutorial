#include <iostream>

int main() {
    int* p = nullptr;
    std::cout << "Before\n";
    if (p != nullptr) {
        std::cout << *p << '\n';
    } else {
        std::cout << "p is null\n";
    }
    std::cout << "After\n";
}

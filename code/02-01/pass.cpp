#include <iostream>

int main() {
    int mark{};
    std::cout << "Mark: ";
    std::cin >> mark;
    if (mark == 100) {
        std::cout << "Full marks!\n";
    }
    if (mark >= 50) {
        std::cout << "Pass\n";
    } else {
        std::cout << "Fail\n";
    }
}

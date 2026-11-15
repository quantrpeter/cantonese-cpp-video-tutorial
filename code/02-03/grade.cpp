#include <iostream>

int main() {
    int mark{};
    std::cout << "Mark: ";
    std::cin >> mark;
    if (mark >= 85) {
        std::cout << "A\n";
    } else if (mark >= 70) {
        std::cout << "B\n";
    } else if (mark >= 55) {
        std::cout << "C\n";
    } else if (mark >= 40) {
        std::cout << "D\n";
    } else {
        std::cout << "F\n";
    }
}

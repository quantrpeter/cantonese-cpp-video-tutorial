#include <iostream>

int main() {
    int mark{};
    std::cout << "Mark: ";
    std::cin >> mark;
    if (mark >= 50) {
        std::cout << "Pass\n";
        std::cout << "Well done!\n";
        if (mark >= 85) {
            std::cout << "Excellent!\n";
        }
    }
}

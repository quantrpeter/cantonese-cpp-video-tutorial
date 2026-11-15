#include <iostream>

int main() {
    int mark{-1};
    do {
        std::cout << "Mark (0-100): ";
        if (!(std::cin >> mark)) {
            std::cin.clear();
            std::cin.ignore(1000, '\n');
            mark = -1;
        }
    } while (mark < 0 || mark > 100);
    std::cout << "OK: " << mark << '\n';
}

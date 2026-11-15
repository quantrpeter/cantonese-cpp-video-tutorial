#include <iostream>

int main() {
    int choice{};
    std::cout << "1) Tea 2) Coffee 3) Milk tea\n";
    std::cout << "Choice: ";
    std::cin >> choice;
    switch (choice) {
    case 3:
        std::cout << "Milk + ";
        [[fallthrough]];
    case 1:
        std::cout << "Tea\n";
        break;
    case 2:
        std::cout << "Coffee\n";
        break;
    default:
        std::cout << "No such drink\n";
    }
}

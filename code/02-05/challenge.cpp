#include <iostream>

int main() {
    int a{};
    int b{};
    std::cout << "Two numbers: ";
    std::cin >> a >> b;
    int bigger = a > b ? a : b;
    std::cout << "Bigger: " << bigger << '\n';
}

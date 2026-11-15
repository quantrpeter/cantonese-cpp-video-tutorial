#include <iostream>
#include <numbers>

int main() {
    constexpr double pi = std::numbers::pi;
    double r{};
    std::cout << "Radius: ";
    std::cin >> r;
    double area = pi * r * r;
    double length = 2 * pi * r;
    std::cout << area << ' ' << length << '\n';
}

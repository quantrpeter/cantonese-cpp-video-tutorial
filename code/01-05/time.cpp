#include <iostream>

int main() {
    int total{};
    std::cout << "Seconds: ";
    std::cin >> total;

    int hours = total / 3600;
    int minutes = total % 3600 / 60;
    int seconds = total % 60;

    std::cout << hours << "h ";
    std::cout << minutes << "m ";
    std::cout << seconds << "s\n";
}

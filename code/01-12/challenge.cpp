#include <iostream>
#include <iomanip>

int main() {
    constexpr double cmPerM = 100.0;
    constexpr double low = 18.5;
    constexpr double high = 22.9;
    double cm{};
    std::cout << "Height (cm): ";
    std::cin >> cm;

    double m = cm / cmPerM;
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Healthy weight: " << low * m * m << " - "
              << high * m * m << " kg\n";
}

#include <iostream>
#include <iomanip>

int main() {
    constexpr double cmPerM = 100.0;
    double kg{};
    std::cout << "Weight (kg): ";
    std::cin >> kg;
    double cm{};
    std::cout << "Height (cm): ";
    std::cin >> cm;

    double m = cm / cmPerM;
    double bmi = kg / (m * m);
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "BMI: " << bmi << '\n';
}

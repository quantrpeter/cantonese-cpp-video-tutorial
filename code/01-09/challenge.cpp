#include <iostream>

int main() {
    constexpr long long daysPerYear = 365;
    constexpr long long secondsPerDay = 24 * 60 * 60;
    constexpr long long secondsPerYear = daysPerYear * secondsPerDay;
    std::cout << secondsPerYear << '\n';
}

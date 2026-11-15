#include <iostream>
#include <iomanip>
#include <cmath>

int main() {
    double sum = 0.1 + 0.2;
    std::cout << sum << '\n';
    std::cout << (sum == 0.3) << '\n';
    std::cout << std::setprecision(17);
    std::cout << sum << '\n';
    double diff = std::abs(sum - 0.3);
    std::cout << (diff < 1e-9) << '\n';
}

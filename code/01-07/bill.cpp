#include <iostream>
#include <iomanip>

int main() {
    double tea{19.5};
    double bun{9.8};
    double tart{8.6};
    double total = tea + bun + tart;
    std::cout << "Total: $" << total << '\n';
    std::cout << std::fixed;
    std::cout << std::setprecision(2);
    std::cout << "Total: $" << total << '\n';
}

#include <iostream>
#include <iomanip>

int main() {
    double bill{100};
    double each = bill / 3;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Each: $" << each << '\n';
}

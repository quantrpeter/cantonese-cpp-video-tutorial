#include <iostream>

int main() {
    auto a = 80;
    auto b = 95;
    auto avg = static_cast<double>(a + b) / 2;
    std::cout << "Average: " << avg << '\n';
}

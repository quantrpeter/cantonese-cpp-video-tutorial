#include <iostream>

int main() {
    int total{0};
    int n{};
    std::cout << "Number (0 to stop): ";
    std::cin >> n;
    while (n != 0) {
        total += n;
        std::cout << "Number (0 to stop): ";
        std::cin >> n;
    }
    std::cout << "Total: " << total << '\n';
}

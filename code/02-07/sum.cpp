#include <iostream>

int main() {
    int n{};
    std::cout << "n: ";
    std::cin >> n;
    int total{0};
    for (int i = 1; i <= n; i++) {
        std::cout << i << ' ';
        total += i;
    }
    std::cout << "\nSum: " << total << '\n';
}

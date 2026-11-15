#include <iostream>

int main() {
    int total{0};
    while (true) {
        int n{};
        std::cout << "Number: ";
        std::cin >> n;
        if (n == 0) {
            break;
        }
        if (n < 0) {
            continue;
        }
        total += n;
    }
    std::cout << "Total: " << total << '\n';
}

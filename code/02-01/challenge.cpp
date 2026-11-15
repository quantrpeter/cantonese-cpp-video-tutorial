#include <iostream>

int main() {
    int n{};
    std::cout << "Number: ";
    std::cin >> n;
    if (n % 2 == 0) {
        std::cout << "Even\n";
    } else {
        std::cout << "Odd\n";
    }
}

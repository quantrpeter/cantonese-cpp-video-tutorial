#include <iostream>

int main() {
    int cents{};
    std::cout << "Cents: ";
    std::cin >> cents;
    std::cout << cents / 100 << " dollars ";
    std::cout << cents % 100 << " cents\n";
}

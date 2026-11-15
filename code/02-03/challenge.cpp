#include <iostream>

int main() {
    int temp{};
    std::cout << "Temperature: ";
    std::cin >> temp;
    if (temp >= 30) {
        std::cout << "Hot\n";
    } else if (temp >= 20) {
        std::cout << "Warm\n";
    } else {
        std::cout << "Cold\n";
    }
}

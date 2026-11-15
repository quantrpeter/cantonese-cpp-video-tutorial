#include <iostream>

int main() {
    char small{};
    std::cout << "Letter: ";
    std::cin >> small;
    char big = static_cast<char>(small - 32);
    std::cout << big << '\n';
}

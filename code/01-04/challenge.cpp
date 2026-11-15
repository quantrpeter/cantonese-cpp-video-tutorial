#include <iostream>

int main() {
    int a{};
    int b{};
    int c{};
    std::cout << "Three numbers: ";
    std::cin >> a >> b >> c;
    std::cout << "Sum: " << a + b + c << '\n';
}

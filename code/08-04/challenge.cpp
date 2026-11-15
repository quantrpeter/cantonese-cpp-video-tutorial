#include <iostream>
#include <utility>

std::pair<int, int> divide(int a, int b) {
    return {a / b, a % b};
}

int main() {
    auto [q, r] = divide(17, 5);
    std::cout << q << ' ' << r << '\n';
}

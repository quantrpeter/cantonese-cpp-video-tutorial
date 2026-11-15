#include <iostream>

template <typename... Ts>
bool allPositive(Ts... args) {
    return ((args > 0) && ...);
}

int main() {
    std::cout << allPositive(1, 2, 3) << ' ' << allPositive(1, -2) << '\n';
}

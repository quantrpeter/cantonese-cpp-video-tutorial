#include <iostream>

#define SQUARE(x) x * x

constexpr int square(int x) {
    return x * x;
}

int main() {
    std::cout << SQUARE(1 + 2) << ' ';
    std::cout << square(1 + 2) << '\n';
#ifdef DEBUG
    std::cout << "debug build\n";
#endif
}

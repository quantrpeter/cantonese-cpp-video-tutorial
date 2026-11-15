#include <iostream>

template <typename T>
T minOf(T a, T b) {
    if (a < b) {
        return a;
    }
    return b;
}

int main() {
    std::cout << minOf(4, 9) << '\n';
    std::cout << minOf('x', 'b') << '\n';
    std::cout << minOf<double>(1, 0.5) << '\n';
}

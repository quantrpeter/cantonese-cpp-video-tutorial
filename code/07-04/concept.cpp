#include <concepts>
#include <iostream>

template <typename T>
concept Comparable = requires(T a, T b) {
    a > b;
};

template <Comparable T>
T maxOf(T a, T b) {
    if (a > b) {
        return a;
    }
    return b;
}

template <std::integral T>
bool isEven(T n) {
    return n % 2 == 0;
}

struct Point {
    int x;
    int y;
};

int main() {
    std::cout << maxOf(3, 7) << ' ' << isEven(10) << '\n';
}

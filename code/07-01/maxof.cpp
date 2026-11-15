#include <iostream>
#include <string>

template <typename T>
T maxOf(T a, T b) {
    if (a > b) {
        return a;
    }
    return b;
}

int main() {
    std::cout << maxOf(3, 7) << '\n';
    std::cout << maxOf(2.5, 1.5) << '\n';
    std::string x = "apple", y = "banana";
    std::cout << maxOf(x, y) << '\n';
    std::cout << maxOf<double>(3, 2.5) << '\n';
}

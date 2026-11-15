#include <iostream>

template <typename... Ts>
auto sum(Ts... args) {
    return (0 + ... + args);
}

template <typename... Ts>
void print(const Ts&... args) {
    std::cout << sizeof...(args) << ": ";
    ((std::cout << args << ' '), ...);
    std::cout << '\n';
}

int main() {
    std::cout << sum(1, 2) << ' ' << sum(1, 2, 3, 4) << '\n';
    std::cout << sum(1.5, 2, 3) << ' ' << sum() << '\n';
    print("Amy", 72, 'A', 3.5);
}

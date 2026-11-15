#include <iostream>
#include <string>
#include <type_traits>

constexpr int square(int x) {
    return x * x;
}

consteval int cube(int x) {
    return x * x * x;
}

template <typename T>
void describe(const T& value) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << "number " << value * 2 << '\n';
    } else {
        std::cout << "text " << value.size() << '\n';
    }
}

int main() {
    static_assert(square(4) == 16);
    std::cout << square(5) << ' ' << cube(3) << '\n';
    describe(21);
    describe(std::string{"hello"});
}

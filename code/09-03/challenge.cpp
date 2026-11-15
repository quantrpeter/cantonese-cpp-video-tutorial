#include <iostream>
#include <type_traits>

struct Safe {
    Safe() = default;
    Safe(Safe&&) noexcept {}
};

struct Risky {
    Risky() = default;
    Risky(Risky&&) {}
};

int main() {
    std::cout << std::is_nothrow_move_constructible_v<Safe> << ' '
              << std::is_nothrow_move_constructible_v<Risky> << '\n';
}

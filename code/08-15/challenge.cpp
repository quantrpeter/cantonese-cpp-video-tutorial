#include <iostream>
#include <ranges>

int main() {
    auto even = [](int x) { return x % 2 == 0; };
    auto square = [](int x) { return x * x; };
    for (int x : std::views::iota(1, 20) | std::views::filter(even)
                     | std::views::transform(square) | std::views::take(3)) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

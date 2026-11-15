#include <algorithm>
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    std::vector<int> m{72, 45, 91, 58, 64};
    std::ranges::sort(m);
    for (int x : m) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
    auto pass = [](int x) { return x >= 60; };
    auto plus5 = [](int x) { return x + 5; };
    auto good = m | std::views::filter(pass)
                  | std::views::transform(plus5);
    for (int x : good) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
    m[2] = 100;
    for (int x : good) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

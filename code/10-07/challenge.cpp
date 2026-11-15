#include <chrono>
#include <iostream>
#include <vector>

int main() {
    using namespace std::chrono;
    const int n = 4000;
    std::vector<std::vector<int>> grid(n, std::vector<int>(n, 1));
    auto t0 = steady_clock::now();
    long long sum = 0;
    for (const auto& row : grid) {
        for (int x : row) {
            sum += x;
        }
    }
    auto took = duration_cast<milliseconds>(steady_clock::now() - t0);
    std::cout << sum << ' ' << (took < 5s) << '\n';
}

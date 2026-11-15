#include <iostream>
#include <vector>

int main() {
    std::vector<int> marks{72, 45, 64, 30};
    int total{0};
    for (const auto& m : marks) {
        total += m;
    }
    for (auto& m : marks) {
        if (m < 50) {
            m = 50;
        }
    }
    std::cout << total << '\n';
    for (const auto& m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
}

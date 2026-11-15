#include <iostream>
#include <vector>

int main() {
    std::vector<int> marks{72, 85, 64};
    for (int m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
    for (auto& m : marks) {
        m = m * 2;
    }
    for (const auto& m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
}

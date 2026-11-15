#include <iostream>
#include <vector>

int findIndex(const std::vector<int>& v, int target) {
    for (std::size_t i = 0; i < v.size(); i++) {
        if (v[i] == target) {
            return static_cast<int>(i);
        }
    }
    return -1;
}

int main() {
    std::vector<int> marks{72, 45, 91, 64, 85};
    std::cout << findIndex(marks, 64) << '\n';
    std::cout << findIndex(marks, 50) << '\n';
}

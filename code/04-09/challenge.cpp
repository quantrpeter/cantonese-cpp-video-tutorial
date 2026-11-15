#include <iostream>
#include <utility>
#include <vector>

void bubbleSortDesc(std::vector<int>& v) {
    for (std::size_t pass = 1; pass < v.size(); pass++) {
        for (std::size_t i = 0; i + pass < v.size(); i++) {
            if (v[i] < v[i + 1]) {
                std::swap(v[i], v[i + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> marks{72, 45, 91, 64, 85};
    bubbleSortDesc(marks);
    for (int m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
}

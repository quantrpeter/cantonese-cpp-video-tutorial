#include <iostream>
#include <vector>

int main() {
    std::vector<int> marks{72, 64, 91};
    for (auto it = marks.rbegin(); it != marks.rend(); ++it) {
        std::cout << *it << ' ';
    }
    std::cout << '\n';
}

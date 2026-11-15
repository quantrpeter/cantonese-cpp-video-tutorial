#include <iostream>
#include <vector>

int main() {
    std::vector<int> marks;
    int m{};
    while (std::cin >> m && m >= 0) {
        marks.push_back(m);
    }
    int best = marks[0];
    for (std::size_t i = 1; i < marks.size(); i++) {
        if (marks[i] > best) {
            best = marks[i];
        }
    }
    std::cout << "Best: " << best << '\n';
}

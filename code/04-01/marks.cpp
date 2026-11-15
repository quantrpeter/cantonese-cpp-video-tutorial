#include <iostream>
#include <vector>

int main() {
    std::vector<int> marks;
    int m{};
    std::cout << "Marks (-1 to end): ";
    while (std::cin >> m && m >= 0) {
        marks.push_back(m);
    }
    std::cout << "Count: " << marks.size() << '\n';
    std::cout << "First: " << marks[0] << '\n';
    int total{0};
    for (std::size_t i = 0; i < marks.size(); i++) {
        total += marks[i];
    }
    double avg = static_cast<double>(total) / marks.size();
    std::cout << "Average: " << avg << '\n';
}

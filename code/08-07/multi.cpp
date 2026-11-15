#include <iostream>
#include <set>

int main() {
    std::multiset<int> marks{72, 64, 72, 91, 72};
    std::cout << marks.count(72) << '\n';
    marks.erase(marks.find(72));
    for (int m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
    marks.erase(72);
    std::cout << marks.size() << '\n';
}

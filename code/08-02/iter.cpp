#include <iostream>
#include <iterator>
#include <list>
#include <vector>

int main() {
    std::vector<int> marks{72, 64, 91};
    for (auto it = marks.begin(); it != marks.end(); ++it) {
        std::cout << *it << ' ';
    }
    std::cout << '\n';
    auto it = marks.begin();
    *it = 80;
    it += 2;
    std::cout << marks[0] << ' ' << *it << '\n';
    std::list<int> nums{1, 2, 3};
    auto lt = nums.begin();
    ++lt;
    std::cout << *lt << ' ' << *std::next(lt) << '\n';
}

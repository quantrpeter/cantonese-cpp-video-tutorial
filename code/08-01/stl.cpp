#include <algorithm>
#include <iostream>
#include <list>
#include <string>
#include <vector>

int main() {
    std::vector<int> marks{72, 64, 91, 64};
    std::list<int> queue{3, 1, 3, 3};
    std::string word = "banana";
    auto a = std::count(marks.begin(), marks.end(), 64);
    auto b = std::count(queue.begin(), queue.end(), 3);
    auto c = std::count(word.begin(), word.end(), 'a');
    std::cout << a << ' ' << b << ' ' << c << '\n';
    std::sort(marks.begin(), marks.end());
    for (int m : marks) {
        std::cout << m << ' ';
    }
    std::cout << '\n';
}

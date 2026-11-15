#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    auto square = [](int x) { return x * x; };
    std::cout << square(5) << '\n';
    std::vector<int> marks{72, 45, 91, 58};
    int pass = 50;
    auto n = std::count_if(marks.begin(), marks.end(),
                           [pass](int m) { return m >= pass; });
    std::cout << n << '\n';
    int total = 0;
    std::for_each(marks.begin(), marks.end(),
                  [&total](int m) { total += m; });
    std::cout << total << '\n';
    int bonus = 5;
    auto byValue = [bonus](int m) { return m + bonus; };
    auto byRef = [&bonus](int m) { return m + bonus; };
    bonus = 100;
    std::cout << byValue(70) << ' ' << byRef(70) << '\n';
}

#include <algorithm>
#include <iostream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

std::pair<int, int> minMax(const std::vector<int>& v) {
    int lo = v[0];
    int hi = v[0];
    for (int x : v) {
        lo = std::min(lo, x);
        hi = std::max(hi, x);
    }
    return {lo, hi};
}

std::tuple<std::string, int, char> top() {
    return {"Amy", 91, 'A'};
}

int main() {
    std::vector<int> marks{72, 58, 91};
    std::pair<int, int> p = minMax(marks);
    std::cout << p.first << ' ' << p.second << '\n';
    auto [lo, hi] = minMax(marks);
    std::cout << lo << ' ' << hi << '\n';
    auto [name, mark, grade] = top();
    std::cout << name << ' ' << mark << ' ' << grade << '\n';
    std::vector<std::pair<std::string, int>> list{
        {"Ben", 64}, {"Cat", 80}};
    for (const auto& [n, m] : list) {
        std::cout << n << '=' << m << ' ';
    }
    std::cout << '\n';
}

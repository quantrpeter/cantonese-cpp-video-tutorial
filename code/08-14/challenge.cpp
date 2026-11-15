#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> m{45, 58, 62, 72, 72, 79, 91};
    auto a = std::lower_bound(m.begin(), m.end(), 60);
    auto b = std::lower_bound(m.begin(), m.end(), 80);
    std::cout << b - a << '\n';
}

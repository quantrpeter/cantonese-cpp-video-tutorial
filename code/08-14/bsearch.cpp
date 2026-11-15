#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> m{45, 58, 72, 72, 72, 91};
    bool has72 = std::binary_search(m.begin(), m.end(), 72);
    bool has60 = std::binary_search(m.begin(), m.end(), 60);
    std::cout << has72 << ' ' << has60 << '\n';
    auto lo = std::lower_bound(m.begin(), m.end(), 72);
    auto hi = std::upper_bound(m.begin(), m.end(), 72);
    std::cout << lo - m.begin() << ' ';
    std::cout << hi - m.begin() << ' ' << hi - lo << '\n';
    auto pos = std::lower_bound(m.begin(), m.end(), 60);
    m.insert(pos, 60);
    for (int x : m) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

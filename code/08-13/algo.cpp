#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> m{72, 45, 91, 58, 45};
    auto it = std::find(m.begin(), m.end(), 91);
    std::cout << "91 at " << (it - m.begin()) << '\n';
    int total = std::accumulate(m.begin(), m.end(), 0);
    auto lo = std::min_element(m.begin(), m.end());
    std::cout << total << ' ' << *lo << '\n';
    std::transform(m.begin(), m.end(), m.begin(),
                   [](int x) { return x + 5; });
    m.erase(std::remove(m.begin(), m.end(), 50), m.end());
    for (int x : m) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

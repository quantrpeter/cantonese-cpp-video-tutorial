#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> m{72, 45, 91, 58, 45};
    auto n = std::count(m.begin(), m.end(), 45);
    std::erase(m, 45);
    std::cout << n << ' ' << m.size() << '\n';
}

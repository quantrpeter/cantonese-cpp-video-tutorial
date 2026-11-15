#include <iostream>
#include <limits>

int main() {
    std::cout << std::numeric_limits<int>::min() << ' '
              << std::numeric_limits<int>::max() << '\n'
              << std::numeric_limits<long long>::min() << ' '
              << std::numeric_limits<long long>::max() << '\n';
}

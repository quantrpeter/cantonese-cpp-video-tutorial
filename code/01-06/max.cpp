#include <iostream>
#include <limits>

int main() {
    int big = std::numeric_limits<int>::max();
    std::cout << big << '\n';
    big = big + 1;
    std::cout << big << '\n';
}

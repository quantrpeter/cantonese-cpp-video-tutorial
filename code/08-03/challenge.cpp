#include <iostream>
#include <vector>

int main() {
    std::vector<int> v(9, 1);
    v.clear();
    std::cout << v.size() << ' ' << v.capacity() << '\n';
    v.shrink_to_fit();
    std::cout << v.size() << ' ' << v.capacity() << '\n';
}

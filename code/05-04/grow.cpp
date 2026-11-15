#include <iostream>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    int* p = &v[0];
    std::cout << *p << '\n';
    v.push_back(4);
    p = &v[0];
    std::cout << *p << '\n';
}

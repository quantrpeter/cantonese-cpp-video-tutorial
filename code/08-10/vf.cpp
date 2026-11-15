#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    for (int i = 0; i < 200000; i++) {
        v.insert(v.begin(), i);
    }
    std::cout << v.front() << '\n';
}

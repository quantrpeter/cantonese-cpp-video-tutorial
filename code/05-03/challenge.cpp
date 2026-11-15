#include <iostream>
#include <vector>

int* findNegative(std::vector<int>& v) {
    for (auto& x : v) {
        if (x < 0) {
            return &x;
        }
    }
    return nullptr;
}

int main() {
    std::vector<int> v{3, 8, -4, 5};
    int* p = findNegative(v);
    if (p != nullptr) {
        std::cout << "Found " << *p << '\n';
    } else {
        std::cout << "None\n";
    }
}

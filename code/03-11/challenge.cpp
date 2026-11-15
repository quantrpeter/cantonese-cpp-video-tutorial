#include <iostream>

namespace shapes {
    int area(int w, int h) {
        return w * h;
    }
}

int main() {
    std::cout << shapes::area(4, 6) << '\n';
}

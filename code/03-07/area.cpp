#include <iostream>

int area(int side) {
    return side * side;
}

int area(int width, int height) {
    return width * height;
}

int main() {
    std::cout << area(5) << '\n';
    std::cout << area(4, 6) << '\n';
}

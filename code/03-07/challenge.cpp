#include <iostream>

int biggest(int a, int b) {
    return a > b ? a : b;
}

int biggest(int a, int b, int c) {
    return biggest(biggest(a, b), c);
}

int main() {
    std::cout << biggest(3, 8) << ' ' << biggest(3, 8, 5) << '\n';
}

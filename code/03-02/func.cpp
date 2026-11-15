#include <iostream>

int square(int x) {
    return x * x;
}

int max3(int a, int b, int c) {
    int best = a;
    if (b > best) {
        best = b;
    }
    if (c > best) {
        best = c;
    }
    return best;
}

int main() {
    std::cout << square(5) << '\n';
    int area = square(12);
    std::cout << area << '\n';
    std::cout << max3(7, 42, 19) << '\n';
}

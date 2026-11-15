#include <iostream>

void swapPtr(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x{1};
    int y{2};
    swapPtr(&x, &y);
    std::cout << x << ' ' << y << '\n';
}

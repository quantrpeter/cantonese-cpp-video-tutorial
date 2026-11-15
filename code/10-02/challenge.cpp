#include <iostream>

#define MAX(a, b) ((a) > (b) ? (a) : (b))

int main() {
    int i = 5;
    int m = MAX(i++, 3);
    std::cout << m << ' ' << i << '\n';
}

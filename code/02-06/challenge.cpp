#include <iostream>

int main() {
    int i{1};
    int total{0};
    while (i <= 100) {
        total += i;
        i++;
    }
    std::cout << total << '\n';
}

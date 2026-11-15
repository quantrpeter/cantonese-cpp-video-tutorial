#include <cassert>
#include <iostream>

int percent(int part, int whole) {
    assert(whole > 0 && "whole must be positive");
    assert(part >= 0 && part <= whole);
    return part * 100 / whole;
}

int main() {
    static_assert(sizeof(long long) == 8);
    std::cout << percent(3, 4) << '\n';
}

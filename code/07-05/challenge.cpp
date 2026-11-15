#include <iostream>

constexpr long long factorial(int n) {
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    static_assert(factorial(5) == 120);
    std::cout << factorial(10) << '\n';
}

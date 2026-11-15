#include <chrono>
#include <iostream>

int main() {
    using namespace std::chrono;
    auto start = steady_clock::now();
    long long sum = 0;
    for (long long i = 1; i <= 10000000; i++) {
        sum += i;
    }
    auto took = duration_cast<milliseconds>(steady_clock::now() - start);
    std::cout << sum << ' ' << (took < 5s) << '\n';
}

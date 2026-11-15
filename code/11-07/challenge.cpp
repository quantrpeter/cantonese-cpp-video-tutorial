#include <algorithm>
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>

bool isPrime(int n) {
    if (n < 2) {
        return false;
    }
    for (int d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            return false;
        }
    }
    return true;
}

int countPrimes(int limit, int threads) {
    std::atomic<int> count{0};
    std::atomic<int> next{0};
    std::vector<std::jthread> workers;
    for (int t = 0; t < threads; t++) {
        workers.emplace_back([&count, &next, limit] {
            int mine = 0;
            while (true) {
                int start = next.fetch_add(1000);
                if (start >= limit) {
                    break;
                }
                int end = std::min(start + 1000, limit);
                for (int n = start; n < end; n++) {
                    if (isPrime(n)) {
                        mine++;
                    }
                }
            }
            count += mine;
        });
    }
    workers.clear();
    return count;
}

int main() {
    using namespace std::chrono;
    const int limit = 3'000'000;
    for (int threads : {8}) {
        auto t0 = steady_clock::now();
        int found = countPrimes(limit, threads);
        auto took = steady_clock::now() - t0;
        std::cout << threads << " threads: " << found << ' '
                  << duration_cast<milliseconds>(took) << '\n';
    }
}

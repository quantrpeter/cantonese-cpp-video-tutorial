#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    std::atomic<int> evens{0};
    {
        std::vector<std::jthread> workers;
        for (int t = 0; t < 4; t++) {
            workers.emplace_back([&evens, t] {
                for (int i = t * 250; i < (t + 1) * 250; i++) {
                    if (i % 2 == 0) {
                        evens++;
                    }
                }
            });
        }
    }
    std::cout << evens << '\n';
}

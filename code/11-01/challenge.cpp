#include <iostream>
#include <thread>
#include <vector>

int main() {
    std::vector<int> results(4);
    {
        std::vector<std::jthread> workers;
        for (int i = 0; i < 4; i++) {
            workers.emplace_back([&results, i] {
                results[i] = i * i;
            });
        }
    }
    for (int r : results) {
        std::cout << r << ' ';
    }
    std::cout << '\n';
}

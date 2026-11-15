#include <future>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> v(1'000'000, 2);
    std::vector<std::future<long long>> parts;
    std::size_t step = v.size() / 4;
    for (std::size_t k = 0; k < 4; k++) {
        parts.push_back(std::async(std::launch::async, [&v, k, step] {
            return std::accumulate(v.begin() + k * step, v.begin() + (k + 1) * step, 0LL);
        }));
    }
    long long total = 0;
    for (auto& f : parts) {
        total += f.get();
    }
    std::cout << total << '\n';
}

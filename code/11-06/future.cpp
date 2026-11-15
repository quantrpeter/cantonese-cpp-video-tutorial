#include <future>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <thread>
#include <vector>

long long sumRange(const std::vector<int>& v, std::size_t from,
                   std::size_t to) {
    return std::accumulate(v.begin() + from, v.begin() + to, 0LL);
}

int main() {
    std::vector<int> v(10'000'000, 1);
    std::size_t half = v.size() / 2;
    auto left = std::async(std::launch::async, [&] {
        return sumRange(v, 0, half);
    });
    long long right = sumRange(v, half, v.size());
    std::cout << left.get() + right << '\n';
    auto bad = std::async(std::launch::async, []() -> int {
        throw std::runtime_error("oops");
    });
    try {
        bad.get();
    } catch (const std::exception& e) {
        std::cout << "caught " << e.what() << '\n';
    }
    std::promise<int> p;
    std::future<int> f = p.get_future();
    std::jthread t([&p] { p.set_value(42); });
    std::cout << f.get() << '\n';
}

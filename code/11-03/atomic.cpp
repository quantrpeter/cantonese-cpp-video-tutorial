#include <atomic>
#include <chrono>
#include <iostream>
#include <mutex>
#include <thread>

std::atomic<int> fast{0};
int slow = 0;
std::mutex m;

void addFast() {
    for (int i = 0; i < 1000000; i++) {
        fast++;
    }
}

void addSlow() {
    for (int i = 0; i < 1000000; i++) {
        std::scoped_lock lock(m);
        slow++;
    }
}

int main() {
    using namespace std::chrono;
    auto t0 = steady_clock::now();
    {
        std::jthread a(addFast), b(addFast);
    }
    auto t1 = steady_clock::now();
    {
        std::jthread a(addSlow), b(addSlow);
    }
    auto t2 = steady_clock::now();
    auto ms = [](auto d) { return duration_cast<milliseconds>(d); };
    std::cout << "atomic " << fast << ' ' << ms(t1 - t0) << '\n';
    std::cout << "mutex  " << slow << ' ' << ms(t2 - t1) << '\n';
}

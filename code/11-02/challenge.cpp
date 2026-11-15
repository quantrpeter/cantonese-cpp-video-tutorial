#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

std::vector<int> entries;
std::mutex m;

void add(int from) {
    for (int i = 0; i < 1000; i++) {
        std::scoped_lock lock(m);
        entries.push_back(from + i);
    }
}

int main() {
    {
        std::jthread a(add, 0);
        std::jthread b(add, 10000);
    }
    std::cout << entries.size() << '\n';
}

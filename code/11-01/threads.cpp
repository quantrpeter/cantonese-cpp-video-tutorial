#include <chrono>
#include <iostream>
#include <thread>

void count(const char* name, int n) {
    for (int i = 1; i <= n; i++) {
        std::cout << name << i << ' ' << std::flush;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main() {
    {
        std::jthread a(count, "A", 3);
        std::jthread b(count, "B", 3);
    }
    std::cout << "\ndone\n";
}

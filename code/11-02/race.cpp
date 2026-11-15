#include <iostream>
#include <mutex>
#include <thread>

int counter = 0;
std::mutex m;

void work() {
    for (int i = 0; i < 100000; i++) {
        std::lock_guard<std::mutex> lock(m);
        counter++;
    }
}

int main() {
    {
        std::jthread a(work);
        std::jthread b(work);
    }
    std::cout << counter << '\n';
}

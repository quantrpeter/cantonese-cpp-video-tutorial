#include <chrono>
#include <iostream>
#include <mutex>
#include <thread>

std::mutex a, b;

void first() {
    std::scoped_lock both(a, b);
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    std::cout << "first done\n";
}

void second() {
    std::scoped_lock both(b, a);
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    std::cout << "second done\n";
}

int main() {
    {
        std::jthread t1(first), t2(second);
    }
    std::cout << "all done\n";
}

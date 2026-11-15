#include <chrono>
#include <iostream>
#include <thread>

int main() {
    using namespace std::chrono;
    seconds s{90};
    milliseconds ms = s;
    auto m = duration_cast<minutes>(s);
    std::cout << s << ' ' << ms << ' ' << m << '\n';
    auto start = steady_clock::now();
    std::this_thread::sleep_for(250ms);
    auto end = steady_clock::now();
    auto took = duration_cast<milliseconds>(end - start);
    std::cout << took << '\n';
}

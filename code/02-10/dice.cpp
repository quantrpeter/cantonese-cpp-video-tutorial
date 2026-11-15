#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dice(1, 6);
    for (int i = 0; i < 5; i++) {
        std::cout << dice(gen) << ' ';
    }
    std::cout << '\n';
}

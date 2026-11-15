#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dice(1, 6);
    int a = dice(gen);
    int b = dice(gen);
    std::cout << a << " + " << b << " = " << a + b << '\n';
    if (a == b) {
        std::cout << "Double!\n";
    }
}

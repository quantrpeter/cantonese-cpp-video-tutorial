#include <iostream>

struct Timer {
    Timer() {
        std::cout << "start\n";
    }
    ~Timer() {
        std::cout << "stop\n";
    }
};

int main() {
    std::cout << "before\n";
    {
        Timer t;
        std::cout << "inside\n";
    }
    std::cout << "after\n";
}

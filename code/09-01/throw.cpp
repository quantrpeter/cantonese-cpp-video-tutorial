#include <iostream>
#include <stdexcept>
#include <string>

struct Guard {
    std::string name;
    ~Guard() {
        std::cout << "~" << name << '\n';
    }
};

double divide(int a, int b) {
    Guard g{"divide"};
    if (b == 0) {
        throw std::runtime_error("divide by zero");
    }
    return static_cast<double>(a) / b;
}

int main() {
    try {
        Guard g{"main"};
        std::cout << divide(7, 2) << '\n';
        std::cout << divide(1, 0) << '\n';
        std::cout << "never\n";
    } catch (const std::runtime_error& e) {
        std::cout << "caught: " << e.what() << '\n';
    }
    std::cout << "still running\n";
}

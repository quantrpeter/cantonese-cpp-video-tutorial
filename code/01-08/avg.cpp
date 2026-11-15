#include <iostream>

int main() {
    int a{80};
    int b{95};
    double avg = static_cast<double>(a + b) / 2;
    std::cout << "Average: " << avg << '\n';
}

#include <iostream>

void work(int n) {
    int* data = new int[n];
    std::cout << "  get " << n << '\n';
    if (n > 3) {
        std::cout << "  too big, return early\n";
        return;
    }
    std::cout << "  working\n";
    delete[] data;
    std::cout << "  give back\n";
}

int main() {
    std::cout << "work(2):\n";
    work(2);
    std::cout << "work(5):\n";
    work(5);
}

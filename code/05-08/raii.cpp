#include <iostream>

struct Buffer {
    int* data;
    Buffer(int n) {
        data = new int[n];
        std::cout << "  get " << n << '\n';
    }
    ~Buffer() {
        delete[] data;
        std::cout << "  give back\n";
    }
};

void work(int n) {
    Buffer buf(n);
    if (n > 3) {
        std::cout << "  too big, return early\n";
        return;
    }
    std::cout << "  working\n";
}

int main() {
    std::cout << "work(2):\n";
    work(2);
    std::cout << "work(5):\n";
    work(5);
}

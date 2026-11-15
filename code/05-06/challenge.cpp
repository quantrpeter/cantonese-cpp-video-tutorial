#include <iostream>

void printAll(const int* a, int n) {
    for (int i = 0; i < n; i++) {
        std::cout << a[i] << ' ';
    }
    std::cout << '\n';
}

int main() {
    int marks[3]{72, 85, 64};
    printAll(marks, 3);
}

#include <iostream>

void printAll(const int a[], int n) {
    for (int i = 0; i < n; i++) {
        std::cout << a[i] << ' ';
    }
    std::cout << '\n';
}

int main() {
    int marks[5]{72, 85, 64, 91, 58};
    int n = sizeof(marks) / sizeof(marks[0]);
    std::cout << "In main: " << n << '\n';
    printAll(marks, n);
}

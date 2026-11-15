#include <iostream>

int sum(const int a[], int n) {
    int total{0};
    for (int i = 0; i < n; i++) {
        total += a[i];
    }
    return total;
}

int main() {
    int marks[5]{72, 85, 64, 91, 58};
    std::cout << sum(marks, 5) << '\n';
}

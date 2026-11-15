#include <iostream>

int main() {
    int n{};
    std::cin >> n;
    double* temps = new double[n];
    double total{0};
    for (int i = 0; i < n; i++) {
        std::cin >> temps[i];
        total += temps[i];
    }
    std::cout << "Average: " << total / n << '\n';
    delete[] temps;
}

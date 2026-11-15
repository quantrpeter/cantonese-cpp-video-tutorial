#include <iostream>

int main() {
    int* p = new int{42};
    std::cout << *p << '\n';
    delete p;

    int n{};
    std::cout << "How many: ";
    std::cin >> n;
    int* arr = new int[n];
    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << ' ';
    }
    std::cout << '\n';
    delete[] arr;
}

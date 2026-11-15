#include <iostream>

int main() {
    int n{};
    std::cout << "Rows: ";
    std::cin >> n;
    for (int row = 1; row <= n; row++) {
        for (int col = 1; col <= row; col++) {
            std::cout << '*';
        }
        std::cout << '\n';
    }
}

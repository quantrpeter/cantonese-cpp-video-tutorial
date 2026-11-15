#include <iostream>

int main() {
    int n{};
    std::cout << "Rows: ";
    std::cin >> n;
    for (int row = n; row >= 1; row--) {
        for (int col = 1; col <= row; col++) {
            std::cout << '*';
        }
        std::cout << '\n';
    }
}

#include <iostream>
#include <vector>

int main() {
    const int n = 5;
    std::vector<std::vector<char>> grid(n, std::vector<char>(n, '.'));
    for (int i = 0; i < n; i++) {
        grid[i][i] = 'X';
    }
    for (const auto& line : grid) {
        for (char s : line) {
            std::cout << s << ' ';
        }
        std::cout << '\n';
    }
}

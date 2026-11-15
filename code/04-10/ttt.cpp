#include <iostream>
#include <vector>

using Grid = std::vector<std::vector<char>>;

void show(const Grid& g) {
    for (const auto& row : g) {
        for (char c : row) {
            std::cout << c << ' ';
        }
        std::cout << '\n';
    }
}

bool same(char a, char b, char c, char p) {
    return a == p && b == p && c == p;
}

bool wins(const Grid& g, char p) {
    for (int i = 0; i < 3; i++) {
        if (same(g[i][0], g[i][1], g[i][2], p)) {
            return true;
        }
        if (same(g[0][i], g[1][i], g[2][i], p)) {
            return true;
        }
    }
    return same(g[0][0], g[1][1], g[2][2], p) ||
           same(g[0][2], g[1][1], g[2][0], p);
}

int main() {
    Grid g(3, std::vector<char>(3, '.'));
    char player = 'X';
    int moves{0};
    while (moves < 9) {
        int r{};
        int c{};
        std::cout << player << " (row col): ";
        std::cin >> r >> c;
        if (r < 0 || r > 2 || c < 0 || c > 2) {
            std::cout << "Out of range!\n";
            continue;
        }
        if (g[r][c] != '.') {
            std::cout << "Taken!\n";
            continue;
        }
        g[r][c] = player;
        moves++;
        show(g);
        if (wins(g, player)) {
            std::cout << player << " wins!\n";
            return 0;
        }
        player = (player == 'X') ? 'O' : 'X';
    }
    std::cout << "Draw!\n";
}

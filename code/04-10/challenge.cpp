// Challenge: keep playing rounds and count each player's wins (answer sketch).
#include <iostream>
#include <vector>

using Grid = std::vector<std::vector<char>>;

bool same(char a, char b, char c, char p) {
    return a == p && b == p && c == p;
}

bool wins(const Grid& g, char p) {
    for (int i = 0; i < 3; i++) {
        if (same(g[i][0], g[i][1], g[i][2], p) || same(g[0][i], g[1][i], g[2][i], p)) {
            return true;
        }
    }
    return same(g[0][0], g[1][1], g[2][2], p) || same(g[0][2], g[1][1], g[2][0], p);
}

char playRound() {
    Grid g(3, std::vector<char>(3, '.'));
    char player = 'X';
    for (int moves = 0; moves < 9;) {
        int r{};
        int c{};
        if (!(std::cin >> r >> c)) {
            return '?';
        }
        if (r < 0 || r > 2 || c < 0 || c > 2 || g[r][c] != '.') {
            continue;
        }
        g[r][c] = player;
        moves++;
        if (wins(g, player)) {
            return player;
        }
        player = (player == 'X') ? 'O' : 'X';
    }
    return '-';
}

int main() {
    int x{0};
    int o{0};
    for (char w = playRound(); w != '?'; w = playRound()) {
        x += (w == 'X');
        o += (w == 'O');
        std::cout << "X " << x << " : " << o << " O\n";
    }
}

#include <bits/stdc++.h>
using namespace std;

int R, C;
vector<string> g;

void dfs(int r, int c, char id) {
    if (r < 0 || r >= R || c < 0 || c >= C || g[r][c] != '#') {
        return;
    }
    g[r][c] = id;
    dfs(r + 1, c, id);
    dfs(r - 1, c, id);
    dfs(r, c + 1, id);
    dfs(r, c - 1, id);
}

int main() {
    cin >> R >> C;
    g.resize(R);
    for (auto& row : g) {
        cin >> row;
    }
    int islands = 0;
    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            if (g[r][c] == '#') {
                islands++;
                dfs(r, c, '0' + islands);
            }
        }
    }
    for (const auto& row : g) {
        cout << row << '\n';
    }
    cout << islands << '\n';
}

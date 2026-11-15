#include <bits/stdc++.h>
using namespace std;
using P = pair<int, int>;

int main() {
    int R, C;
    cin >> R >> C;
    vector<string> g(R);
    for (auto& row : g) {
        cin >> row;
    }
    vector<vector<int>> dist(R, vector<int>(C, -1));
    vector<vector<P>> from(R, vector<P>(C));
    queue<P> q;
    q.push({0, 0});
    dist[0][0] = 0;
    int dr[] = {1, -1, 0, 0};
    int dc[] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) {
                continue;
            }
            if (g[nr][nc] == '#' || dist[nr][nc] != -1) {
                continue;
            }
            dist[nr][nc] = dist[r][c] + 1;
            from[nr][nc] = {r, c};
            q.push({nr, nc});
        }
    }
    int er = R - 1, ec = C - 1;
    cout << "steps " << dist[er][ec] << '\n';
    P cur = from[er][ec];
    while (cur != P{0, 0}) {
        g[cur.first][cur.second] = '*';
        cur = from[cur.first][cur.second];
    }
    for (const auto& row : g) {
        cout << row << '\n';
    }
}

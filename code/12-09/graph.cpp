#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<vector<bool>> mat(n + 1, vector<bool>(n + 1, false));
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
        mat[u][v] = mat[v][u] = true;
    }
    for (int u = 1; u <= n; u++) {
        cout << u << ':';
        for (int v : adj[u]) {
            cout << ' ' << v;
        }
        cout << '\n';
    }
    cout << mat[2][3] << ' ' << mat[3][4] << '\n';
}

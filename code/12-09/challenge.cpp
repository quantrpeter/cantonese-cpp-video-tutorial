#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    int best = 1;
    for (int u = 2; u <= n; u++) {
        if (adj[u].size() > adj[best].size()) {
            best = u;
        }
    }
    cout << best << ' ' << adj[best].size() << '\n';
}

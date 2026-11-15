#include <bits/stdc++.h>
using namespace std;
using P = pair<int, int>;

int main() {
    int n, m;
    cin >> n >> m;
    vector<string> name(n);
    for (auto& s : name) {
        cin >> s;
    }
    vector<vector<P>> adj(n);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    vector<int> dist(n, INT_MAX), from(n, -1);
    priority_queue<P, vector<P>, greater<P>> pq;
    dist[0] = 0;
    pq.push({0, 0});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) {
            continue;
        }
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                from[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    cout << dist[n - 1] << " min:";
    vector<int> path;
    for (int x = n - 1; x != -1; x = from[x]) {
        path.push_back(x);
    }
    for (int i = (int)path.size() - 1; i >= 0; i--) {
        cout << ' ' << name[path[i]];
    }
    cout << '\n';
}

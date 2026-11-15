#include <bits/stdc++.h>
using namespace std;

vector<int> parent;

int find(int x) {
    return parent[x] == x ? x : parent[x] = find(parent[x]);
}

int main() {
    int n = 4;
    parent.resize(n);
    iota(parent.begin(), parent.end(), 0);
    vector<array<int, 2>> edges{{0, 1}, {1, 2}, {2, 0}, {2, 3}};
    for (auto [a, b] : edges) {
        int ra = find(a), rb = find(b);
        if (ra == rb) {
            cout << "cycle at " << a << '-' << b << '\n';
        } else {
            parent[ra] = rb;
        }
    }
}

#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> parent, size;
    DSU(int n) : parent(n), size(n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) {
            return false;
        }
        if (size[a] < size[b]) {
            swap(a, b);
        }
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};

int main() {
    int n, q;
    cin >> n >> q;
    DSU d(n);
    int groups = n;
    while (q--) {
        char op;
        int a, b;
        cin >> op >> a >> b;
        if (op == 'U') {
            groups -= d.unite(a, b);
        } else {
            cout << (d.find(a) == d.find(b) ? "yes" : "no") << '\n';
        }
    }
    cout << "groups " << groups << '\n';
}

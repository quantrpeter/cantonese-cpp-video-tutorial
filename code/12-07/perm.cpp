#include <bits/stdc++.h>
using namespace std;

vector<int> cur;
vector<bool> used(4, false);

void permute(int n) {
    if ((int)cur.size() == n) {
        for (int x : cur) {
            cout << x;
        }
        cout << ' ';
        return;
    }
    for (int i = 1; i <= n; i++) {
        if (!used[i]) {
            used[i] = true;
            cur.push_back(i);
            permute(n);
            cur.pop_back();
            used[i] = false;
        }
    }
}

int main() {
    permute(3);
    cout << '\n';
}

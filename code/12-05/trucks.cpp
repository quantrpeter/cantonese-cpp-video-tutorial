#include <bits/stdc++.h>
using namespace std;

bool canShip(const vector<int>& w, int trucks, long long cap) {
    int used = 1;
    long long load = 0;
    for (int x : w) {
        if (load + x > cap) {
            used++;
            load = 0;
        }
        load += x;
    }
    return used <= trucks;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> w(n);
    for (auto& x : w) {
        cin >> x;
    }
    long long lo = *max_element(w.begin(), w.end());
    long long hi = accumulate(w.begin(), w.end(), 0LL);
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        bool ok = canShip(w, m, mid);
        cout << "try " << mid << (ok ? " ok" : " no") << '\n';
        if (ok) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    cout << "answer " << lo << '\n';
}

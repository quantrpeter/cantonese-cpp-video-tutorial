#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) {
        cin >> x;
    }
    long long sum = 0;
    int best = 0;
    int left = 0;
    for (int right = 0; right < n; right++) {
        sum += a[right];
        while (sum > k) {
            sum -= a[left];
            left++;
        }
        best = max(best, right - left + 1);
    }
    cout << best << '\n';
}

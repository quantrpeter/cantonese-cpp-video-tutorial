#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n = 1000000;
    long long lo = 0, hi = n;
    while (lo < hi) {
        long long mid = (lo + hi + 1) / 2;
        if (mid * mid <= n) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    cout << lo << '\n';
}

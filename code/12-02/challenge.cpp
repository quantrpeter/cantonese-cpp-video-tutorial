#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n = 100000;
    long long steps = n * n;
    cout << steps << ' ' << (steps <= 100000000 ? "ok" : "too slow") << '\n';
    long long logn = 17;
    cout << n * logn << ' ' << (n * logn <= 100000000 ? "ok" : "too slow") << '\n';
}

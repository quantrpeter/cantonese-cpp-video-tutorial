#include <bits/stdc++.h>
using namespace std;

int main() {
    const long long MOD = 1'000'000'007;
    long long fact = 1;
    for (int i = 1; i <= 100; i++) {
        fact = fact * i % MOD;
    }
    cout << fact << '\n';
}

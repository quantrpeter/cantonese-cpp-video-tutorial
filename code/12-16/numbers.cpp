#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1'000'000'007;

long long myGcd(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

long long power(long long base, long long exp) {
    long long result = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp & 1) {
            result = result * base % MOD;
        }
        base = base * base % MOD;
        exp >>= 1;
    }
    return result;
}

int main() {
    cout << myGcd(84, 36) << ' ' << gcd(84, 36) << ' ' << lcm(4, 6) << '\n';
    int n = 50;
    vector<bool> prime(n + 1, true);
    prime[0] = prime[1] = false;
    for (int i = 2; i * i <= n; i++) {
        if (prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                prime[j] = false;
            }
        }
    }
    for (int i = 2; i <= n; i++) {
        if (prime[i]) {
            cout << i << ' ';
        }
    }
    cout << '\n';
    long long x = 100000, y = 100000;
    cout << x * y % MOD << ' ' << power(2, 100) << '\n';
}

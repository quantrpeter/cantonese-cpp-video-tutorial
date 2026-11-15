#include <bits/stdc++.h>
using namespace std;

long long calls = 0;

long long plain(int n) {
    calls++;
    if (n <= 1) {
        return 1;
    }
    return plain(n - 1) + plain(n - 2);
}

vector<long long> memo(91, -1);

long long remember(int n) {
    calls++;
    if (n <= 1) {
        return 1;
    }
    if (memo[n] != -1) {
        return memo[n];
    }
    return memo[n] = remember(n - 1) + remember(n - 2);
}

long long table(int n) {
    vector<long long> dp(n + 1);
    dp[0] = dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

int main() {
    int n = 40;
    calls = 0;
    cout << "plain    " << plain(n) << " calls " << calls << '\n';
    calls = 0;
    cout << "remember " << remember(n) << " calls " << calls << '\n';
    cout << "table    " << table(n) << '\n';
    cout << "n=90     " << table(90) << '\n';
}

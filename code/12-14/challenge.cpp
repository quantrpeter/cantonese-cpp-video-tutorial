#include <bits/stdc++.h>
using namespace std;

int main() {
    int n = 10;
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int step : {1, 2, 3}) {
            if (i - step >= 0) {
                dp[i] += dp[i - step];
            }
        }
    }
    cout << dp[n] << '\n';
}

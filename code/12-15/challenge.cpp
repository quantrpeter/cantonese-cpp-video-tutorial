#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> coins{1, 3, 4};
    int amount = 6;
    vector<int> dp(amount + 1, INT_MAX);
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a && dp[a - c] != INT_MAX) {
                dp[a] = min(dp[a], dp[a - c] + 1);
            }
        }
    }
    cout << dp[amount] << '\n';
}

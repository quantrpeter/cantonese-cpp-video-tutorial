#include <bits/stdc++.h>
using namespace std;

int knapsack(const vector<int>& w, const vector<int>& v,
             int cap) {
    vector<int> dp(cap + 1, 0);
    for (size_t i = 0; i < w.size(); i++) {
        for (int c = cap; c >= w[i]; c--) {
            dp[c] = max(dp[c], dp[c - w[i]] + v[i]);
        }
    }
    return dp[cap];
}

int lis(const vector<int>& a) {
    vector<int> dp(a.size(), 1);
    for (size_t i = 0; i < a.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }
    return *max_element(dp.begin(), dp.end());
}

int lcs(const string& s, const string& t) {
    size_t n = s.size(), m = t.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (size_t i = 1; i <= n; i++) {
        for (size_t j = 1; j <= m; j++) {
            if (s[i - 1] == t[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    return dp[n][m];
}

int main() {
    vector<int> weight{1, 3, 4, 5}, value{1, 4, 5, 7};
    cout << "knapsack " << knapsack(weight, value, 7) << '\n';
    vector<int> a{10, 9, 2, 5, 3, 7, 101, 18};
    cout << "lis " << lis(a) << '\n';
    cout << "lcs " << lcs("ABCBDAB", "BDCABA") << '\n';
}

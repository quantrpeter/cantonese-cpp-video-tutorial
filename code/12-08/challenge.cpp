#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> items{3, 5, 7, 9};
    int target = 12, count = 0;
    for (int mask = 0; mask < (1 << 4); mask++) {
        int sum = 0;
        for (int i = 0; i < 4; i++) {
            if (mask & (1 << i)) {
                sum += items[i];
            }
        }
        if (sum == target) {
            count++;
        }
    }
    cout << count << ' ' << __builtin_popcount(13) << '\n';
}

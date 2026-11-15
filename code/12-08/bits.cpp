#include <bits/stdc++.h>
using namespace std;

int main() {
    int a = 12, b = 10;
    cout << bitset<4>(a) << ' ' << bitset<4>(b) << '\n';
    cout << (a & b) << ' ' << (a | b) << ' ' << (a ^ b) << '\n';
    cout << (1 << 5) << ' ' << (a >> 2) << '\n';
    if ((a & b) == 8) {
        cout << "and is 8\n";
    }
    vector<int> items{3, 5, 7};
    for (int mask = 0; mask < (1 << 3); mask++) {
        int sum = 0;
        for (int i = 0; i < 3; i++) {
            if (mask & (1 << i)) {
                sum += items[i];
            }
        }
        cout << bitset<3>(mask) << ':' << sum << ' ';
    }
    cout << '\n';
}

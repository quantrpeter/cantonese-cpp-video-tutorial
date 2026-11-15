#include <bits/stdc++.h>
using namespace std;

int main() {
    int amount = 63;
    vector<int> coins{50, 20, 10, 5, 2, 1};
    int used = 0;
    for (int c : coins) {
        used += amount / c;
        amount %= c;
    }
    cout << used << '\n';
}

#include <bits/stdc++.h>
using namespace std;

int main() {
    int g[4][4] = {};
    int val = 1;
    for (int r = 1; r <= 3; r++) {
        for (int c = 1; c <= 3; c++) {
            g[r][c] = val++;
        }
    }
    int p[4][4] = {};
    for (int r = 1; r <= 3; r++) {
        for (int c = 1; c <= 3; c++) {
            p[r][c] = g[r][c] + p[r - 1][c] + p[r][c - 1] - p[r - 1][c - 1];
        }
    }
    int r1 = 2, c1 = 2, r2 = 3, c2 = 3;
    cout << p[r2][c2] - p[r1 - 1][c2] - p[r2][c1 - 1] + p[r1 - 1][c1 - 1] << '\n';
}

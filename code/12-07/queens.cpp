#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> col;
int solutions = 0;

bool safe(int row, int c) {
    for (int r = 0; r < row; r++) {
        if (col[r] == c || abs(col[r] - c) == row - r) {
            return false;
        }
    }
    return true;
}

void place(int row) {
    if (row == n) {
        solutions++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (safe(row, c)) {
            col[row] = c;
            place(row + 1);
        }
    }
}

int main() {
    for (n = 4; n <= 8; n++) {
        col.assign(n, 0);
        solutions = 0;
        place(0);
        cout << n << ": " << solutions << '\n';
    }
}

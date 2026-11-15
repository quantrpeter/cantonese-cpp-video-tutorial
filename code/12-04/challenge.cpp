#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> a{1, 2, 3, 4, 5, 6};
    int target = 7;
    int i = 0, j = (int)a.size() - 1, pairs = 0;
    while (i < j) {
        int s = a[i] + a[j];
        if (s == target) {
            pairs++;
            i++;
            j--;
        } else if (s < target) {
            i++;
        } else {
            j--;
        }
    }
    cout << pairs << '\n';
}

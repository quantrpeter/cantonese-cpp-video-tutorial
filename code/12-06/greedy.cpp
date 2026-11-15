#include <bits/stdc++.h>
using namespace std;

struct Act {
    int start;
    int end;
};

int main() {
    int n;
    cin >> n;
    vector<Act> acts(n);
    for (auto& a : acts) {
        cin >> a.start >> a.end;
    }
    sort(acts.begin(), acts.end(), [](const Act& a, const Act& b) {
        return a.end < b.end;
    });
    int count = 0;
    int lastEnd = 0;
    for (const auto& a : acts) {
        if (a.start >= lastEnd) {
            count++;
            lastEnd = a.end;
            cout << a.start << '-' << a.end << ' ';
        }
    }
    cout << "\ncount " << count << '\n';
}

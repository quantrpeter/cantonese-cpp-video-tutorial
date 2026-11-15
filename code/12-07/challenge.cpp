#include <bits/stdc++.h>
using namespace std;

vector<int> items{1, 2, 3};
vector<int> chosen;

void subsets(int i) {
    if (i == (int)items.size()) {
        cout << '{';
        for (int x : chosen) {
            cout << x;
        }
        cout << "} ";
        return;
    }
    subsets(i + 1);
    chosen.push_back(items[i]);
    subsets(i + 1);
    chosen.pop_back();
}

int main() {
    subsets(0);
    cout << '\n';
}

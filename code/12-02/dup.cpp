#include <bits/stdc++.h>
using namespace std;

bool slowHasDup(const vector<int>& v) {
    for (size_t i = 0; i < v.size(); i++) {
        for (size_t j = i + 1; j < v.size(); j++) {
            if (v[i] == v[j]) {
                return true;
            }
        }
    }
    return false;
}

bool fastHasDup(vector<int> v) {
    sort(v.begin(), v.end());
    for (size_t i = 1; i < v.size(); i++) {
        if (v[i] == v[i - 1]) {
            return true;
        }
    }
    return false;
}

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int i = 0; i < n; i++) {
        v[i] = 1LL * i * 7919 % n;
    }
    using namespace chrono;
    auto t0 = steady_clock::now();
    bool a = slowHasDup(v);
    auto t1 = steady_clock::now();
    bool b = fastHasDup(v);
    auto t2 = steady_clock::now();
    auto ms = [](auto d) {
        return duration_cast<milliseconds>(d).count();
    };
    cout << "O(n^2)     " << a << ' ' << ms(t1 - t0) << "ms\n";
    cout << "O(n log n) " << b << ' ' << ms(t2 - t1) << "ms\n";
}

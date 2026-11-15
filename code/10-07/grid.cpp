#include <chrono>
#include <iostream>
#include <vector>

int main() {
    using namespace std::chrono;
    const int n = 4000;
    std::vector<int> grid(n * n, 1);
    auto t0 = steady_clock::now();
    long long byRow = 0;
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            byRow += grid[r * n + c];
        }
    }
    auto t1 = steady_clock::now();
    long long byCol = 0;
    for (int c = 0; c < n; c++) {
        for (int r = 0; r < n; r++) {
            byCol += grid[r * n + c];
        }
    }
    auto t2 = steady_clock::now();
    std::cout << "rows " << byRow << ' '
              << duration_cast<milliseconds>(t1 - t0) << '\n';
    std::cout << "cols " << byCol << ' '
              << duration_cast<milliseconds>(t2 - t1) << '\n';
}

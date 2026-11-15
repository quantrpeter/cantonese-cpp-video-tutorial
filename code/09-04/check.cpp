#include <cassert>
#include <iostream>
#include <vector>

double average(const std::vector<int>& v) {
    assert(!v.empty() && "need at least one mark");
    int sum = 0;
    for (int x : v) {
        sum += x;
    }
    return static_cast<double>(sum) / v.size();
}

int main() {
    static_assert(sizeof(int) == 4, "needs 4-byte int");
    std::cout << average({72, 64}) << '\n';
}

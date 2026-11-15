#include <iostream>
#include <map>

int main() {
    std::map<int, int> table;
    for (int i = 0; i < 2000000; i++) {
        table[i * 7] = i;
    }
    long long sum = 0;
    for (int i = 0; i < 2000000; i++) {
        sum += table[i * 7];
    }
    std::cout << sum << '\n';
}

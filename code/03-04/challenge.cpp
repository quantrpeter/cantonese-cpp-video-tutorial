#include <iostream>

int doubled(int x) {
    return x * 2;
}

int main() {
    int coins{21};
    coins = doubled(coins);
    std::cout << coins << '\n';
}

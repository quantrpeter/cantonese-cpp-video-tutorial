#include <iostream>

int addOne(int n) {
    n = n + 1;
    return n;
}

int main() {
    int score{10};
    score = addOne(score);
    std::cout << "Outside: " << score << '\n';
}

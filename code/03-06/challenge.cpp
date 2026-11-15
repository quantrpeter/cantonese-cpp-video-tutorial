#include <iostream>

void addBonus(int& score, int bonus) {
    score += bonus;
}

int main() {
    int score{70};
    addBonus(score, 15);
    std::cout << score << '\n';
}

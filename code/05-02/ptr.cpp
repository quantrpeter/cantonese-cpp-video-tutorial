#include <iostream>

void addOne(int* p) {
    *p = *p + 1;
}

int main() {
    int score{10};
    int* p = &score;
    std::cout << "score: " << score << '\n';
    std::cout << "p:     " << p << '\n';
    std::cout << "*p:    " << *p << '\n';
    *p = 99;
    std::cout << "score: " << score << '\n';
    addOne(&score);
    std::cout << "score: " << score << '\n';
}

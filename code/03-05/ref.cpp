#include <iostream>

int main() {
    int score{10};
    int& nick = score;
    nick = nick + 5;
    std::cout << "score: " << score << '\n';
    std::cout << "nick:  " << nick << '\n';
    score = 100;
    std::cout << "nick:  " << nick << '\n';
}

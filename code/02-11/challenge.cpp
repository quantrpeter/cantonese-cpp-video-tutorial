#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> pick(1, 100);
    const int answer = pick(gen);
    constexpr int maxTries = 7;

    int guess{0};
    int tries{0};
    while (guess != answer && tries < maxTries) {
        std::cout << "Guess (1-100): ";
        std::cin >> guess;
        tries++;
        if (guess > answer) {
            std::cout << "Too big\n";
        } else if (guess < answer) {
            std::cout << "Too small\n";
        }
    }
    if (guess == answer) {
        std::cout << "Correct! " << tries << " tries\n";
    } else {
        std::cout << "Game over! It was " << answer << '\n';
    }
}

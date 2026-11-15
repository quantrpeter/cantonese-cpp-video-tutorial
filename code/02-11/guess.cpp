#include <iostream>
#include <random>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> pick(1, 100);
    const int answer = pick(gen);

    int guess{0};
    int tries{0};
    while (guess != answer) {
        std::cout << "Guess (1-100): ";
        std::cin >> guess;
        tries++;
        if (guess > answer) {
            std::cout << "Too big\n";
        } else if (guess < answer) {
            std::cout << "Too small\n";
        }
    }
    std::cout << "Correct! " << tries << " tries\n";
}

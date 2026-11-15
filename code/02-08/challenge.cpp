#include <iostream>

int main() {
    constexpr int answer = 7;
    int guess{};
    do {
        std::cout << "Guess: ";
        std::cin >> guess;
    } while (guess != answer);
    std::cout << "Correct!\n";
}

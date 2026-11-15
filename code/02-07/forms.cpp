// The table of for-loop forms in the video: each line printed by a real run.
#include <iostream>

int main() {
    for (int i = 0; i < 5; i++) { std::cout << i << ' '; }
    std::cout << '\n';
    for (int i = 1; i <= 5; i++) { std::cout << i << ' '; }
    std::cout << '\n';
    for (int i = 5; i > 0; i--) { std::cout << i << ' '; }
    std::cout << '\n';
    for (int i = 0; i < 10; i += 2) { std::cout << i << ' '; }
    std::cout << '\n';
}

#include <iostream>

int main() {
    char letter{'A'};
    int code = static_cast<int>(letter);
    std::cout << code << '\n';
    std::cout << letter + 1 << '\n';
    char next = static_cast<char>(letter + 1);
    std::cout << next << '\n';
}

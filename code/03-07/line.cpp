#include <iostream>

void printLine(int length = 20, char ch = '-') {
    for (int i = 0; i < length; i++) {
        std::cout << ch;
    }
    std::cout << '\n';
}

int main() {
    printLine();
    printLine(10);
    printLine(10, '*');
}

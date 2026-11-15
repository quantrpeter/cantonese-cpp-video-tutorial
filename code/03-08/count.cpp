#include <iostream>

void visit() {
    static int count = 0;
    count++;
    std::cout << "Visit #" << count << '\n';
}

int main() {
    visit();
    visit();
    visit();
}

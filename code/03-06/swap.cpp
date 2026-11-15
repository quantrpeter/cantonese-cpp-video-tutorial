#include <iostream>
#include <string>

void swapInts(int& a, int& b) {
    int temp = a;
    a = b;
    b = temp;
}

void greet(const std::string& name) {
    std::cout << "Hello, " << name << "!\n";
}

int main() {
    int x{1};
    int y{2};
    swapInts(x, y);
    std::cout << x << ' ' << y << '\n';
    std::string who = "Chan Tai Man";
    greet(who);
}

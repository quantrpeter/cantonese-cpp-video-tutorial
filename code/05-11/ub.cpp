#include <iostream>
#include <limits>

void outOfBounds() {
    int a[3]{1, 2, 3};
    int i = 3;
    std::cout << a[i] << '\n';
}

void overflow() {
    int big = std::numeric_limits<int>::max();
    big = big + 1;
    std::cout << big << '\n';
}

void uninit() {
    int x;
    std::cout << x << '\n';
}

int main() {
    int choice{};
    std::cin >> choice;
    switch (choice) {
    case 1: outOfBounds(); break;
    case 2: overflow(); break;
    case 3: uninit(); break;
    }
}

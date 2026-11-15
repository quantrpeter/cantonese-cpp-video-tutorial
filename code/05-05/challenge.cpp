#include <iostream>

int main() {
    int marks[5]{72, 85, 64, 91, 58};
    for (int* q = marks + 5; q != marks;) {
        --q;                    // step back first: never point before the array
        std::cout << *q << ' ';
    }
    std::cout << '\n';
}

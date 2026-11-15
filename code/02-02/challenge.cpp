#include <iostream>

int main() {
    int age{};
    std::cout << "Age: ";
    std::cin >> age;
    if (age >= 13 && age <= 19) {
        std::cout << "Teen\n";
    } else {
        std::cout << "Not a teen\n";
    }
}

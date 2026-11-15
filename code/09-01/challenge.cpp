#include <iostream>
#include <stdexcept>

int checkAge(int age) {
    if (age < 0) {
        throw std::runtime_error("negative age");
    }
    return age;
}

int main() {
    for (int a : {20, -5}) {
        try {
            std::cout << checkAge(a) << '\n';
        } catch (const std::runtime_error& e) {
            std::cout << "caught: " << e.what() << '\n';
        }
    }
}

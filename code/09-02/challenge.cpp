#include <iostream>
#include <stdexcept>
#include <string>

class BadAge : public std::invalid_argument {
public:
    BadAge(int age) : std::invalid_argument("bad age " + std::to_string(age)) {}
};

int main() {
    try {
        throw BadAge(-5);
    } catch (const std::logic_error& e) {
        std::cout << e.what() << '\n';
    }
}

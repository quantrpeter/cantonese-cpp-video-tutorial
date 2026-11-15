#include <iostream>
#include <stdexcept>

void risky() noexcept {
    throw std::runtime_error("oops");
}

int main() {
    try {
        risky();
    } catch (const std::exception& e) {
        std::cout << "caught " << e.what() << '\n';
    }
}

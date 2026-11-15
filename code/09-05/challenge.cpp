#include <expected>
#include <iostream>
#include <string>

std::expected<int, std::string> safeDivide(int a, int b) {
    if (b == 0) {
        return std::unexpected("divide by zero");
    }
    return a / b;
}

int main() {
    for (int b : {4, 0}) {
        auto r = safeDivide(12, b);
        if (r) {
            std::cout << *r << '\n';
        } else {
            std::cout << "error: " << r.error() << '\n';
        }
    }
}

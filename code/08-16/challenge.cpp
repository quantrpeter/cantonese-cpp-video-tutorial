#include <iostream>
#include <optional>

std::optional<int> toDigit(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    }
    return std::nullopt;
}

int main() {
    std::cout << toDigit('7').value_or(-1) << ' ' << toDigit('x').value_or(-1) << '\n';
}

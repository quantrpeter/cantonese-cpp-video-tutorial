#include <expected>
#include <iostream>
#include <string>

std::expected<int, std::string>
parseInt(const std::string& s) {
    if (s.empty()) {
        return std::unexpected("empty");
    }
    int value = 0;
    for (char c : s) {
        if (c < '0' || c > '9') {
            return std::unexpected("not a digit");
        }
        value = value * 10 + (c - '0');
    }
    return value;
}

int main() {
    for (std::string s : {"42", "4x2", ""}) {
        auto r = parseInt(s);
        if (r) {
            std::cout << "ok " << *r << '\n';
        } else {
            std::cout << "error: " << r.error() << '\n';
        }
    }
    std::cout << parseInt("7x").value_or(-1) << '\n';
}

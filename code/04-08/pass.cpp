#include <cctype>
#include <iostream>
#include <string>

int countChars(const std::string& s) {
    int n{0};
    for (char c : s) {
        if ((static_cast<unsigned char>(c) & 0xC0) != 0x80) {
            n++;
        }
    }
    return n;
}

int main() {
    std::string pw;
    std::cout << "Password: ";
    std::cin >> pw;
    int digits{0};
    for (char c : pw) {
        if (std::isdigit(static_cast<unsigned char>(c))) {
            digits++;
        }
    }
    bool ok = countChars(pw) >= 8 && digits > 0;
    std::cout << (ok ? "Strong\n" : "Weak\n");
}

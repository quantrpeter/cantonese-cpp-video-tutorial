#include <iostream>
#include <string>

int main() {
    std::string hk = "香港";
    std::cout << hk << ' ' << hk.size() << '\n';
    for (char c : hk) {
        int b = static_cast<unsigned char>(c);
        std::cout << std::hex << b << ' ';
    }
    std::cout << '\n';
}

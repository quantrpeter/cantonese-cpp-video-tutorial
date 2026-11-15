#include <iostream>
#include <string_view>

std::string_view firstWord(std::string_view s) {
    return s.substr(0, s.find(' '));
}

int main() {
    std::cout << firstWord("hello world") << '\n';
}

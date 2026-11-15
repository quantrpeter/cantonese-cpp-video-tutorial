#include <iostream>
#include <map>
#include <string>

int main() {
    std::string text = "banana";
    std::map<char, int> freq;
    for (char c : text) {
        freq[c]++;
    }
    for (const auto& [c, n] : freq) {
        std::cout << c << ' ' << n << '\n';
    }
}

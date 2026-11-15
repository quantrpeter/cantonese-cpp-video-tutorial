#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, int> count;
    std::string word;
    while (std::cin >> word) {
        count[word]++;
    }
    for (const auto& [w, n] : count) {
        std::cout << w << ' ' << n << '\n';
    }
}

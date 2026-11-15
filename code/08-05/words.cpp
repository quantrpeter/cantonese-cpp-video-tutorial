#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> count;
    std::string word;
    while (std::cin >> word) {
        count[word]++;
    }
    for (const auto& [w, n] : count) {
        std::cout << w << ' ' << n << '\n';
    }
    std::cout << count.size() << ' ';
    std::cout << count.contains("dog") << ' ';
    std::cout << count.size() << '\n';
}

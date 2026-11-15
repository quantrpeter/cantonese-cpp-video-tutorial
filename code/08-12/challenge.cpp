#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> w{"pear", "fig", "apple", "kiwi"};
    std::sort(w.begin(), w.end(), [](const std::string& a, const std::string& b) {
        if (a.size() != b.size()) {
            return a.size() < b.size();
        }
        return a < b;
    });
    for (const auto& x : w) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

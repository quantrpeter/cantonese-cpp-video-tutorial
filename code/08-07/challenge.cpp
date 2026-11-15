#include <iostream>
#include <set>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> monday{"Amy", "Ben", "Cat"};
    std::vector<std::string> tuesday{"Ben", "Dan", "Amy"};
    std::set<std::string> seen(monday.begin(), monday.end());
    std::set<std::string> both;
    for (const auto& n : tuesday) {
        if (seen.contains(n)) {
            both.insert(n);
        }
    }
    for (const auto& n : both) {
        std::cout << n << ' ';
    }
    std::cout << '\n';
}

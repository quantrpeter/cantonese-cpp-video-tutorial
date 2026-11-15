#include <iostream>
#include <set>
#include <string>

int main() {
    std::set<std::string> visitors;
    std::string name;
    while (std::cin >> name) {
        auto [it, added] = visitors.insert(name);
        if (!added) {
            std::cout << "again: " << name << '\n';
        }
    }
    std::cout << visitors.size() << ':';
    for (const auto& v : visitors) {
        std::cout << ' ' << v;
    }
    std::cout << '\n';
}

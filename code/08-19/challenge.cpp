#include <print>
#include <string>
#include <utility>
#include <vector>

int main() {
    std::vector<std::pair<std::string, int>> rows{{"Amy", 72}, {"Ben", 9}, {"Cathy", 100}};
    for (const auto& [name, mark] : rows) {
        std::println("{:<6}{:>4}", name, mark);
    }
}

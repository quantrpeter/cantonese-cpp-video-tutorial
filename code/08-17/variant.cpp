#include <iostream>
#include <string>
#include <variant>
#include <vector>

using Value = std::variant<int, double, std::string>;

int main() {
    Value v = 42;
    std::cout << v.index() << ' ' << std::get<int>(v) << '\n';
    v = std::string{"Amy"};
    std::cout << v.index() << ' ';
    std::cout << std::holds_alternative<int>(v) << '\n';
    std::vector<Value> row{42, 3.5, std::string{"Ben"}};
    auto print = [](const auto& a) { std::cout << a << ' '; };
    for (const Value& x : row) {
        std::visit(print, x);
    }
    std::cout << '\n';
}

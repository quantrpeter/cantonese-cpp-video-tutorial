#include <iostream>
#include <string>
#include <variant>
#include <vector>

using Value = std::variant<int, double, std::string>;

int main() {
    std::vector<Value> row{1, std::string{"a"}, 2.5, std::string{"b"}};
    int texts = 0;
    for (const Value& x : row) {
        if (std::holds_alternative<std::string>(x)) {
            texts++;
        }
    }
    std::cout << texts << '\n';
}

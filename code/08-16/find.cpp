#include <iostream>
#include <optional>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int mark;
};

std::optional<int> findMark(const std::vector<Student>& list,
                            const std::string& name) {
    for (const auto& s : list) {
        if (s.name == name) {
            return s.mark;
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<Student> list{{"Amy", 72}, {"Ben", 91}};
    auto a = findMark(list, "Ben");
    if (a) {
        std::cout << *a << '\n';
    }
    auto b = findMark(list, "Zoe");
    std::cout << b.has_value() << ' ';
    std::cout << b.value_or(-1) << '\n';
}

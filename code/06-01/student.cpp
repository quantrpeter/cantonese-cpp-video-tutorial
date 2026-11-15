#include <iostream>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int mark;
};

int main() {
    Student a{"Amy", 85};
    Student b{"Ben", 72};
    std::cout << a.name << ": " << a.mark << '\n';
    b.mark = b.mark + 5;
    std::cout << b.name << ": " << b.mark << '\n';
    std::vector<Student> cls{a, b, {"Cat", 91}};
    for (const auto& s : cls) {
        std::cout << s.name << ' ' << s.mark << '\n';
    }
}

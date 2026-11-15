#include <iostream>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int mark;
};

int main() {
    std::vector<int> v;
    v.reserve(9);
    for (int i = 0; i < 9; i++) {
        v.push_back(i);
        std::cout << v.capacity() << ' ';
    }
    std::cout << '\n';
    std::vector<Student> s;
    s.emplace_back("Amy", 72);
    std::cout << s[0].name << ' ' << s[0].mark << '\n';
    std::vector<int> nums{1, 2, 3};
    nums.push_back(4);
    auto it = nums.begin();
    std::cout << *it << '\n';
}

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Student {
    std::string name;
    int mark;
};

int main() {
    std::vector<Student> s{
        {"Cat", 72}, {"Amy", 91}, {"Ben", 72}, {"Dan", 58}};
    std::sort(s.begin(), s.end(),
              [](const Student& a, const Student& b) {
                  if (a.mark != b.mark) {
                      return a.mark > b.mark;
                  }
                  return a.name < b.name;
              });
    for (const auto& x : s) {
        std::cout << x.name << ' ' << x.mark << '\n';
    }
}

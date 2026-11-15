#include <iostream>
#include <string>
#include <utility>
#include <vector>

int main() {
    std::vector<std::string> names;
    std::string name = "a very long name that does not fit in a small string";
    names.push_back(std::move(name));
    std::cout << names[0].size() << ' ' << name.size() << '\n';
}

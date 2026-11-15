#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> names{"Amy", "Ben", "Cat", "Dan", "Eve"};
    names.erase(names.begin() + 2);
    names.push_back("Fay");
    std::cout << names.at(0) << ' ' << names.at(names.size() - 1) << '\n';
}

#include <iostream>
#include <string>

int main() {
    std::string name;
    std::cout << "Full name: ";
    std::getline(std::cin, name);
    std::cout << name.size() << '\n';
    std::cout << name[0] << '\n';
    std::cout << name[name.size() - 1] << '\n';
}

#include <iostream>
#include <string>

int main() {
    int age{};
    std::cout << "Age: ";
    std::cin >> age;
    std::string name;
    std::cout << "Full name: ";
    std::getline(std::cin >> std::ws, name);
    std::string hi = "Hello, " + name + "!";
    std::cout << hi << '\n';
    std::cout << name.size() << '\n';
    std::cout << name[0] << '\n';
}

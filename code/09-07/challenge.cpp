#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::istringstream csv("3,4,5");
    std::string field;
    int sum = 0;
    while (std::getline(csv, field, ',')) {
        sum += std::stoi(field);
    }
    std::cout << sum << '\n';
}

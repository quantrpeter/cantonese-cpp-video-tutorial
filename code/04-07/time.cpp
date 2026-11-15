#include <iostream>
#include <string>

int main() {
    std::string text;
    std::cout << "Time (HH:MM): ";
    std::cin >> text;
    std::size_t colon = text.find(':');
    if (colon == std::string::npos) {
        std::cout << "No colon!\n";
        return 1;
    }
    int hh = std::stoi(text.substr(0, colon));
    int mm = std::stoi(text.substr(colon + 1));
    int total = hh * 60 + mm;
    std::string msg = std::to_string(total) + " minutes";
    std::cout << msg << '\n';
    text.replace(colon, 1, "h");
    std::cout << text << '\n';
}

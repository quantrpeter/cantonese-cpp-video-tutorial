#include <iostream>
#include <string>

int main() {
    std::string date;
    std::cout << "Date (YYYY-MM-DD): ";
    std::cin >> date;
    std::size_t a = date.find('-');
    std::size_t b = date.find('-', a + 1);
    int year = std::stoi(date.substr(0, a));
    int month = std::stoi(date.substr(a + 1, b - a - 1));
    int day = std::stoi(date.substr(b + 1));
    std::cout << year << ' ' << month << ' ' << day << '\n';
}

#include <iostream>

int main() {
    int year{};
    std::cout << "Year: ";
    std::cin >> year;
    bool by4 = year % 4 == 0;
    bool by100 = year % 100 == 0;
    bool by400 = year % 400 == 0;
    if ((by4 && !by100) || by400) {
        std::cout << "Leap year\n";
    } else {
        std::cout << "Not a leap year\n";
    }
}

#include <array>
#include <iostream>

int main() {
    std::array<int, 12> days{31, 28, 31, 30, 31, 30,
                             31, 31, 30, 31, 30, 31};
    std::cout << "Months: " << days.size() << '\n';
    int month{};
    std::cout << "Month (1-12): ";
    std::cin >> month;
    std::cout << "Days: " << days.at(month - 1) << '\n';
    int total{0};
    for (int d : days) {
        total += d;
    }
    std::cout << "Year: " << total << '\n';
}

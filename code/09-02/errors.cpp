#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

class NotEnoughMoney : public std::runtime_error {
public:
    NotEnoughMoney(int shortBy)
        : std::runtime_error("short by " + std::to_string(shortBy)) {}
};

void withdraw(int& balance, int amount) {
    if (amount > balance) {
        throw NotEnoughMoney(amount - balance);
    }
    balance -= amount;
}

int main() {
    std::vector<int> v{1, 2, 3};
    try {
        std::cout << v.at(5) << '\n';
    } catch (const std::out_of_range& e) {
        std::cout << "range: " << e.what() << '\n';
    }
    int balance = 100;
    try {
        withdraw(balance, 30);
        withdraw(balance, 200);
    } catch (const NotEnoughMoney& e) {
        std::cout << "money: " << e.what() << '\n';
    } catch (const std::exception& e) {
        std::cout << "other: " << e.what() << '\n';
    }
    std::cout << balance << '\n';
}

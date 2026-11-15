#include <iostream>

class BankAccount {
public:
    bool deposit(double amount) {
        if (amount <= 0) {
            return false;
        }
        balance_ += amount;
        return true;
    }
    bool withdraw(double amount) {
        if (amount <= 0 || amount > balance_) {
            return false;
        }
        balance_ -= amount;
        return true;
    }
    double balance() {
        return balance_;
    }

private:
    double balance_{0};
};

int main() {
    BankAccount acc;
    acc.deposit(100);
    acc.withdraw(30);
    if (!acc.withdraw(150)) {
        std::cout << "Not enough money\n";
    }
    std::cout << "Balance: " << acc.balance() << '\n';
}

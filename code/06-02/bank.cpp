#include <iostream>
#include <string>

class BankAccount {
public:
    std::string owner;
    double balance{0};

    void deposit(double amount) {
        balance += amount;
    }
    void withdraw(double amount) {
        balance -= amount;
    }
    void show() {
        std::cout << owner << ": $" << balance << '\n';
    }
};

int main() {
    BankAccount acc;
    acc.owner = "Amy";
    acc.deposit(100);
    acc.withdraw(30);
    acc.show();
    acc.withdraw(150);
    acc.show();
}

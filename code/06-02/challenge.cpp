#include <iostream>
#include <string>

class BankAccount {
public:
    std::string owner;
    double balance{0};

    void deposit(double amount) {
        balance += amount;
    }
    void addInterest(double rate) {
        balance += balance * rate;
    }
    void show() {
        std::cout << owner << ": $" << balance << '\n';
    }
};

int main() {
    BankAccount acc;
    acc.owner = "Amy";
    acc.deposit(1000);
    acc.addInterest(0.05);
    acc.show();
}

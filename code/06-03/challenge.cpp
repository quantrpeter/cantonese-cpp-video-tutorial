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
    bool transfer(BankAccount& other, double amount) {
        if (!withdraw(amount)) {
            return false;
        }
        other.deposit(amount);
        return true;
    }
    double balance() {
        return balance_;
    }

private:
    double balance_{0};
};

int main() {
    BankAccount a;
    BankAccount b;
    a.deposit(100);
    a.transfer(b, 40);
    std::cout << a.balance() << ' ' << b.balance() << '\n';
}

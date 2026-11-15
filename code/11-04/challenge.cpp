#include <iostream>
#include <mutex>
#include <thread>

struct Account {
    std::mutex m;
    int balance;
};

void transfer(Account& from, Account& to, int amount) {
    std::scoped_lock both(from.m, to.m);
    from.balance -= amount;
    to.balance += amount;
}

int main() {
    Account x{{}, 100}, y{{}, 100};
    {
        std::jthread t1([&] { for (int i = 0; i < 1000; i++) transfer(x, y, 1); });
        std::jthread t2([&] { for (int i = 0; i < 1000; i++) transfer(y, x, 1); });
    }
    std::cout << x.balance << ' ' << y.balance << '\n';
}

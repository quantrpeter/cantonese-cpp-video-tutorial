#include <iostream>

int nextTicket() {
    static int ticket = 0;
    ticket++;
    return ticket;
}

int main() {
    std::cout << nextTicket() << ' ' << nextTicket() << ' ' << nextTicket() << '\n';
}

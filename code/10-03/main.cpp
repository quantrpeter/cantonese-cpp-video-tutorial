#include <iostream>
#include "calc.h"

int main() {
    double a{};
    double b{};
    char op{};
    std::cout << "a op b (q to quit)\n";
    while (std::cin >> a >> op >> b) {
        if (!validOp(op)) {
            std::cout << "Unknown operator\n";
        } else if (op == '/' && b == 0) {
            std::cout << "Cannot divide by 0\n";
        } else {
            std::cout << "= " << calculate(a, op, b) << '\n';
        }
    }
}

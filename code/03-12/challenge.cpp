#include <iostream>
#include <cmath>

bool validOp(char op) {
    switch (op) {
    case '+': case '-': case '*': case '/': case '%': case '^':
        return true;
    default:
        return false;
    }
}

double calculate(double a, char op, double b) {
    switch (op) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    case '/': return a / b;
    case '%': return std::fmod(a, b);
    case '^': return std::pow(a, b);
    }
    return 0;
}

int main() {
    double a{};
    double b{};
    char op{};
    while (std::cin >> a >> op >> b) {
        if (!validOp(op)) {
            std::cout << "Unknown operator\n";
        } else {
            std::cout << "= " << calculate(a, op, b) << '\n';
        }
    }
}

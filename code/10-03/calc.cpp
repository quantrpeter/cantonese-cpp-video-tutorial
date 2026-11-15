#include "calc.h"

bool validOp(char op) {
    switch (op) {
    case '+': case '-': case '*': case '/':
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
    }
    return 0;
}

#include <iostream>
#include "calc.h"

int main() {
    if (calculate(6, '*', 7) == 42 && !validOp('?')) {
        std::cout << "ok\n";
    } else {
        std::cout << "FAIL\n";
    }
}

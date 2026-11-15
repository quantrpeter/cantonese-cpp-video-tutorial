// The truth table in the video, printed by a real run.
#include <iostream>

int main() {
    std::cout << std::boolalpha;
    for (bool a : {true, false}) {
        for (bool b : {true, false}) {
            std::cout << a << ' ' << b << ' ' << (a && b) << ' ' << (a || b) << '\n';
        }
    }
    std::cout << !true << ' ' << !false << '\n';
}

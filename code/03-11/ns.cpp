#include <iostream>

namespace english {
    void print() {
        std::cout << "Hello!\n";
    }
}

namespace cantonese {
    void print() {
        std::cout << "Nei hou!\n";
    }
}

int main() {
    english::print();
    cantonese::print();
}

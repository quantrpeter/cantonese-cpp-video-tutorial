#include <iostream>
#include <memory>
#include <utility>

struct Robot {
    int id;
    Robot(int i) {
        id = i;
        std::cout << "Robot " << id << " on\n";
    }
    ~Robot() {
        std::cout << "Robot " << id << " off\n";
    }
};

int main() {
    auto a = std::make_unique<Robot>(1);
    std::cout << "a has robot " << a->id << '\n';
    auto b = std::move(a);
    std::cout << "a empty: " << (a == nullptr) << '\n';
    std::cout << "b has robot " << b->id << '\n';
}

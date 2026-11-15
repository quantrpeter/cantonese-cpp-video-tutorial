#include <iostream>
#include <memory>
#include <vector>

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
    std::vector<std::unique_ptr<Robot>> robots;
    for (int i = 1; i <= 3; i++) {
        robots.push_back(std::make_unique<Robot>(i));
    }
    std::cout << robots.size() << " robots\n";
}

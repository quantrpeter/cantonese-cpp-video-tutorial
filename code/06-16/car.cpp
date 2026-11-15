#include <iostream>

class Engine {
public:
    void start() const {
        std::cout << "engine starts\n";
    }
};

class Car {
public:
    void drive() const {
        engine_.start();
        std::cout << "car drives\n";
    }

private:
    Engine engine_;
};

void repair(const Engine&) {
    std::cout << "repairing an engine\n";
}

int main() {
    Car car;
    car.drive();
}

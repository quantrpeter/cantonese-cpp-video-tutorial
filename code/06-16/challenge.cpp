#include <iostream>

class Engine {
public:
    void start() const {
        std::cout << "engine starts\n";
    }
};

class Radio {
public:
    void play() const {
        std::cout << "radio plays\n";
    }
};

class Car {
public:
    void drive() const {
        engine_.start();
        radio_.play();
        std::cout << "car drives\n";
    }

private:
    Engine engine_;
    Radio radio_;
};

int main() {
    Car car;
    car.drive();
}

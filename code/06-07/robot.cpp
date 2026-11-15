#include <iostream>

class Robot {
public:
    Robot() : id_{++created_} {
        ++alive_;
    }
    ~Robot() {
        --alive_;
    }
    int id() const {
        return id_;
    }
    static int alive() {
        return alive_;
    }

private:
    int id_;
    static inline int created_ = 0;
    static inline int alive_ = 0;
};

int main() {
    Robot a;
    Robot b;
    std::cout << "alive: " << Robot::alive() << '\n';
    {
        Robot c;
        std::cout << "c is #" << c.id() << '\n';
        std::cout << "alive: " << Robot::alive() << '\n';
    }
    std::cout << "alive: " << Robot::alive() << '\n';
}

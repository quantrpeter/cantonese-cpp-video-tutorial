#include <iostream>

class Robot {
public:
    Robot() : id_{++created_} {}
    static int created() {
        return created_;
    }

private:
    int id_;
    static inline int created_ = 0;
};

int main() {
    Robot a;
    {
        Robot b;
        Robot c;
    }
    std::cout << Robot::created() << '\n';
}

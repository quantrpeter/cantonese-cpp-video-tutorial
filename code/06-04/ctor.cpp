#include <iostream>
#include <string>

class Student {
public:
    Student() : name_{"Unknown"}, mark_{0} {}
    Student(std::string name, int mark)
        : name_{name}, mark_{mark} {
        if (mark_ < 0) {
            mark_ = 0;
        }
    }
    void show() {
        std::cout << name_ << ": " << mark_ << '\n';
    }

private:
    std::string name_;
    int mark_;
};

int main() {
    Student a;
    Student b{"Ben", 72};
    Student c{"Cat", -5};
    a.show();
    b.show();
    c.show();
}

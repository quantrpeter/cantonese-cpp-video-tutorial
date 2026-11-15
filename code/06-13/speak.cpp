#include <iostream>

class Animal {
public:
    virtual void speak() const {
        std::cout << "...\n";
    }
};

class Dog : public Animal {
public:
    void speak() const override {
        std::cout << "Woof!\n";
    }
};

class Cat : public Animal {
public:
    void speak() const override {
        std::cout << "Meow!\n";
    }
};

void talk(const Animal& a) {
    a.speak();
}

int main() {
    Dog d;
    Cat c;
    talk(d);
    talk(c);
    const Animal* p = &c;
    p->speak();
}

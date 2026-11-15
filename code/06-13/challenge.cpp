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

class Cow : public Animal {
public:
    void speak() const override {
        std::cout << "Moo!\n";
    }
};

void talk(const Animal& a) {
    a.speak();
}

int main() {
    Dog d;
    Cow c;
    const Animal* zoo[] = {&d, &c, &d};
    for (const Animal* a : zoo) {
        talk(*a);
    }
}

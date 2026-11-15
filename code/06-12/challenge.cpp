#include <iostream>
#include <string>

class Animal {
public:
    Animal(const std::string& name) : name_{name} {
        std::cout << "Animal " << name_ << '\n';
    }
    void eat() const {
        std::cout << name_ << " eats\n";
    }

protected:
    std::string name_;
};

class Cat : public Animal {
public:
    Cat(const std::string& name) : Animal{name} {
        std::cout << "Cat " << name_ << '\n';
    }
    void meow() const {
        std::cout << name_ << ": Meow!\n";
    }
};

int main() {
    Cat c{"Kitty"};
    c.eat();
    c.meow();
}

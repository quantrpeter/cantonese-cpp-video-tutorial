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

class Dog : public Animal {
public:
    Dog(const std::string& name) : Animal{name} {
        std::cout << "Dog " << name_ << '\n';
    }
    void bark() const {
        std::cout << name_ << ": Woof!\n";
    }
};

int main() {
    Dog d{"Lucky"};
    d.eat();
    d.bark();
}

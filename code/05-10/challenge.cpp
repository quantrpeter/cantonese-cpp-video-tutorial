#include <iostream>
#include <memory>
#include <string>

struct Person {
    std::string name;
    std::weak_ptr<Person> buddy;
    Person(std::string n) {
        name = n;
    }
};

int main() {
    auto amy = std::make_shared<Person>("Amy");
    auto ben = std::make_shared<Person>("Ben");
    amy->buddy = ben;
    ben->buddy = amy;
    if (auto b = amy->buddy.lock()) {
        std::cout << "Amy's buddy: " << b->name << '\n';
    }
}

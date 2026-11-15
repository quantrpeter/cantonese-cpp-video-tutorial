#include <iostream>
#include <memory>
#include <string>

struct Person {
    std::string name;
    std::weak_ptr<Person> buddy;
    Person(std::string n) {
        name = n;
        std::cout << name << " in\n";
    }
    ~Person() {
        std::cout << name << " out\n";
    }
};

int main() {
    auto amy = std::make_shared<Person>("Amy");
    {
        auto copy = amy;
        std::cout << "count: " << amy.use_count() << '\n';
    }
    std::cout << "count: " << amy.use_count() << '\n';
    auto ben = std::make_shared<Person>("Ben");
    amy->buddy = ben;
    ben->buddy = amy;
}

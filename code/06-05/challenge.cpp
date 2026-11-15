#include <iostream>
#include <string>
#include <vector>

class Tracer {
public:
    Tracer(std::string name) : name_{name} {
        std::cout << "+ " << name_ << '\n';
    }
    ~Tracer() {
        std::cout << "- " << name_ << '\n';
    }

private:
    std::string name_;
};

int main() {
    for (int i = 1; i <= 3; i++) {
        Tracer t{"loop " + std::to_string(i)};
    }
}

#include <iostream>
#include <memory>
#include <string>

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

void f() {
    Tracer t{"in f"};
}

int main() {
    std::cout << "main starts\n";
    Tracer a{"a"};
    {
        Tracer b{"b"};
        Tracer c{"c"};
    }
    f();
    auto h = std::make_unique<Tracer>("heap");
    std::cout << "main ends\n";
}

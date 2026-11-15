#include <iostream>

class Shape {
public:
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

class Square final : public Shape {
public:
    Square(double s) : s_{s} {}
    double area() const override {
        return s_ * s_;
    }

private:
    double s_;
};

int main() {
    Shape* s = new Square{3.0};
    std::cout << s->area() << '\n';
    delete s;
}

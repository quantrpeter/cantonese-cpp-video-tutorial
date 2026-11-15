#include <iostream>

class Shape {
public:
    virtual double area() const = 0;
};

class Circle : public Shape {
public:
    Circle(double r) : r_{r} {}
    double area() const override {
        return 3.14159 * r_ * r_;
    }

private:
    double r_;
};

class Square : public Shape {
public:
    Square(double s) : s_{s} {}
    double area() const override {
        return s_ * s_;
    }

private:
    double s_;
};

void report(const Shape& s) {
    std::cout << s.area() << '\n';
}

int main() {
    Circle c{1.0};
    Square q{2.0};
    report(c);
    report(q);
}

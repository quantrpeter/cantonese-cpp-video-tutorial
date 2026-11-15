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

class Triangle : public Shape {
public:
    Triangle(double b, double h) : b_{b}, h_{h} {}
    double area() const override {
        return 0.5 * b_ * h_;
    }

private:
    double b_;
    double h_;
};

void report(const Shape& s) {
    std::cout << s.area() << '\n';
}

int main() {
    Circle c{1.0};
    Square q{2.0};
    report(c);
    report(q);
    report(Triangle{3.0, 4.0});
}

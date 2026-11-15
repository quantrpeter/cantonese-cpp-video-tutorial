#include <iostream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

const double pi = 3.14159;

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;
    virtual std::string name() const = 0;
};

class Circle : public Shape {
public:
    Circle(double r) : r_{r} {}
    double area() const override { return pi * r_ * r_; }
    std::string name() const override { return "circle"; }

private:
    double r_;
};

class Rect : public Shape {
public:
    Rect(double w, double h) : w_{w}, h_{h} {}
    double area() const override { return w_ * h_; }
    std::string name() const override { return "rect"; }

private:
    double w_;
    double h_;
};

class Triangle : public Shape {
public:
    Triangle(double b, double h) : b_{b}, h_{h} {}
    double area() const override { return 0.5 * b_ * h_; }
    std::string name() const override { return "triangle"; }

private:
    double b_;
    double h_;
};

std::unique_ptr<Shape> readShape(char kind) {
    if (kind == 'c') {
        double r;
        std::cin >> r;
        return std::make_unique<Circle>(r);
    }
    if (kind == 'r') {
        double w, h;
        std::cin >> w >> h;
        return std::make_unique<Rect>(w, h);
    }
    if (kind == 't') {
        double b, h;
        std::cin >> b >> h;
        return std::make_unique<Triangle>(b, h);
    }
    return nullptr;
}

int main() {
    std::vector<std::unique_ptr<Shape>> shapes;
    char kind;
    while (std::cin >> kind && kind != 'q') {
        auto s = readShape(kind);
        if (s == nullptr) {
            std::cout << "unknown shape\n";
            continue;
        }
        shapes.push_back(std::move(s));
    }
    double total = 0;
    for (const auto& s : shapes) {
        std::cout << s->name() << ' ' << s->area() << '\n';
        total += s->area();
    }
    std::cout << "total " << total << '\n';
}

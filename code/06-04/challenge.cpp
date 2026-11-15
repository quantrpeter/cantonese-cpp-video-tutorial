#include <iostream>

class Rectangle {
public:
    Rectangle() : w_{1}, h_{1} {}
    Rectangle(int w, int h) : w_{w}, h_{h} {}
    int area() {
        return w_ * h_;
    }

private:
    int w_;
    int h_;
};

int main() {
    Rectangle a;
    Rectangle b{4, 6};
    std::cout << a.area() << ' ' << b.area() << '\n';
}

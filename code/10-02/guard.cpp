#include <iostream>
#include "point.h"
#include "shape.h"

int main() {
    Line l{{0, 0}, {3, 4}};
    std::cout << l.b.x << '\n';
}

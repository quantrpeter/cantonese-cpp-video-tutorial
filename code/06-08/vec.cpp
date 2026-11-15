#include <compare>
#include <iostream>

struct Vec2 {
    int x;
    int y;

    Vec2 operator+(const Vec2& other) const {
        return {x + other.x, y + other.y};
    }
    auto operator<=>(const Vec2&) const = default;
};

std::ostream& operator<<(std::ostream& out, const Vec2& v) {
    return out << '(' << v.x << ", " << v.y << ')';
}

int main() {
    Vec2 a{1, 2};
    Vec2 b{3, 4};
    Vec2 c = a + b;
    std::cout << c << '\n';
    std::cout << (a == b) << ' ' << (a < b) << '\n';
}

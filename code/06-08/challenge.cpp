#include <iostream>

struct Vec2 {
    int x;
    int y;

    Vec2 operator-(const Vec2& other) const {
        return {x - other.x, y - other.y};
    }
    Vec2 operator*(int k) const {
        return {x * k, y * k};
    }
};

std::ostream& operator<<(std::ostream& out, const Vec2& v) {
    return out << '(' << v.x << ", " << v.y << ')';
}

int main() {
    Vec2 a{5, 7};
    Vec2 b{1, 2};
    std::cout << (a - b) << ' ' << (b * 3) << '\n';
}

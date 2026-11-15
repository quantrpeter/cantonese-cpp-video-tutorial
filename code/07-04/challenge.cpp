#include <iostream>

template <typename T>
concept Comparable = requires(T a, T b) {
    a > b;
};

template <Comparable T>
T maxOf(T a, T b) {
    if (a > b) {
        return a;
    }
    return b;
}

struct Point {
    int x;
    int y;
    bool operator>(const Point& other) const {
        return x > other.x;
    }
};

int main() {
    Point p{1, 2}, q{3, 4};
    std::cout << maxOf(p, q).x << '\n';
}

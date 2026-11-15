#include <iostream>
#include <string>
#include <utility>
#include <vector>

template <typename T>
class Box {
public:
    Box(T value) : value_{value} {}
    T get() const {
        return value_;
    }

private:
    T value_;
};

int main() {
    Box s{std::string{"hi"}};
    std::pair p{'A', 7};
    std::cout << s.get() << ' ' << p.first << ' ' << p.second << '\n';
}

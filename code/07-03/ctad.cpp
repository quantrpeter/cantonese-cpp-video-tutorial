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
    std::vector v{1, 2, 3};
    std::pair p{1, 2.5};
    Box b{3.5};
    std::cout << v.size() << ' ' << p.second << '\n';
    std::cout << b.get() << '\n';
    std::vector<std::string> names{"Amy", "Ben"};
    std::cout << names[0] + names[1] << '\n';
}

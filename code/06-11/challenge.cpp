#include <iostream>
#include <utility>
#include <vector>

class Buffer {
public:
    Buffer(int n) : data_(n) {}
    int size() const {
        return static_cast<int>(data_.size());
    }

private:
    std::vector<int> data_;
};

int main() {
    Buffer a{1000000};
    Buffer b = a;
    Buffer c = std::move(a);
    std::cout << a.size() << ' ' << b.size() << ' ' << c.size() << '\n';
}

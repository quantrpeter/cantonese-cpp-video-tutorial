#include <iostream>
#include <utility>
#include <vector>

class Buffer {
public:
    Buffer(int n) : data_(n) {}
    void set(int i, int v) {
        data_[i] = v;
    }
    int get(int i) const {
        return data_[i];
    }

private:
    std::vector<int> data_;
};

int main() {
    Buffer a{3};
    a.set(0, 42);
    Buffer b = a;
    b.set(0, 99);
    Buffer c{1};
    c = a;
    std::cout << a.get(0) << ' ' << b.get(0) << ' ' << c.get(0) << '\n';
    Buffer d = std::move(a);
    std::cout << d.get(0) << '\n';
}

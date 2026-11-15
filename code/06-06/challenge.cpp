#include <iostream>

class Counter {
public:
    Counter& add(int n) {
        count_ += n;
        return *this;
    }
    Counter& reset() {
        count_ = 0;
        return *this;
    }
    int count() const {
        return count_;
    }

private:
    int count_{0};
};

int main() {
    Counter c;
    std::cout << c.add(5).reset().add(2).count() << '\n';
}

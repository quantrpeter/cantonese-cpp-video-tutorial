#include <iostream>
#include <string>

class Counter {
public:
    Counter(std::string name) : name_{name} {}
    Counter& add(int n) {
        count_ += n;
        return *this;
    }
    int count() const {
        return count_;
    }
    void show() const {
        std::cout << name_ << ": " << count_ << '\n';
    }

private:
    std::string name_;
    int count_{0};
};

void report(const Counter& c) {
    c.show();
}

int main() {
    Counter steps{"Steps"};
    steps.add(3).add(4);
    report(steps);
}

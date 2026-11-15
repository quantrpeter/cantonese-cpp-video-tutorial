#include <iostream>
#include <string>
#include <vector>

template <typename T>
class Stack {
public:
    void push(const T& value) {
        items_.push_back(value);
    }
    T pop() {
        T top = items_.back();
        items_.pop_back();
        return top;
    }
    const T& top() const {
        return items_.back();
    }
    bool empty() const {
        return items_.empty();
    }
    int size() const {
        return static_cast<int>(items_.size());
    }

private:
    std::vector<T> items_;
};

int main() {
    Stack<char> s;
    s.push('a');
    s.push('b');
    std::cout << s.top() << ' ' << s.size() << '\n';
    s.pop();
    std::cout << s.top() << ' ' << s.size() << '\n';
}

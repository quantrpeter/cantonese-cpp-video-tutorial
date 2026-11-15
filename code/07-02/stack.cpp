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
    Stack<int> nums;
    nums.push(1);
    nums.push(2);
    nums.push(3);
    while (!nums.empty()) {
        std::cout << nums.pop() << ' ';
    }
    std::cout << '\n';
    Stack<std::string> words;
    words.push("hello");
    words.push("world");
    std::cout << words.pop() << ' ' << words.size() << '\n';
}

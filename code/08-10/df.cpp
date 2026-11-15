#include <deque>
#include <iostream>

int main() {
    std::deque<int> d;
    for (int i = 0; i < 200000; i++) {
        d.push_front(i);
    }
    std::cout << d.front() << '\n';
}

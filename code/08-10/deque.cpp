#include <deque>
#include <iostream>

int main() {
    std::deque<int> d{2, 3};
    d.push_front(1);
    d.push_back(4);
    for (int x : d) {
        std::cout << x << ' ';
    }
    std::cout << "| " << d[0] << '\n';
}

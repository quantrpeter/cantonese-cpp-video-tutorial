#include <deque>
#include <iostream>

int main() {
    std::deque<int> window;
    for (int x : {5, 1, 4, 2, 8, 3}) {
        window.push_back(x);
        if (window.size() > 3) {
            window.pop_front();
        }
    }
    for (int x : window) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

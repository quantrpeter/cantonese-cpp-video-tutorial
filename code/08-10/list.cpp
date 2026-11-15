#include <iostream>
#include <iterator>
#include <list>

int main() {
    std::list<int> l{1, 2, 4};
    auto it = std::next(l.begin(), 2);
    l.insert(it, 3);
    l.push_front(0);
    std::cout << *it << " |";
    for (int x : l) {
        std::cout << ' ' << x;
    }
    std::cout << '\n';
}

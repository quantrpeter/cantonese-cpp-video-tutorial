#include <functional>
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::priority_queue<int, std::vector<int>,
                        std::greater<int>> pq;
    for (int x : {8, 3, 9, 1, 5}) {
        pq.push(x);
    }
    for (int i = 0; i < 3; i++) {
        std::cout << pq.top() << ' ';
        pq.pop();
    }
    std::cout << '\n';
}

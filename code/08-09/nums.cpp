#include <functional>
#include <iostream>
#include <queue>
#include <vector>

int main() {
    std::priority_queue<int, std::vector<int>,
                        std::greater<int>> pq;
    for (int x : {3, 9, 1, 7}) {
        pq.push(x);
    }
    while (!pq.empty()) {
        std::cout << pq.top() << ' ';
        pq.pop();
    }
    std::cout << '\n';
}

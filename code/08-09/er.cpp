#include <iostream>
#include <queue>
#include <string>
#include <utility>

int main() {
    std::priority_queue<std::pair<int, std::string>> er;
    er.push({2, "Amy (cut)"});
    er.push({5, "Ben (heart)"});
    er.push({3, "Cat (arm)"});
    er.push({5, "Dan (breathing)"});
    while (!er.empty()) {
        auto [level, name] = er.top();
        std::cout << level << ' ' << name << '\n';
        er.pop();
    }
}

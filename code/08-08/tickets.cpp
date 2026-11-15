#include <iostream>
#include <queue>
#include <string>

int main() {
    std::queue<std::string> line;
    line.push("Amy");
    line.push("Ben");
    line.push("Cat");
    while (!line.empty()) {
        std::cout << "serving " << line.front() << '\n';
        line.pop();
    }
}

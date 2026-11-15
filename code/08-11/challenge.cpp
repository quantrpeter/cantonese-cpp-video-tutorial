#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> words{"hi", "hello", "cpp", "lambda"};
    std::size_t k = 3;
    auto n = std::count_if(words.begin(), words.end(),
                           [k](const std::string& w) { return w.size() > k; });
    std::cout << n << '\n';
}

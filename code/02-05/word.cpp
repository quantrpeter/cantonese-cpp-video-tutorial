#include <iostream>
#include <string>

int main() {
    int n{};
    std::cout << "How many apples? ";
    std::cin >> n;
    std::string word = n == 1 ? "apple" : "apples";
    std::cout << n << ' ' << word << '\n';
}

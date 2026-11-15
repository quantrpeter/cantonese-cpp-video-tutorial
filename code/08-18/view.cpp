#include <iostream>
#include <span>
#include <string>
#include <string_view>
#include <vector>

int countA(std::string_view s) {
    int n = 0;
    for (char c : s) {
        if (c == 'a') {
            n++;
        }
    }
    return n;
}

int total(std::span<const int> v) {
    int t = 0;
    for (int x : v) {
        t += x;
    }
    return t;
}

int main() {
    std::string word = "banana";
    std::cout << countA(word) << ' ';
    std::cout << countA("papaya") << '\n';
    std::vector<int> v{1, 2, 3};
    int arr[] = {4, 5, 6};
    std::cout << total(v) << ' ' << total(arr) << '\n';
}

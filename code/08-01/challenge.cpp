#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> marks{72, 64, 91};
    std::string word = "banana";
    std::reverse(marks.begin(), marks.end());
    std::reverse(word.begin(), word.end());
    for (int m : marks) {
        std::cout << m << ' ';
    }
    std::cout << word << '\n';
}

#include <iostream>
#include <string>
#include <unordered_map>

int main() {
    std::unordered_map<char, int> freq;
    for (char c : std::string{"abracadabra"}) {
        freq[c]++;
    }
    std::cout << freq['a'] << ' ' << freq.size() << '\n';
}

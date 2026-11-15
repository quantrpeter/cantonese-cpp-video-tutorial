#include <algorithm>
#include <cctype>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

using Entry = std::pair<std::string, int>;

std::string clean(const std::string& raw) {
    std::string w;
    for (char c : raw) {
        if (std::isalpha(c)) {
            w += static_cast<char>(std::tolower(c));
        }
    }
    return w;
}

int main() {
    std::map<std::string, int> count;
    std::string raw;
    while (std::cin >> raw) {
        std::string w = clean(raw);
        if (w.size() >= 3) {
            count[w]++;
        }
    }
    std::vector<Entry> list(count.begin(), count.end());
    std::sort(list.begin(), list.end(),
              [](const Entry& a, const Entry& b) {
                  if (a.second != b.second) {
                      return a.second > b.second;
                  }
                  return a.first < b.first;
              });
    for (std::size_t i = 0; i < list.size() && i < 3; i++) {
        const auto& [word, n] = list[i];
        std::cout << n << ' ' << word << '\n';
    }
}

#include <iostream>
#include <stack>
#include <string>

bool balanced(const std::string& s) {
    const std::string opens = "([{";
    const std::string closes = ")]}";
    std::stack<char> st;
    for (char c : s) {
        auto o = opens.find(c);
        auto k = closes.find(c);
        if (o != std::string::npos) {
            st.push(c);
        } else if (k != std::string::npos) {
            if (st.empty() || st.top() != opens[k]) {
                return false;
            }
            st.pop();
        }
    }
    return st.empty();
}

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::cout << (balanced(line) ? "ok" : "bad") << '\n';
    }
}

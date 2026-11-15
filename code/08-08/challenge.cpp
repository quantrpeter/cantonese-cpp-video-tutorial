#include <iostream>
#include <stack>
#include <string>

int main() {
    std::string word = "hello";
    std::stack<char> st;
    for (char c : word) {
        st.push(c);
    }
    while (!st.empty()) {
        std::cout << st.top();
        st.pop();
    }
    std::cout << '\n';
}

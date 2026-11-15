#include <iostream>
#include <string>
#include <string_view>

int main() {
    std::string_view sv =
        std::string{"a temporary string, long enough"};
    std::cout << sv << '\n';
}

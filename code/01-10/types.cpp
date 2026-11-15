// Checks the types the video says auto deduces: it only compiles if they are right.
#include <type_traits>

int main() {
    auto a = 80;
    auto x = 80.0;
    auto c = 'A';
    auto ok = true;
    auto avg = static_cast<double>(a + 95) / 2;
    static_assert(std::is_same_v<decltype(a), int>);
    static_assert(std::is_same_v<decltype(x), double>);
    static_assert(std::is_same_v<decltype(c), char>);
    static_assert(std::is_same_v<decltype(ok), bool>);
    static_assert(std::is_same_v<decltype(avg), double>);
}

#include <iostream>

int main() {
    long long f{479001600};
    std::cout << "12! = " << f << '\n';
    f = f * 13;
    std::cout << "13! = " << f << '\n';
}

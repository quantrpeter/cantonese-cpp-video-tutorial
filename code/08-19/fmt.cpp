#include <format>
#include <iostream>
#include <print>
#include <string>

int main() {
    std::string name = "Amy";
    int mark = 72;
    double avg = 68.456;
    std::cout << name << " got " << mark;
    std::cout << ", avg " << avg << '\n';
    std::string line = std::format("{} got {}, avg {:.1f}",
                                   name, mark, avg);
    std::cout << line << '\n';
    std::print("{:<6}|{:>5}|\n", name, mark);
    std::println("{:08.3f}", avg);
    std::println("{:x} {:b}", 255, 5);
}

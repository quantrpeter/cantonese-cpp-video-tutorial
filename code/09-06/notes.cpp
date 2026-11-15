#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ofstream out("notes.txt");
    out << "buy milk\n";
    out << "call Amy\n";
    out.close();
    std::ifstream in("notes.txt");
    if (!in) {
        std::cout << "cannot open\n";
        return 1;
    }
    std::string line;
    int n = 0;
    while (std::getline(in, line)) {
        n++;
        std::cout << n << ": " << line << '\n';
    }
}

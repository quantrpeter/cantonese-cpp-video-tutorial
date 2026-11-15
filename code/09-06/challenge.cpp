#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("todo.txt");
        out << "buy milk\ncall Amy\n";
    }
    {
        std::ofstream more("todo.txt", std::ios::app);
        more << "pay rent\n";
    }
    std::ifstream in("todo.txt");
    std::string line;
    int n = 0;
    while (std::getline(in, line)) {
        n++;
    }
    std::cout << n << '\n';
}

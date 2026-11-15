#include <iostream>
#include <vector>

int main() {
    const int rows = 3;
    const int cols = 4;
    std::vector<char> row(cols, '.');
    std::vector<std::vector<char>> seats(rows, row);
    int r{};
    int c{};
    std::cout << "Row and seat: ";
    std::cin >> r >> c;
    seats[r][c] = 'X';
    for (const auto& line : seats) {
        for (char s : line) {
            std::cout << s << ' ';
        }
        std::cout << '\n';
    }
}

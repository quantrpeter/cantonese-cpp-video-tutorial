#include <iostream>
#include <string>
#include <vector>

struct Book {
    std::string title;
    std::string author;
    int pages;
};

int main() {
    std::vector<Book> books{{"Dune", "Herbert", 412}, {"Emma", "Austen", 474}, {"Holes", "Sachar", 233}};
    Book longest = books[0];
    for (const auto& b : books) {
        if (b.pages > longest.pages) {
            longest = b;
        }
    }
    std::cout << longest.title << " (" << longest.pages << ")\n";
}

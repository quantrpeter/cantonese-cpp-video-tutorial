#include <iostream>
#include "library.h"

int main() {
    Library lib;
    int stories = lib.addBook("Harbour Stories", "Chan");
    lib.addBook("Night Market", "Wong");
    lib.addBook("Harbour Food", "Chan");
    int amy = lib.addMember("Amy");
    for (int id : lib.search("Harbour")) {
        std::cout << id << ' ' << lib.book(id).title << '\n';
    }
    lib.borrow(stories, amy);
    for (int id : {stories, 99}) {
        try {
            lib.borrow(id, amy);
        } catch (const std::exception& e) {
            std::cout << "error: " << e.what() << '\n';
        }
    }
    lib.save("books.csv");
}

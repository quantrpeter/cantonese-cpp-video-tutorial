#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "library.h"

TEST_CASE("borrow and give back") {
    Library lib;
    int b = lib.addBook("A", "X");
    int m = lib.addMember("Amy");
    lib.borrow(b, m);
    CHECK(lib.book(b).borrowedBy == m);
    CHECK_THROWS(lib.borrow(b, m));
    lib.giveBack(b);
    CHECK_FALSE(lib.book(b).borrowedBy.has_value());
    CHECK_THROWS(lib.giveBack(b));
}

TEST_CASE("search") {
    Library lib;
    lib.addBook("Harbour Stories", "Chan");
    lib.addBook("Night Market", "Wong");
    CHECK(lib.search("Harbour").size() == 1);
    CHECK(lib.search("zzz").empty());
}

TEST_CASE("unknown member") {
    Library lib;
    int b = lib.addBook("A", "X");
    CHECK_THROWS_AS(lib.borrow(b, 42), std::invalid_argument);
}

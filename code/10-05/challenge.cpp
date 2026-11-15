#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "leap.h"

TEST_CASE("ordinary years") {
    CHECK(isLeapYear(2024));
    CHECK_FALSE(isLeapYear(2023));
}

TEST_CASE("centuries") {
    CHECK_FALSE(isLeapYear(1900));
    CHECK(isLeapYear(2000));
}

TEST_CASE("more centuries") {
    CHECK_FALSE(isLeapYear(2100));
    CHECK(isLeapYear(2400));
}

#include <iostream>
#include <vector>

struct Item {
    Item() = default;
    Item(const Item&) {
        std::cout << "copy ";
    }
    Item(Item&&) noexcept {
        std::cout << "move ";
    }
};

int main() {
    std::vector<Item> v;
    for (int i = 0; i < 3; i++) {
        v.emplace_back();
    }
    std::cout << '\n';
}

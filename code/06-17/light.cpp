#include <iostream>

enum class Fruit { Apple, Orange };
enum class Light { Red, Orange, Green };

Light next(Light l) {
    switch (l) {
    case Light::Red:
        return Light::Green;
    case Light::Green:
        return Light::Orange;
    case Light::Orange:
        return Light::Red;
    }
    return l;
}

int main() {
    const char* names[] = {"red", "orange", "green"};
    Light l = Light::Red;
    for (int i = 0; i < 4; i++) {
        std::cout << names[static_cast<int>(l)] << ' ';
        l = next(l);
    }
    std::cout << '\n';
}

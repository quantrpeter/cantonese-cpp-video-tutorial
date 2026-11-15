#include <array>
#include <iostream>

int main() {
    std::array<double, 7> temps{24.5, 26.0, 27.5, 25.0, 23.5, 28.0, 29.5};
    double total{0};
    double best = temps.at(0);
    for (double t : temps) {
        total += t;
        if (t > best) {
            best = t;
        }
    }
    std::cout << "Average: " << total / temps.size() << '\n';
    std::cout << "Highest: " << best << '\n';
}

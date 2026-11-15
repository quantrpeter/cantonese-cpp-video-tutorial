#include <iostream>

enum class Day { Mon, Tue, Wed, Thu, Fri, Sat, Sun };

bool isWeekend(Day d) {
    switch (d) {
    case Day::Sat:
    case Day::Sun:
        return true;
    case Day::Mon:
    case Day::Tue:
    case Day::Wed:
    case Day::Thu:
    case Day::Fri:
        return false;
    }
    return false;
}

int main() {
    std::cout << isWeekend(Day::Sat) << ' ' << isWeekend(Day::Mon) << '\n';
}

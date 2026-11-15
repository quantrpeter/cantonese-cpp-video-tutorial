#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::istringstream words("72 64 abc 91");
    int x;
    int sum = 0;
    while (words >> x) {
        sum += x;
    }
    std::cout << sum << '\n';
    std::istringstream csv("Amy,72,A");
    std::string field;
    std::vector<std::string> fields;
    while (std::getline(csv, field, ',')) {
        fields.push_back(field);
    }
    for (const auto& f : fields) {
        std::cout << '[' << f << ']';
    }
    std::cout << '\n';
    std::ostringstream out;
    out << fields[0] << " got " << std::stoi(fields[1]) + 5;
    std::cout << out.str() << '\n';
}

#include <fstream>
#include <iostream>
#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    std::ifstream in("scores.json");
    json data = json::parse(in);
    std::string cls = data["class"];
    std::cout << "class " << cls << '\n';
    int total = 0;
    for (const auto& s : data["students"]) {
        std::string name = s["name"];
        int mark = s["mark"];
        std::cout << name << ' ' << mark << '\n';
        total += mark;
    }
    std::cout << "total " << total << '\n';
}

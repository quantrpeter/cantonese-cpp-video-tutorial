#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main() {
    json out;
    out["name"] = "Cat";
    out["mark"] = 85;
    out["tags"] = {"new", "2A"};
    std::cout << out.dump(2) << '\n';
}

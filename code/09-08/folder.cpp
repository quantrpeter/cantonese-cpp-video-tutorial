#include <cstdint>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

int main() {
    fs::path dir = "photos";
    fs::path p = dir / "2025" / "beach.jpg";
    std::cout << p.string() << '\n';
    std::cout << p.filename().string() << ' ';
    std::cout << p.extension().string() << '\n';
    std::cout << fs::exists(p) << ' ';
    std::cout << fs::exists("nope.txt") << '\n';
    std::uintmax_t total = 0;
    for (auto& e : fs::recursive_directory_iterator(dir)) {
        if (e.is_regular_file()) {
            std::cout << e.path().string() << ' ';
            std::cout << e.file_size() << '\n';
            total += e.file_size();
        }
    }
    std::cout << "total " << total << " bytes\n";
}

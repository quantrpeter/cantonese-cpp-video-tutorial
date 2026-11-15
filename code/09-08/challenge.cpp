#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

int main() {
    int jpgs = 0;
    for (const auto& e : fs::recursive_directory_iterator("photos")) {
        if (e.is_regular_file() && e.path().extension() == ".jpg") {
            jpgs++;
        }
    }
    std::cout << jpgs << '\n';
}

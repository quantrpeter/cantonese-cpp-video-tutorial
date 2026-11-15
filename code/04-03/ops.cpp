#include <iostream>
#include <vector>

void show(const std::vector<int>& v) {
    for (const auto& x : v) {
        std::cout << x << ' ';
    }
    std::cout << "(size " << v.size() << ")\n";
}

int main() {
    std::vector<int> nums{10, 20, 30};
    show(nums);
    nums.insert(nums.begin(), 5);
    show(nums);
    nums.erase(nums.begin() + 1);
    show(nums);
    std::cout << nums.front() << ' ' << nums.back() << '\n';
    nums.clear();
    show(nums);
}

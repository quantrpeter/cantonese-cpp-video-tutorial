#include <iostream>
#include <vector>

int main() {
    std::vector<int> nums{10, 20, 30};
    std::cout << nums[5] << '\n';
    std::cout << nums.at(5) << '\n';
}

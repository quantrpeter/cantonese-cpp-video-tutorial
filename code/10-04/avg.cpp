#include <iostream>
#include <vector>

double average(const std::vector<int>& v) {
    int sum = 0;
    for (std::size_t i = 0; i < v.size(); i++) {
        sum += v[i];
    }
    return static_cast<double>(sum) / v.size();
}

int main() {
    std::vector<int> marks{70, 80, 90};
    std::cout << average(marks) << '\n';
}

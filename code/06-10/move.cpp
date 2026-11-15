#include <iostream>
#include <utility>

class Buffer {
public:
    Buffer(int n) : size_{n}, data_{new int[n]{}} {}
    Buffer(const Buffer& other)
        : size_{other.size_}, data_{new int[other.size_]} {
        std::cout << "copy " << size_ << " ints\n";
        for (int i = 0; i < size_; i++) {
            data_[i] = other.data_[i];
        }
    }
    Buffer(Buffer&& other) noexcept
        : size_{other.size_}, data_{other.data_} {
        other.size_ = 0;
        other.data_ = nullptr;
        std::cout << "move\n";
    }
    ~Buffer() {
        delete[] data_;
    }
    int size() const {
        return size_;
    }

private:
    int size_;
    int* data_;
};

int main() {
    Buffer a{1000000};
    Buffer b = a;
    Buffer c = std::move(a);
    std::cout << a.size() << ' ' << c.size() << '\n';
}

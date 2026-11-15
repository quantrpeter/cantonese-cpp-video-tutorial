#include <iostream>

class Buffer {
public:
    Buffer(int n) : size_{n}, data_{new int[n]{}} {}
    Buffer(const Buffer& other)
        : size_{other.size_}, data_{new int[other.size_]} {
        copyFrom(other);
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new int[size_];
            copyFrom(other);
        }
        return *this;
    }
    ~Buffer() {
        delete[] data_;
    }
    void set(int i, int v) {
        data_[i] = v;
    }
    int get(int i) const {
        return data_[i];
    }
    void fill(int v) {
        for (int i = 0; i < size_; i++) {
            data_[i] = v;
        }
    }

private:
    void copyFrom(const Buffer& other) {
        for (int i = 0; i < size_; i++) {
            data_[i] = other.data_[i];
        }
    }
    int size_;
    int* data_;
};

int main() {
    Buffer a{4};
    a.fill(7);
    Buffer b = a;
    b.fill(1);
    std::cout << a.get(3) << ' ' << b.get(3) << '\n';
}

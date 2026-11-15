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
    Buffer a{3};
    a.set(0, 42);
    Buffer b = a;
    b.set(0, 99);
    Buffer c{1};
    c = a;
    std::cout << a.get(0) << ' ' << b.get(0) << ' ' << c.get(0) << '\n';
}

#include <iostream>
#include <string>
#include <utility>

template <typename T>
class MiniVector {
public:
    MiniVector() = default;
    MiniVector(const MiniVector& other) {
        for (int i = 0; i < other.size_; i++) {
            push_back(other.data_[i]);
        }
    }
    MiniVector(MiniVector&& other) noexcept
        : data_{other.data_}, size_{other.size_},
          cap_{other.cap_} {
        other.data_ = nullptr;
        other.size_ = 0;
        other.cap_ = 0;
    }
    MiniVector& operator=(MiniVector other) noexcept {
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
        std::swap(cap_, other.cap_);
        return *this;
    }
    ~MiniVector() {
        delete[] data_;
    }
    void push_back(const T& value) {
        if (size_ == cap_) {
            grow();
        }
        data_[size_] = value;
        size_++;
    }
    T& operator[](int i) {
        return data_[i];
    }
    int size() const {
        return size_;
    }
    void pop_back() {
        size_--;
    }
    T& back() {
        return data_[size_ - 1];
    }
    int capacity() const {
        return cap_;
    }

private:
    void grow() {
        int bigger = cap_ == 0 ? 1 : cap_ * 2;
        T* fresh = new T[bigger];
        for (int i = 0; i < size_; i++) {
            fresh[i] = std::move(data_[i]);
        }
        delete[] data_;
        data_ = fresh;
        cap_ = bigger;
    }
    T* data_ = nullptr;
    int size_ = 0;
    int cap_ = 0;
};

int main() {
    MiniVector<int> v;
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);
    v.pop_back();
    std::cout << v.back() << ' ' << v.size() << '\n';
}

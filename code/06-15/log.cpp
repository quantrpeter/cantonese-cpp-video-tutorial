#include <iostream>
#include <memory>
#include <vector>

class Log {
public:
    virtual void write() const {
        std::cout << "log\n";
    }
    virtual ~Log() {
        std::cout << "~Log\n";
    }
};

class FileLog final : public Log {
public:
    FileLog() : buffer_(1000) {}
    void write() const override {
        std::cout << "file\n";
    }
    ~FileLog() override {
        std::cout << "~FileLog\n";
    }

private:
    std::vector<int> buffer_;
};

int main() {
    std::unique_ptr<Log> p = std::make_unique<FileLog>();
    p->write();
}

#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct Expense {
    double amount;
    std::string what;
};

class Book {
public:
    Book(const std::string& file) : file_{file} {
        load();
    }
    void add(double amount, const std::string& what) {
        if (amount <= 0) {
            throw std::invalid_argument("amount <= 0");
        }
        items_.push_back({amount, what});
    }
    void list() const {
        for (const auto& e : items_) {
            std::cout << e.what << ' ' << e.amount << '\n';
        }
    }
    std::size_t count() const {
        return items_.size();
    }
    double total() const {
        double sum = 0;
        for (const auto& e : items_) {
            sum += e.amount;
        }
        return sum;
    }
    void save() const {
        std::ofstream out(file_);
        for (const auto& e : items_) {
            out << e.amount << ',' << e.what << '\n';
        }
    }

private:
    void load() {
        std::ifstream in(file_);
        std::string line;
        while (std::getline(in, line)) {
            std::istringstream row(line);
            std::string amount, what;
            std::getline(row, amount, ',');
            std::getline(row, what);
            items_.push_back({std::stod(amount), what});
        }
    }
    std::string file_;
    std::vector<Expense> items_;
};

int main() {
    Book book("expenses.csv");
    std::string cmd;
    while (std::cin >> cmd) {
        if (cmd == "add") {
            std::string amount, what;
            std::cin >> amount >> what;
            try {
                book.add(std::stod(amount), what);
            } catch (const std::exception& e) {
                std::cout << "error: " << e.what() << '\n';
            }
        } else if (cmd == "list") {
            book.list();
        } else if (cmd == "count") {
            std::cout << book.count() << '\n';
        } else if (cmd == "total") {
            std::cout << book.total() << '\n';
        } else if (cmd == "quit") {
            book.save();
            break;
        }
    }
}

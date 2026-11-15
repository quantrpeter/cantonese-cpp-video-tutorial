#pragma once
#include <fstream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

struct Book {
    int id;
    std::string title;
    std::string author;
    std::optional<int> borrowedBy;
};

struct Member {
    int id;
    std::string name;
};

class Library {
public:
    int addBook(const std::string& title,
                const std::string& author) {
        books_.push_back({nextBook_, title, author, {}});
        return nextBook_++;
    }
    int addMember(const std::string& name) {
        members_[nextMember_] = {nextMember_, name};
        return nextMember_++;
    }
    std::vector<int> search(const std::string& word) const {
        std::vector<int> found;
        for (const auto& b : books_) {
            if (b.title.find(word) != std::string::npos) {
                found.push_back(b.id);
            }
        }
        return found;
    }
    void borrow(int bookId, int memberId) {
        Book& b = find(bookId);
        if (!members_.contains(memberId)) {
            throw std::invalid_argument("no such member");
        }
        if (b.borrowedBy) {
            throw std::runtime_error("already borrowed");
        }
        b.borrowedBy = memberId;
    }
    void giveBack(int bookId) {
        Book& b = find(bookId);
        if (!b.borrowedBy) {
            throw std::runtime_error("not borrowed");
        }
        b.borrowedBy.reset();
    }
    const Book& book(int id) {
        return find(id);
    }
    void save(const std::string& file) const {
        std::ofstream out(file);
        for (const auto& b : books_) {
            out << b.id << ',' << b.title << ',' << b.author << ',';
            out << b.borrowedBy.value_or(0) << '\n';
        }
    }

private:
    Book& find(int id) {
        for (auto& b : books_) {
            if (b.id == id) {
                return b;
            }
        }
        throw std::out_of_range("no such book");
    }
    std::vector<Book> books_;
    std::map<int, Member> members_;
    int nextBook_ = 1;
    int nextMember_ = 1;
};

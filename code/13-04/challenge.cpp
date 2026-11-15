#include <iostream>
#include <map>
#include <optional>
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
    int countBooks(const std::string& author) const {
        int n = 0;
        for (const auto& b : books_) {
            n += b.author == author;
        }
        return n;
    }
    void list() const {
        for (const auto& b : books_) {
            std::cout << b.id << ' ' << b.title;
            std::cout << " / " << b.author;
            std::cout << (b.borrowedBy ? " (out)" : "") << '\n';
        }
        std::cout << members_.size() << " members\n";
    }

private:
    std::vector<Book> books_;
    std::map<int, Member> members_;
    int nextBook_ = 1;
    int nextMember_ = 1;
};

int main() {
    Library lib;
    lib.addBook("Harbour Stories", "Chan");
    lib.addBook("Night Market", "Wong");
    lib.addBook("Learning C++", "Lee");
    lib.addMember("Amy");
    lib.addMember("Ben");
    lib.addBook("Harbour Food", "Chan");
    std::cout << lib.countBooks("Chan") << '\n';
}

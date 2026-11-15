#include <algorithm>
#include <chrono>
#include <deque>
#include <iostream>
#include <string>
#include <thread>
#include <sys/select.h>
#include <termios.h>
#include <unistd.h>

using namespace std::chrono_literals;

const int W = 20;
const int H = 10;

struct Point {
    int x;
    int y;
    bool operator==(const Point&) const = default;
};
using Snake = std::deque<Point>;

bool isWall(Point p) {
    return p.x == 0 || p.x == W - 1 || p.y == 0 || p.y == H - 1;
}

struct RawMode {
    termios old{};
    RawMode() {
        tcgetattr(STDIN_FILENO, &old);
        termios raw = old;
        raw.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &raw);
    }
    ~RawMode() {
        tcsetattr(STDIN_FILENO, TCSANOW, &old);
    }
};

char readKey() {
    fd_set set;
    FD_ZERO(&set);
    FD_SET(STDIN_FILENO, &set);
    timeval none{0, 0};
    char c = 0;
    if (select(1, &set, nullptr, nullptr, &none) > 0) {
        if (read(STDIN_FILENO, &c, 1) != 1) {
            c = 0;
        }
    }
    return c;
}

void draw(const Snake& snake) {
    std::string out = "\x1b[2J\x1b[H";
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            char c = isWall({x, y}) ? '#' : ' ';
            for (std::size_t i = 0; i < snake.size(); i++) {
                if (snake[i] == Point{x, y}) {
                    c = i == 0 ? 'O' : 'o';
                }
            }
            out += c;
        }
        out += '\n';
    }
    std::cout << out << std::flush;
}

int main() {
    RawMode raw;
    Snake snake{{5, 5}, {4, 5}, {3, 5}};
    Point dir{1, 0};
    while (true) {
        char k = readKey();
        if (k == 'w' && dir.y == 0) {
            dir = {0, -1};
        } else if (k == 's' && dir.y == 0) {
            dir = {0, 1};
        } else if (k == 'a' && dir.x == 0) {
            dir = {-1, 0};
        } else if (k == 'd' && dir.x == 0) {
            dir = {1, 0};
        } else if (k == 'p') {
            while (readKey() != 'p') {
                std::this_thread::sleep_for(50ms);
            }
        } else if (k == 'q') {
            break;
        }
        Point head = snake.front();
        head.x += dir.x;
        head.y += dir.y;
        bool self = std::ranges::find(snake, head) != snake.end();
        if (isWall(head) || self) {
            break;
        }
        snake.push_front(head);
        snake.pop_back();
        draw(snake);
        std::this_thread::sleep_for(200ms);
    }
    std::cout << "game over!\n";
}

#include <chrono>
#include <deque>
#include <iostream>
#include <string>
#include <thread>

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
    Snake snake{{5, 5}, {4, 5}, {3, 5}};
    Point dir{1, 0};
    for (int tick = 0; tick < 13; tick++) {
        Point head = snake.front();
        head.x += dir.x;
        head.y += dir.y;
        snake.push_front(head);
        snake.pop_back();
        draw(snake);
        std::this_thread::sleep_for(200ms);
    }
}

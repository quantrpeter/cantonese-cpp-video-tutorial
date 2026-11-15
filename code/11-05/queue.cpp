#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

std::queue<int> jobs;
std::mutex m;
std::condition_variable cv;
bool finished = false;

void producer() {
    for (int i = 1; i <= 5; i++) {
        {
            std::scoped_lock lock(m);
            jobs.push(i);
        }
        cv.notify_one();
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    {
        std::scoped_lock lock(m);
        finished = true;
    }
    cv.notify_one();
}

void consumer() {
    while (true) {
        std::unique_lock lock(m);
        cv.wait(lock, [] { return !jobs.empty() || finished; });
        if (jobs.empty()) {
            break;
        }
        int job = jobs.front();
        jobs.pop();
        lock.unlock();
        std::cout << "got " << job << '\n';
    }
}

int main() {
    std::jthread c(consumer);
    std::jthread p(producer);
}

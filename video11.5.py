#!/usr/bin/env python3
"""Video 130 (syllabus 11.5): condition_variable

Producer / consumer: the producer pushes jobs 1..5 into a std::queue (200 ms apart) under a
mutex and calls notify_one; the consumer sleeps in cv.wait(lock, predicate) until there is a job
or the producer has finished. The real run prints got 1 … got 5 over about a second, then both
threads end. Run `python3 video11.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 130
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-05"
FINAL = (CODE / "queue.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    for i in range(start - 1, len(LINES)):
        if text in LINES[i]:
            return i + 1
    raise ValueError(text)


CC = "g++ -std=c++20 -Wall -Wextra queue.cpp -o q"

(c1, r1, cch, rch) = cpp.session({"queue.cpp": FINAL}, [
    CC, "./q", Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "got 1\ngot 2\ngot 3\ngot 4\ngot 5\n" and r1.seconds > 0.8, r1.output
assert c1.code == cch.code == 0 and rch.output == "55\n"

SAY = {"std::condition_variable": "S T D condition variable", "condition_variable": "condition variable", "cv.wait": "c v 點 wait",
       "wait": "wait", "notify_one": "notify one", "notify_all": "notify all", "std::unique_lock": "S T D unique lock", "unique_lock": "unique lock",
       "scoped_lock": "scoped lock", "producer": "producer", "consumer": "consumer", "finished": "finished", "jobs": "jobs", "got": "got",
       "spurious wakeup": "spurious wakeup", "lambda": "lambda"}

s = Stage({"queue.cpp": FINAL}, title="condition_variable", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！一個 thread 負責生產工作，另一個負責處理。處理嘅嗰個，冇工作嘅時候應該點？不停問「有冇嘢做」好嘥 CPU。今集學 condition_variable：瞓低等，有嘢做先叫醒。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "producer · consumer · wait · notify")),
    Scene("goal",
          "今集會講：[[b1]]生產者同消費者；[[b2]]notify 叫醒；[[b3]]wait 加條件；[[b4]]點樣通知完工。",
          BulletCard("今集學識", [("producer / consumer", "b1"), ("cv.notify_one()", "b2"), ("cv.wait(lock, 條件)", "b3"), ("finished 旗", "b4")])),
    Scene("shared",
          "[[q]]共用嘅嘢：一條工作 queue，[[m]]一個 mutex 保護佢，[[cv]]一個 condition_variable 用嚟叫醒人，[[f]]仲有一個 finished，表示生產完未。",
          s.scene(Open("queue.cpp", at="q"), Mark(ln("std::queue<int> jobs"), at="q"), Mark(ln("std::mutex m"), at="m"),
                  Mark(ln("std::condition_variable cv"), at="cv"), Mark(ln("bool finished"), at="f"))),
    Scene("producer",
          "[[push]]生產者：鎖住 mutex，放一個工作入 queue；[[notify]]解鎖之後 notify_one，叫醒一個等緊嘅人；[[sleep]]每二百毫秒做一個，扮做慢慢生產。[[done]]做完五個，設定 finished，再叫醒佢。",
          s.scene(Mark((ln("std::scoped_lock lock(m);"), ln("jobs.push(i);")), at="push"), Mark(ln("cv.notify_one();"), at="notify"),
                  Mark(ln("sleep_for"), at="sleep"), Mark((ln("finished = true;") - 2, ln("cv.notify_one();", ln("finished = true;"))), at="done"))),
    Scene("consumer",
          "[[lock]]消費者用 unique_lock，因為 wait 需要暫時放開個鎖。[[wait]]cv.wait 會瞓低，直到被叫醒，而且條件成立：有工作，或者已經完工。[[exit]]queue 空而且完工，就離開；"
          "[[take]]否則攞一個工作，先解鎖，再慢慢處理。",
          s.scene(Mark(ln("std::unique_lock lock(m);"), at="lock"), Mark(ln("cv.wait(lock"), at="wait"), Mark((ln("if (jobs.empty())"), ln("break;") + 1), at="exit"),
                  Mark((ln("int job = jobs.front();"), ln('std::cout << "got "')), at="take"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]got 一、got 二……每隔一陣先出一個，因為消費者真係瞓咗喺度等，有工作先醒。五個做完，兩個 thread 都結束。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o", stream=True))),
    Scene("why",
          "幾個重點：[[pred]]wait 一定要加條件，因為 thread 有時會無故醒，叫 spurious wakeup，有條件先唔會出錯；[[lock]]改共用資料之前一定要鎖；[[done]]要有方法話消費者知已經完工，唔係佢會永遠等。",
          BulletCard("記住", [("wait 一定加條件（spurious wakeup）", "pred"), ("改共用資料：先鎖", "lock"), ("要通知完工", "done")])),
    Scene("recap",
          "總結：[[r1]]condition_variable 令 thread 瞓低等，唔使不停問；[[r2]]生產者 push 完 notify_one；[[r3]]消費者用 unique_lock 加 wait 同條件；[[r4]]用 finished 通知完工。",
          BulletCard("今集重點", [("瞓低等，唔好不停問", "r1"), ("push + notify_one", "r2"), ("unique_lock + wait(條件)", "r3"), ("finished", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]改做生產一到十，消費者唔印，而係加埋所有工作，最後 main 印總和。[[next]]下一集：async 同 future。多謝收睇，下次見！",
          EndCard("生產 1 到 10，消費者將工作加入 total，兩個 thread 完咗之後 main 印 total：55。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

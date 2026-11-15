#!/usr/bin/env python3
"""Video 127 (syllabus 11.2): Data race 同 mutex

Two jthreads each add 1 to a shared counter 100,000 times. Unprotected, two real runs print two
different numbers, both below 200000; built with -fsanitize=thread, ThreadSanitizer really
reports "WARNING: ThreadSanitizer: data race" at race.cpp:10. With a std::mutex and
std::lock_guard the run prints 200000. Run `python3 video11.2.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 127
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-02"
FINAL = (CODE / "race.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LOCK = "        std::lock_guard<std::mutex> lock(m);\n"
BAD = FINAL.replace(LOCK, "")
CC = "g++ -std=c++20 -Wall -Wextra race.cpp -o race"
TS = "g++ -std=c++20 -g -fsanitize=thread race.cpp -o ts"

(c1, r1, r1b, clr, ct, rt, clr2, c2, r2, cch, rch) = cpp.session({"race.cpp": BAD}, [
    CC, "./race", "./race", "clear", TS, "./ts", "clear", Write("race.cpp", FINAL), CC, "./race",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
a, b = int(r1.output), int(r1b.output)
assert a < 200000 and b < 200000 and a != b, (a, b)
assert "WARNING: ThreadSanitizer: data race" in rt.output and "race.cpp:10" in rt.output, rt.output[:300]
assert r2.output == "200000\n" and c1.code == ct.code == c2.code == cch.code == 0 and rch.output == "2000\n"
D = "零一二三四五六七八九"


def zh(n):
    return "".join(D[int(c)] for c in str(n))


SAY = {"data race": "data race", "std::mutex": "S T D mutex", "mutex": "mutex", "std::lock_guard": "S T D lock guard", "lock_guard": "lock guard",
       "std::scoped_lock": "S T D scoped lock", "scoped_lock": "scoped lock", "ThreadSanitizer": "Thread Sanitizer", "-fsanitize=thread": "f sanitize thread",
       "counter++": "counter 加加", "counter": "counter", "jthread": "j thread", "RAII": "R A I I", "lock": "lock", "unlock": "unlock"}

s = Stage({"race.cpp": BAD}, title="Data race 同 mutex", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！兩個 thread 同時改同一個變數，會發生咩事？今集睇一個真正壞咗嘅計數器，用 ThreadSanitizer 捉佢，再用 mutex 修好。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "data race · mutex · lock_guard")),
    Scene("goal",
          "今集會講：[[b1]]data race 係乜；[[b2]]用 ThreadSanitizer 捉；[[b3]]mutex 同 lock_guard；[[b4]]scoped_lock。",
          BulletCard("今集學識", [("data race", "b1"), ("-fsanitize=thread", "b2"), ("std::mutex + lock_guard", "b3"), ("std::scoped_lock", "b4")])),
    Scene("race",
          f"[[code]]兩個 thread 各自將 counter 加十萬次，答案應該係二十萬。[[cc]]編譯運行：[[o1]]{zh(a)}？[[o2]]再運行一次：{zh(b)}！次次唔同，而且都唔夠。",
          s.scene(Open("race.cpp", at="code"), Mark((8, 12), at="code"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1, at="o1"), Run(r1b, at="o2"))),
    Scene("why",
          "[[three]]counter 加加其實係三步：讀出嚟、加一、寫返去。[[mix]]兩個 thread 同時做，可能一齊讀到同一個舊值，各自加一再寫返，結果只係加咗一次。呢個就叫 data race。",
          TableCard("counter++ 被打斷", ["時間", "thread A", "thread B"], [
              (["①", "讀 counter = 5", ""], "three"),
              (["②", "", "讀 counter = 5"], "mix"),
              (["③", "寫 6", ""], "mix"),
              (["④", "", "寫 6（應該係 7！）"], "mix", RED),
          ], widths=[0.6, 1.4, 1.6], code_cols=(), size=38)),
    Scene("tsan",
          "[[cc]]用 ThreadSanitizer 編譯，即係 f sanitize thread。運行：[[o]]WARNING：data race，仲講明係第十行，兩個 thread 同時讀寫 counter。",
          s.scene(Run(clr, at="cc"), Run(ct), Run(rt, at="o"), Scroll(at="o"), Mark(10, at="o"))),
    Scene("mutex",
          "[[m]]用一個 std::mutex 保護 counter。[[type]]加 counter 之前，用 lock_guard 鎖住 m：同一時間只有一個 thread 可以入嚟；離開大括號，lock_guard 解構，自動解鎖，又係 RAII。"
          "[[cc]]運行：[[o]]二十萬，啱晒。再運行幾多次都係二十萬。",
          s.scene(Mark(6, at="m"), Run(clr2, at="type"), Type("race.cpp", LOCK, after="    for (int i = 0; i < 100000; i++) {\n", at="type", rate=40),
                  Expect("race.cpp", FINAL), Mark(10, at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("locks",
          "[[lg]]lock_guard 鎖一個 mutex；[[sl]]C++17 嘅 scoped_lock 可以一次鎖幾個，寫法仲短；[[manual]]唔好自己 lock 同 unlock，中間一 throw 就永遠唔解鎖。",
          TableCard("點樣鎖", ["寫法", "說明"], [
              (["std::lock_guard<std::mutex> l(m);", "鎖一個，離開範圍自動解"], "lg"),
              (["std::scoped_lock l(m);", "C++17：可以鎖幾個"], "sl", GREEN),
              (["m.lock(); … m.unlock();", "唔好：throw 咗就唔解"], "manual", RED),
          ], widths=[1.9, 1.5], code_cols=(0,), size=34)),
    Scene("recap",
          "總結：[[r1]]幾個 thread 同時讀寫同一個變數，冇保護就係 data race；[[r2]]結果亂，而且次次唔同；[[r3]]ThreadSanitizer 捉到；[[r4]]用 mutex 加 lock_guard 或者 scoped_lock 保護。",
          BulletCard("今集重點", [("data race：同時讀寫", "r1"), ("結果唔穩定", "r2"), ("-fsanitize=thread", "r3"), ("mutex + lock_guard / scoped_lock", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]兩個 thread 各自 push_back 一千個數入同一個 vector，用 scoped_lock 保護，最後 size 應該係二千。[[next]]下一集：atomic。多謝收睇，下次見！",
          EndCard("兩個 jthread 各 push_back 1000 次入同一個 vector；用 std::scoped_lock 保護，size 應該係 2000。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

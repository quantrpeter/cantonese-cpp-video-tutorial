#!/usr/bin/env python3
"""Video 132 (syllabus 11.7): 小項目：平行搵質數

Count the primes below 3,000,000 (216816 of them) with 1, 2 and 4 threads, built with -O2.
First version: thread t takes n = t, t + threads, …; the real timings barely improve with 2
threads, because one thread gets all the even numbers (instant) and the other all the odd ones.
Final version: threads grab chunks of 1000 from an std::atomic<int> next, so the work is shared
evenly and the real timings drop with more threads. Spoken numbers are the measured ones.
Run `python3 video132.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 132
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-07"
FINAL = (CODE / "primes.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LAMBDA_F = "        workers.emplace_back([&count, &next, limit] {" + FINAL.split("        workers.emplace_back([&count, &next, limit] {")[1].split("        });\n")[0]
LAMBDA_1 = ("        workers.emplace_back([&count, limit, threads, t] {\n            int mine = 0;\n"
            "            for (int n = t; n < limit; n += threads) {\n                if (isPrime(n)) {\n                    mine++;\n"
            "                }\n            }\n            count += mine;\n")
V1 = FINAL.replace(LAMBDA_F, LAMBDA_1).replace("    std::atomic<int> next{0};\n", "").replace("#include <algorithm>\n", "")
CC = "g++ -std=c++20 -O2 -Wall -Wextra primes.cpp -o pr"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"primes.cpp": V1}, [
    CC, "./pr", "clear", Write("primes.cpp", FINAL), CC, "./pr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)


def times(r):
    got = dict((int(a), int(b)) for a, b in re.findall(r"(\d+) threads: 216816 (\d+)ms", r.output))
    assert sorted(got) == [1, 2, 4], r.output
    return got


t1, t2 = times(r1), times(r2)
assert t1[2] > 0.75 * t1[1], t1          # the uneven split barely helps with 2 threads
assert t2[2] < 0.7 * t2[1] and t2[4] < t2[2], t2
assert c1.code == c2.code == cch.code == 0 and rch.output.startswith("8 threads: 216816 ")
D = "零一二三四五六七八九"


def zh(n):
    if n == 0:
        return "零"
    out, gap = "", False
    for unit, name in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        d = n // unit % 10
        if d:
            if gap and out:
                out += "零"
            out += ("" if (unit == 10 and d == 1 and not out) else D[d]) + name
            gap = False
        elif out:
            gap = True
    return out


SAY = {"isPrime": "is prime", "countPrimes": "count primes", "std::atomic": "S T D atomic", "atomic": "atomic", "fetch_add": "fetch add",
       "next": "next", "jthread": "j thread", "threads": "threads", "-O2": "O 二", "ms": "毫秒", "216816": "二十一萬六千八百一十六"}

s = Stage({"primes.cpp": V1}, title="小項目：平行搵質數", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十一部分最後一集：數三百萬以下有幾多個質數，用一個、兩個、四個 thread，睇吓快咗幾多。中間會遇到一個好常見嘅陷阱：分工唔平均。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "thread · atomic · chrono · 分工")),
    Scene("plan",
          "計劃：[[b1]]isPrime 用試除法；[[b2]]countPrimes 開幾個 thread 一齊數，結果加入 atomic；[[b3]]main 用 chrono 計一、二、四個 thread 嘅時間。",
          BulletCard("計劃", [("isPrime：試除到 √n", "b1"), ("countPrimes(limit, threads)", "b2"), ("chrono 計時：1、2、4", "b3")])),
    Scene("code",
          "[[prime]]isPrime 由二試除到開方。[[split]]第一個分工方法：第 t 個 thread 負責 t、t 加 threads、再加 threads……輪流分。[[mine]]每個 thread 自己先數，最後先加入 atomic，咁就唔使成日爭。",
          s.scene(Open("primes.cpp", mode="instant"), Mark((7, 17), at="prime"), Mark((23, 25), at="split"), Mark(30, at="mine"))),
    Scene("run1",
          f"[[cc]]用 O 二編譯運行：[[o]]一個 thread {zh(t1[1])} 毫秒；兩個 thread {zh(t1[2])} 毫秒，差唔多冇快到！四個 {zh(t1[4])} 毫秒。三次都數到二十一萬六千幾個，答案冇錯，但係點解兩個 thread 唔快？",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("uneven",
          "[[two]]兩個 thread 嘅時候：[[even]]thread 零攞晒雙數，雙數除二就知唔係質數，一下就做完；[[odd]]thread 一攞晒單數，要慢慢試除。結果一個坐喺度等，一個做晒全部。",
          TableCard("兩個 thread 輪流分", ["thread", "攞到", "工作量"], [
              (["0", "0, 2, 4, 6 …", "好少：雙數即刻唔係"], "even", GREEN),
              (["1", "1, 3, 5, 7 …", "好多：慢慢試除"], "odd", RED),
          ], widths=[0.7, 1.3, 1.8], code_cols=(1,), size=38, note=("分工唔平均：多咗 thread 都唔快", "two"))),
    Scene("fix",
          "[[next]]改法：用一個 atomic next，大家輪流去攞下一批，每批一千個數。[[grab]]fetch_add 一千，即係「攞走一批，順手將 next 推前」，唔會兩個人攞到同一批。[[end]]攞完就停。"
          "邊個做得快，就攞多啲，自然平均。",
          s.scene(Run(clr, at="next"), Replace("primes.cpp", LAMBDA_1, LAMBDA_F, at="next", rate=120),
                  Replace("primes.cpp", "    std::atomic<int> count{0};\n", "    std::atomic<int> count{0};\n    std::atomic<int> next{0};\n", rate=60),
                  Replace("primes.cpp", "#include <atomic>\n", "#include <algorithm>\n#include <atomic>\n", rate=60), Expect("primes.cpp", FINAL),
                  Mark(22, at="next"), Mark(28, at="grab"), Mark((29, 31), at="end"))),
    Scene("run2",
          f"[[cc]]再編譯運行：[[o]]一個 thread {zh(t2[1])} 毫秒，兩個 {zh(t2[2])} 毫秒，四個 {zh(t2[4])} 毫秒。今次 thread 越多越快。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(r2, at="o"))),
    Scene("lessons",
          "學到乜：[[split]]分工要平均，唔係多開 thread 都冇用；[[local]]每個 thread 先自己數，最後先合併，減少爭用；[[measure]]一定要量度，唔好估；[[limit]]thread 數唔好多過 CPU 核心太多。",
          BulletCard("平行運算嘅教訓", [("分工要平均", "split"), ("先自己數，最後合併", "local"), ("一定要量度", "measure"), ("thread 數 ≈ 核心數", "limit")])),
    Scene("recap",
          "總結：[[r1]]用 jthread 分工，用 atomic 收結果；[[r2]]輪流分可能唔平均；[[r3]]用 atomic 計數器動態派工，最平均；[[r4]]用 chrono 量度加速。第十一部分完成！",
          BulletCard("今集重點", [("jthread + atomic", "r1"), ("輪流分：可能唔平均", "r2"), ("fetch_add 動態派工", "r3"), ("chrono 量度", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]試吓用八個 thread，睇吓仲有冇快；你部電腦有幾多個核心，就係上限。[[next]]下一集開始第十二部分：演算法同競賽，第一集係競賽寫法。多謝收睇，下次見！",
          EndCard("改用 8 個 thread 再計時：仲快唔快？同你部電腦嘅核心數比較。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

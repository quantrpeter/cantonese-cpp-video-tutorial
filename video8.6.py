#!/usr/bin/env python3
"""Video 93 (syllabus 8.6): unordered_map

8.5's word count with std::unordered_map really prints the words in no particular order (bat,
hat, and, cat, the). 2,000,000 inserts and lookups built with -O2: `time ./m` (std::map) really
takes 0.46 s, `time ./u` (std::unordered_map) 0.06 s. Hashing explains both: average O(1),
no order. Run `python3 video8.6.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 93
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-06"
FINAL = (CODE / "words.cpp").read_text()
M = (CODE / "m.cpp").read_text()
U = (CODE / "u.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
V0 = FINAL.replace("#include <unordered_map>\n#include <string>\n", "#include <map>\n#include <string>\n").replace("std::unordered_map<", "std::map<")
CC = "g++ -std=c++20 -Wall -Wextra words.cpp -o words"
IN = ["the cat and the hat", "and the bat", "^D"]

(c1, r1, cm, cu, tm, tu, cch, rch) = cpp.session({"words.cpp": FINAL, "m.cpp": M, "u.cpp": U}, [
    CC, Input("./words", IN), "g++ -std=c++20 -O2 m.cpp -o m", "g++ -std=c++20 -O2 u.cpp -o u", "time ./m", "time ./u",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
lines = r1.output.split("\n")[2:7]
assert sorted(lines) == ["and 2", "bat 1", "cat 1", "hat 1", "the 3"] and lines != sorted(lines), r1.output


def secs(r):
    return float(re.search(r"real\s+0m([\d.]+)s", r.output).group(1))


ms, us = secs(tm), secs(tu)
assert tm.output.startswith("1999999000000\n") and tu.output.startswith("1999999000000\n") and ms > 3 * us, (ms, us)
assert c1.code == cm.code == cu.code == cch.code == 0 and rch.output == "5 5\n"
ZH = dict(zip("0123456789", "零一二三四五六七八九"))


def zh(x):
    a, b = f"{x:.2f}".split(".")
    return "".join(ZH[c] for c in a) + "點" + "".join(ZH[c] for c in b)


say_ms, say_us = zh(ms), zh(us)

SAY = {"std::unordered_map": "S T D unordered map", "unordered_map": "unordered map", "std::map": "S T D map", "hash": "hash",
       "O(1)": "O 一", "O(log n)": "O log n", "-O2": "O 二", "time": "time", "bucket": "bucket", "std::hash": "S T D hash",
       "bat": "bat", "hat": "hat", "and": "and", "cat": "cat", "the": "the"}

s = Stage({"words.cpp": V0, "m.cpp": M}, title="unordered_map", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！map 永遠排好序，但係好多時我哋根本唔需要次序，只想查得快。今集學 unordered_map：用 hash，平均一步就搵到。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "hash · 平均 O(1) · 冇次序")),
    Scene("goal",
          "今集會講：[[b1]]unordered_map 點用；[[b2]]佢冇次序；[[b3]]hash 點運作；[[b4]]快幾多，幾時揀邊個。",
          BulletCard("今集學識", [("用法同 map 一樣", "b1"), ("冇次序", "b2"), ("hash 同 bucket", "b3"), ("map vs unordered_map", "b4")])),
    Scene("swap",
          "[[open]]上一集嘅數字程式。[[type]]將 map 換做 unordered_map，include 都要換。其他一個字都唔使改，用法一樣。",
          s.scene(Open("words.cpp", at="open"), Replace("words.cpp", "#include <map>\n", "#include <unordered_map>\n", at="type", rate=30),
                  Replace("words.cpp", "std::map<", "std::unordered_map<", rate=30), Expect("words.cpp", FINAL), Mark(6, at="type"))),
    Scene("run1",
          "[[cc]]編譯運行，輸入同樣兩行。[[o]]次數全部啱，但係次序亂咗：bat、hat、and……唔再按字母排。呢個次序亦唔保證，換部機或者多放幾個字都可能會變。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, type_rate=24), Note("次數啱\n但係冇次序", at="o", where="editor"))),
    Scene("hash",
          "點解？[[fn]]unordered_map 用一個 hash 函數，將 key 變成一個數，[[bucket]]直接決定放入邊個 bucket。[[fast]]查嘅時候再計一次，就知去邊個 bucket 搵，"
          "平均一步搞掂。[[order]]但係 bucket 嘅次序同字母無關，所以冇次序。",
          BoxesCard("hash：key → bucket", [
              BoxRow([Box("key", "\"cat\"", "", at="fn", color=BLUE, w=240, key="k"), Box("hash", "std::hash", "計一個數", at="fn", color=PURPLE, w=280, key="h")],
                     gap=120),
              BoxRow([Box("", "bat", "0", at="bucket", w=150), Box("", "", "1", at="bucket", w=150), Box("", "cat", "2", at="bucket", color=GREEN, w=150, key="b2"),
                      Box("", "the", "3", at="bucket", w=150), Box("", "and", "4", at="bucket", w=150)], gap=10, label="bucket"),
          ], arrows=[("k", "h", "fn", PURPLE), ("h", "b2", "bucket", GREEN)], notes=[("平均 O(1)：一步就搵到", "fast"), ("bucket 次序 ≠ 字母次序", "order")],
              top=CONTENT_TOP, row_h=250, box_h=110, size=38)),
    Scene("speed",
          "快幾多？[[open]]m.cpp 用 map，放兩百萬個 key，再逐個查一次；u.cpp 一模一樣，只係換咗 unordered_map。[[cc]]兩個都用 O 二編譯，再用 time 計時。"
          f"[[m]]map 用咗 {say_ms} 秒，[[u]]unordered_map 只用 {say_us} 秒，快咗幾倍。數據越多，差距越明顯。",
          s.scene(Note(None), Open("m.cpp", at="open"), Mark((6, 8), at="open"), Mark(None, at="cc"), Run(cm, at="cc"), Run(cu), Run(tm, at="m"), Run(tu, at="u"))),
    Scene("compare",
          "點揀？[[ord]]要次序，例如由細到大印，用 map；[[spd]]淨係要查得快，用 unordered_map；[[key]]map 嘅 key 要識比較細過，unordered_map 嘅 key 要識 hash。"
          "int 同 string 兩樣都識。",
          TableCard("map vs unordered_map", ["", "map", "unordered_map"], [
              (["次序", "按 key 排好", "冇次序"], "ord"),
              (["查一次", "O(log n)", "平均 O(1)"], "spd"),
              (["key 要識", "<", "std::hash、=="], "key"),
          ], widths=[0.8, 1.2, 1.4], code_cols=(), size=40)),
    Scene("recap",
          "總結：[[r1]]unordered_map 用法同 map 一樣；[[r2]]用 hash，平均一步搵到；[[r3]]代價係冇次序；[[r4]]唔使次序，就揀 unordered_map。",
          BulletCard("今集重點", [("用法同 map 一樣", "r1"), ("hash：平均 O(1)", "r2"), ("冇次序", "r3"), ("唔使次序 → unordered_map", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 unordered_map 數 abracadabra，印出 a 嘅次數，同埋有幾多種唔同嘅字母。[[next]]下一集：set 同 multiset。多謝收睇，下次見！",
          EndCard("用 std::unordered_map<char, int> 數 \"abracadabra\"：印 freq['a'] 同 freq.size()。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

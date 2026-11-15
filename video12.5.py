#!/usr/bin/env python3
"""Video 137 (syllabus 12.5): 二分答案

Seven parcels 4 8 2 6 5 3 7 go, in order, onto 3 trucks; what is the smallest possible maximum
load? canShip(cap) answers "is cap enough?" greedily, and the answers are no…no ok…ok, so binary
search over cap between max (8) and sum (35). The real run prints its tries (21 ok, 14 ok, 11 no,
13 ok, 12 no) and answer 13. The challenge finds ⌊√1000000⌋ = 1000 the same way.
Run `python3 video12.5.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 137
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-05"
FINAL = (CODE / "trucks.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"trucks.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 trucks.cpp -o tr", "./tr < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "try 21 ok\ntry 14 ok\ntry 11 no\ntry 13 ok\ntry 12 no\nanswer 13\n", r1.output
assert c1.code == cch.code == 0 and rch.output == "1000\n"

SAY = {"canShip": "can ship", "cap": "cap", "lo": "lo", "hi": "hi", "mid": "mid", "ok": "OK", "no": "no", "max_element": "max element",
       "accumulate": "accumulate", "O(n log S)": "O n log S", "in.txt": "in 點 t x t", "cat": "cat", "answer": "answer", "try": "try"}

s = Stage({"trucks.cpp": FINAL}, title="二分答案", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！有啲題目直接計答案好難，但係如果俾你一個答案，檢查佢得唔得就好易。咁就可以二分搜尋個答案。今集學二分答案。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "檢查容易 · 二分個答案")),
    Scene("problem",
          "[[p]]七件貨，按次序放上三架貨車，每架車要連續嘅一段。[[goal]]想最重嗰架車盡量輕，最少可以係幾重？[[hard]]直接諗好難，有好多種分法。",
          BulletCard("題目", [("7 件貨：4 8 2 6 5 3 7，按次序", "p"), ("分去 3 架車，每架一段連續嘅", "p"), ("最重嗰架最少幾重？", "goal")])),
    Scene("check",
          "[[fn]]但係反過嚟問：每架車最多載 cap，三架夠唔夠？[[greedy]]好易：由頭開始裝，裝唔落就開新一架，最後數用咗幾架。[[mono]]而且 cap 越大越易成功：細嘅全部唔得，大過某個數之後全部得。",
          s.scene(Open("trucks.cpp", at="fn"), Mark((4, 15), at="fn"), Mark((8, 11), at="greedy"))),
    Scene("line",
          "[[no]]所以答案排落去係：唔得、唔得、唔得……[[ok]]然後得、得、得。[[find]]我哋要搵第一個得，即係二分搜尋可以做嘅事。",
          BoxesCard("cap 由細到大", [
              BoxRow([Box("", "8", "no", at="no", color=RED, w=110), Box("", "…", "no", at="no", color=RED, w=110), Box("", "12", "no", at="no", color=RED, w=110),
                      Box("", "13", "ok", at="find", color=GREEN, w=110), Box("", "14", "ok", at="ok", color=GREEN, w=110), Box("", "…", "ok", at="ok", color=GREEN, w=110),
                      Box("", "35", "ok", at="ok", color=GREEN, w=110)], gap=10),
          ], notes=[("搵第一個 ok", "find")], top=CONTENT_TOP + 60, row_h=250, box_h=110, size=40)),
    Scene("search",
          "[[range]]答案一定喺最重嗰件，八，到總重，三十五之間。[[loop]]每次試中間 mid：[[ok]]得，答案可能係 mid 或者更細，hi 移去 mid；[[no]]唔得，就要更大，lo 移去 mid 加一。",
          s.scene(Mark((24, 25), at="range"), Mark((26, 28), at="loop"), Mark((30, 31), at="ok"), Mark((32, 33), at="no"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]試二十一，得；十四，得；十一，唔得；十三，得；十二，唔得。答案係十三，只係試咗五次。",
          s.scene(Mark(None), Run(cat, at="cc"), Run(c1), Run(r1, at="o"))),
    Scene("pattern",
          "二分答案嘅套路：[[ask]]將「最少幾多」改成「X 得唔得」；[[mono]]確定得唔得係單調，即係一過咗某點就一直得；[[bs]]再二分搜尋。時間係檢查一次嘅時間，乘 log 範圍。",
          BulletCard("二分答案套路", [("問題變成：X 得唔得？", "ask"), ("確認單調：過咗某點就一直得", "mono"), ("二分搜尋 X", "bs")])),
    Scene("recap",
          "總結：[[r1]]直接計難，檢查容易，就諗二分答案；[[r2]]寫一個 check 函數；[[r3]]得就收細上限，唔得就提高下限；[[r4]]複雜度係 n 乘 log 範圍。",
          BulletCard("今集重點", [("檢查容易 → 二分答案", "r1"), ("check(x)", "r2"), ("ok：hi = mid；no：lo = mid + 1", "r3"), ("O(n log S)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]唔用 sqrt，用二分答案搵一百萬嘅平方根整數部分：最大嘅 x，令 x 乘 x 唔超過一百萬。[[next]]下一集：貪心。多謝收睇，下次見！",
          EndCard("二分搵最大嘅 x，令 x × x ≤ 1000000（答案 1000）。留意要用 mid = (lo + hi + 1) / 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

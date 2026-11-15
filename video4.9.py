#!/usr/bin/env python3
"""Video 50 (syllabus 4.9): 自己寫搜尋同排序

findIndex() is a linear search (3 for 64, -1 for 50); bubble sort with std::swap prints the
vector after every pass; writing `i + pass <= v.size()` reads one past the end and really stops
at g++ 15's assertion; `<` fixes it. Run `python3 video50.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 50
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-09"
SEARCH = (CODE / "find.cpp").read_text()
SORT = (CODE / "sort.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BUG = SORT.replace("i + pass < v.size()", "i + pass <= v.size()")
CS = "g++ -std=c++20 -Wall -Wextra find.cpp -o find"
CB = "g++ -std=c++20 -Wall -Wextra sort.cpp -o sort"
START = [72, 45, 91, 64, 85]

(c1, r1, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"find.cpp": SEARCH, "sort.cpp": BUG}, [
    CS, "./find", "clear", CB, "./sort", Write("sort.cpp", SORT), CB, "./sort",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["3", "-1"]
assert "Assertion '__n < this->size()' failed" in r2.output and r2.code != 0, r2.output
passes = r3.output.rstrip("\n").split("\n")
assert passes[0] == "45 72 64 85 91 " and passes[-1] == "45 64 72 85 91 " and len(passes) == 4, passes
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.strip() == "91 85 72 64 45"

steps, v = [], START[:]                       # the comparisons of the first pass, for the card
for i in range(len(v) - 1):
    a, b = v[i], v[i + 1]
    swap = a > b
    if swap:
        v[i], v[i + 1] = b, a
    steps.append((f"{a} > {b}？", "交換" if swap else "唔換", " ".join(map(str, v))))
assert steps[-1][2] + " " == passes[0]

SAY = {"findIndex": "find index", "std::swap": "S T D swap", "bubbleSort": "bubble sort", "-1": "負一",
       "i + pass <= v.size()": "i 加 pass 細過或等於 size"}

s = Stage({"find.cpp": SEARCH, "sort.cpp": BUG}, title="自己寫搜尋同排序", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！標準庫有現成嘅搜尋同排序，第八章會學。今集我哋先自己動手寫一次，了解背後係點運作。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "線性搜尋 · 泡沫排序 · std::swap")),
    Scene("goal",
          "今集會講：[[b1]]線性搜尋；[[b2]]用 std::swap 交換兩個值；[[b3]]泡沫排序。",
          BulletCard("今集學識", [("線性搜尋 linear search", "b1"), ("std::swap", "b2"), ("泡沫排序 bubble sort", "b3")])),
    Scene("search",
          "[[open]]findIndex 由頭到尾逐個比較：[[hit]]搵到，就即刻回傳位置；[[miss]]成個 vector 都冇，就回傳負一，代表搵唔到。"
          "[[cc]]編譯運行，[[o]]六十四喺位置三；五十，搵唔到，負一。",
          s.scene(Open("find.cpp", at="open"), Mark((5, 9), at="open"), Mark(7, at="hit"), Mark(10, at="miss"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("idea",
          "跟住係排序。泡沫排序嘅諗法係：[[cmp]]由頭開始，兩個兩個比較，前面嗰個大過後面嗰個，就交換。"
          "[[end]]行完一輪，最大嘅數就好似泡泡咁，浮咗去最尾。",
          TableCard("第一輪：兩個兩個比較", ["比較", "做咩", "之後"], [
              (list(st), ("cmp", 0.8 * k)) + ((GREEN,) if k == len(steps) - 1 else ()) for k, st in enumerate(steps)
          ], widths=[1, 0.7, 1.6], code_cols=(0, 2), size=40, note=("最大嘅 91 浮咗去最尾", "end"))),
    Scene("sort",
          "[[open]]寫成程式：[[outer]]外層迴圈係第幾輪；[[inner]]內層迴圈兩個兩個比較；[[swap]]需要交換，就用 std::swap。"
          "[[show]]每輪完咗，印出成個 vector 睇吓。",
          s.scene(Run(clr, at="open"), Open("sort.cpp", at="open"), Mark(13, at="outer"), Mark(14, at="inner"), Mark((15, 17), at="swap"),
                  Mark(19, at="show"))),
    Scene("bug",
          "[[cc]]編譯運行：[[o]]第一輪都未完，就停咗：Assertion failed，又係出界！[[why]]內層條件用咗細過或等於：i 去到最尾一格，"
          "i 加一就超出咗 vector，4.3 講過嘅情況。",
          s.scene(Mark(None), Run(c2, at="cc"), Run(r2), Mark(14, at="why"),
                  Note("<= 多行咗一次\nv[i + 1] 出界", at="why", where="editor"))),
    Scene("fix",
          "[[fix]]改返做細過。[[cc]]再編譯運行，[[o]]每一輪印一行：第一輪九十一去咗最尾，第二輪八十五都排好咗，最後由細到大排好晒。",
          s.scene(Note(None), Replace("sort.cpp", "i + pass <= v.size()", "i + pass < v.size()", at="fix"), Expect("sort.cpp", SORT),
                  Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("speed",
          "自己寫完，就知道佢哋幾慢：[[lin]]線性搜尋，一千個數最多比較一千次；[[bub]]泡沫排序，一千個數要比較大約五十萬次。"
          "[[std]]第八章嘅 std::sort 同二分搜尋，會快好多。",
          TileCard("有幾快？", [
              Tile("🔍", "線性搜尋", "n 個數：最多比較 n 次", "lin", BLUE),
              Tile("🫧", "泡沫排序", "n 個數：大約 n² ÷ 2 次比較", "bub", AMBER),
          ], cols=2, height=330, footer=("第八章：std::sort、二分搜尋", "std"))),
    Scene("recap",
          "總結：[[r1]]線性搜尋逐個比較，搵唔到就回傳負一；[[r2]]std::swap 交換兩個值；[[r3]]泡沫排序兩個兩個比較，每輪將最大嘅推去最尾；"
          "[[r4]]小心迴圈邊界，唔好出界。",
          BulletCard("今集重點", [("線性搜尋：搵唔到回傳 -1", "r1"), ("std::swap(a, b)", "r2"),
                                ("泡沫排序：每輪最大嘅去最尾", "r3"), ("小心邊界：i + 1 唔可以出界", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]改吓 bubbleSort，令佢由大排到細。[[next]]下一集係第四章嘅小項目：井字過三關。多謝收睇，下次見！",
          EndCard("改吓 bubbleSort，令佢由大排到細。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

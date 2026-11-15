#!/usr/bin/env python3
"""Video 124 (syllabus 10.7): 效能入門

A 4000 × 4000 grid stored in one vector, summed row by row and column by column and timed with
steady_clock. Built with -O0 and then -O2, the real runs show both effects: -O2 is several times
faster, and walking by columns is several times slower than by rows (cache misses), even though
both sums are 16000000. The numbers spoken are the measured ones. Run `python3 video10.7.py --help`.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 124
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-07"
FINAL = (CODE / "grid.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(c0, r0, c2, r2, cch, rch) = cpp.session({"grid.cpp": FINAL}, [
    "g++ -std=c++20 -O0 grid.cpp -o g0", "./g0", "g++ -std=c++20 -O2 grid.cpp -o g2", "./g2",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)


def ms(r, which):
    return int(re.search(which + r" 16000000 (\d+)ms", r.output).group(1))


row0, col0, row2, col2 = ms(r0, "rows"), ms(r0, "cols"), ms(r2, "rows"), ms(r2, "cols")
assert row0 > row2 and col2 > 2 * row2 and col0 > row0, (row0, col0, row2, col2)
assert rch.output == "16000000 1\n"
D = "零一二三四五六七八九"


def zh(n):
    if n < 10:
        return D[n]
    if n < 100:
        return ("" if n // 10 == 1 else D[n // 10]) + "十" + (D[n % 10] if n % 10 else "")
    h = D[n // 100] + "百"
    rest = n % 100
    if rest == 0:
        return h
    return h + ("零" + D[rest] if rest < 10 else (D[rest // 10] + "十" + (D[rest % 10] if rest % 10 else "")))


SAY = {"-O0": "O 零", "-O2": "O 二", "cache": "cache", "byRow": "by row", "byCol": "by col", "steady_clock": "steady clock",
       "grid[r * n + c]": "grid r 乘 n 加 c", "ms": "毫秒", "vector": "vector"}

s = Stage({"grid.cpp": FINAL}, title="效能入門", code_px=21, split=0.5)

scenes = [
    Scene("intro",
          "歡迎返嚟！同一個程式，點樣令佢快幾倍？今集講兩樣最簡單又最有效嘅嘢：開編譯器優化，同埋用 cache 友善嘅次序去行記憶體。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "-O0 vs -O2 · 行定列")),
    Scene("goal",
          "今集會講：[[b1]]點樣計時；[[b2]]O 零同 O 二；[[b3]]按行行同按列行；[[b4]]cache 點解咁重要。",
          BulletCard("今集學識", [("steady_clock 計時", "b1"), ("-O0 vs -O2", "b2"), ("按行 vs 按列", "b3"), ("cache", "b4")])),
    Scene("code",
          "[[grid]]一個四千乘四千嘅格，存喺一個 vector 入面，第 r 行第 c 格就係 r 乘 n 加 c。[[row]]第一次按行行：外面行，入面列；[[col]]第二次按列行：外面列，入面行。"
          "[[time]]兩次都用 steady_clock 計時。",
          s.scene(Open("grid.cpp", at="grid"), Mark((7, 8), at="grid"), Mark((10, 15), at="row"), Mark((17, 22), at="col"), Mark((24, 27), at="time"))),
    Scene("o0",
          f"[[cc]]先用 O 零，即係唔優化。運行：[[o]]按行 {zh(row0)} 毫秒，按列 {zh(col0)} 毫秒。兩個答案一樣，但係按列慢好多。",
          s.scene(Mark(None), Run(c0, at="cc"), Run(r0, at="o"))),
    Scene("o2",
          f"[[cc]]再用 O 二，叫編譯器優化。運行：[[o]]按行只係 {zh(row2)} 毫秒，按列 {zh(col2)} 毫秒。開咗優化，全部快咗；但係按列仲係慢幾倍。",
          s.scene(Run(c2, at="cc"), Run(r2, at="o"))),
    Scene("cache",
          "點解？[[cache]]CPU 由記憶體攞嘢，唔係一格一格咁攞，而係一次攞一段，放入好快嘅 cache。[[row]]按行行，下一格就喺隔籬，已經喺 cache 入面；"
          "[[col]]按列行，每次都跳四千格，cache 冇用，次次都要去慢嘅記憶體攞。",
          BoxesCard("記憶體入面嘅次序", [
              BoxRow([Box("", "[0][0]", "", at="cache", color=GREEN, w=150), Box("", "[0][1]", "", at="row", color=GREEN, w=150),
                      Box("", "[0][2]", "", at="row", color=GREEN, w=150), Box("", "…", "", w=100), Box("", "[1][0]", "", at="col", color=RED, w=150)], gap=8),
          ], notes=[("按行：下一格就喺隔籬（cache 命中）", "row"), ("按列：每次跳 4000 格（cache miss）", "col")], top=CONTENT_TOP + 40, row_h=250, box_h=110, size=36)),
    Scene("tips",
          "效能貼士：[[m]]先量度，再優化，唔好靠估；[[o]]正式版本用 O 二；[[c]]資料連續放，按記憶體次序行，vector 通常最快；[[a]]揀啱演算法，影響仲大，第十二部分會講。",
          BulletCard("效能貼士", [("先量度，唔好估", "m"), ("正式版本：-O2", "o"), ("連續資料、按次序行", "c"), ("演算法最重要（Part 12）", "a")])),
    Scene("recap",
          "總結：[[r1]]用 steady_clock 量度時間；[[r2]]O 二令程式快好多；[[r3]]按記憶體次序行，善用 cache；[[r4]]改之前先量度。",
          BulletCard("今集重點", [("steady_clock 計時", "r1"), ("-O2", "r2"), ("cache 友善：按行", "r3"), ("先量度", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]改用 vector 嘅 vector 做格，用 range-for 逐行加，量度吓要幾耐。[[next]]下一集：C++20 modules 簡介。多謝收睇，下次見！",
          EndCard("用 std::vector<std::vector<int>> 做 4000 × 4000 格，range-for 逐行加總，用 steady_clock 計時。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

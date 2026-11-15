#!/usr/bin/env python3
"""Video 101 (syllabus 8.14): 二分搜尋

std::binary_search for 45 in the unsorted {72, 45, 91, 58} really prints 0 although 45 is there.
On the sorted {45, 58, 72, 72, 72, 91}: 72 is found, 60 is not (1 0); lower_bound / upper_bound
for 72 are positions 2 and 5, so 3 copies; inserting 60 at lower_bound(60) keeps it sorted
(45 58 60 72 72 72 91). Run `python3 video101.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 101
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-14"
FINAL = (CODE / "bsearch.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = ("#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> m{72, 45, 91, 58};\n"
       "    bool has45 = std::binary_search(m.begin(), m.end(), 45);\n    std::cout << has45 << '\\n';\n}\n")
INS = "    auto pos" + FINAL.split("    auto pos")[1].rsplit("}\n", 1)[0]
V2 = FINAL.replace(INS, "")
BOUNDS = "    auto lo" + V2.split("    auto lo")[1].rsplit("}\n", 1)[0]
CC = "g++ -std=c++20 -Wall -Wextra bsearch.cpp -o bs"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"bsearch.cpp": BAD}, [
    CC, "./bs", "clear", Write("bsearch.cpp", V2), CC, "./bs", "clear", Write("bsearch.cpp", FINAL), CC, "./bs",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "0\n" and r2.output == "1 0\n2 5 3\n" and r3.output == "1 0\n2 5 3\n45 58 60 72 72 72 91 \n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "4\n"

SAY = {"std::binary_search": "S T D binary search", "binary_search": "binary search", "std::lower_bound": "S T D lower bound",
       "lower_bound": "lower bound", "std::upper_bound": "S T D upper bound", "upper_bound": "upper bound", "O(log n)": "O log n",
       "O(n)": "O n", "insert": "insert", "has45": "has 四十五", "has72": "has 七十二", "has60": "has 六十", "hi - lo": "hi 減 lo"}

s = Stage({"bsearch.cpp": BAD}, title="二分搜尋", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！喺一百萬個數入面搵一個，逐個睇要一百萬步；如果已經排好序，二十步就搵到。今集學二分搜尋：binary_search、lower_bound 同 upper_bound。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "排好序 · 每次減半 · O(log n)")),
    Scene("goal",
          "今集會講：[[b1]]二分搜尋點運作；[[b2]]一定要排好序；[[b3]]binary_search；[[b4]]lower_bound 同 upper_bound。",
          BulletCard("今集學識", [("每次減半", "b1"), ("前提：排好序", "b2"), ("binary_search：有冇", "b3"), ("lower_bound、upper_bound：喺邊", "b4")])),
    Scene("idea",
          "[[mid]]睇中間嗰個：[[left]]要搵嘅細過佢，就淨係搵左半；[[right]]大過佢，就搵右半。[[log]]每次唔要一半，一百萬個數，大約二十步就搞掂。",
          BoxesCard("搵 72：每次減半", [
              BoxRow([Box("", "45", "", at="mid", w=120), Box("", "58", "", at="mid", w=120), Box("", "72", "中間", at="mid", color=AMBER, w=120),
                      Box("", "72", "", at="mid", w=120), Box("", "72", "", at="mid", w=120), Box("", "91", "", at="mid", w=120)], gap=10),
          ], notes=[("細過中間 → 搵左半", "left"), ("大過中間 → 搵右半", "right"), ("10⁶ 個 ≈ 20 步：O(log n)", "log")],
              top=CONTENT_TOP + 40, row_h=250, box_h=110, size=44)),
    Scene("unsorted",
          "[[open]]但係有個前提。呢個 vector 冇排序，[[search]]用 binary_search 搵四十五。[[cc]]編譯運行：[[o]]零，即係話搵唔到！但係四十五明明喺度。"
          "[[why]]因為佢假設咗有排序，一開始就揀錯咗邊。",
          s.scene(Open("bsearch.cpp", at="open"), Mark(6, at="open"), Mark(7, at="search"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note("冇排序：答案唔可信", at="why", where="editor"))),
    Scene("sorted",
          "[[type]]改用一個排好序嘅 vector，七十二有三個。[[has]]binary_search 只答有冇：七十二有，六十冇。[[lb]]lower_bound 係第一個大過或等於七十二嘅位置，"
          "[[ub]]upper_bound 係第一個大過七十二嘅位置；兩個相減，就係七十二有幾多個。[[cc]]運行：[[o]]一零；二、五、三：七十二由位置二開始，有三個。",
          s.scene(Note(None), Run(clr, at="type"), Replace("bsearch.cpp", BAD.split("int main() {\n")[1].rstrip("\n"), V2.split("int main() {\n")[1].rstrip("\n"),
                                                              at="type", rate=80),
                  Expect("bsearch.cpp", V2), Mark((7, 9), at="has"), Mark(10, at="lb"), Mark(11, at="ub"), Mark(None, at="cc"),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("bounds",
          "[[lo]]lower_bound 指住第一個七十二，[[hi]]upper_bound 指住七十二之後嗰個九十一。[[range]]即係範圍 lo 到 hi，正正係全部七十二。",
          BoxesCard("lower_bound / upper_bound（72）", [
              BoxRow([Box("", "45", "0", w=120), Box("", "58", "1", w=120), Box("", "72", "2 ← lo", at="lo", color=GREEN, w=140),
                      Box("", "72", "3", at="range", color=GREEN, w=120), Box("", "72", "4", at="range", color=GREEN, w=120),
                      Box("", "91", "5 ← hi", at="hi", color=AMBER, w=140)], gap=10),
          ], notes=[("hi − lo = 3 個 72", "range")], top=CONTENT_TOP + 60, row_h=250, box_h=110, size=44)),
    Scene("insert",
          "[[type]]lower_bound 仲有一個用途：搵六十應該插喺邊，然後 insert，vector 就保持排好序。[[cc]]運行，[[o]]六十插咗喺五十八同七十二中間。",
          s.scene(Run(clr2, at="type"), Type("bsearch.cpp", INS, before="}", last=True, at="type", rate=60), Expect("bsearch.cpp", FINAL),
                  Mark((14, 15), at="type"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]二分搜尋每次減半，係 O log n；[[r2]]一定要先排好序；[[r3]]binary_search 答有冇；[[r4]]lower_bound 同 upper_bound 答喺邊，相減就係有幾多個。",
          BulletCard("今集重點", [("每次減半：O(log n)", "r1"), ("一定要排好序", "r2"), ("binary_search：有冇", "r3"), ("lower / upper_bound：範圍", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用兩個 lower_bound，數排好序嘅分數入面，有幾多個喺六十至八十之間，包六十，唔包八十。[[next]]下一集：C++20 嘅 ranges 同 views。多謝收睇，下次見！",
          EndCard("{45, 58, 62, 72, 72, 79, 91}：lower_bound(60) 同 lower_bound(80) 相減，數 [60, 80) 有幾多個（答案 4）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

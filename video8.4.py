#!/usr/bin/env python3
"""Video 91 (syllabus 8.4): pair、tuple、structured bindings

minMax returns a std::pair: p.first / p.second really print 58 91; auto [lo, hi] gives the same
with names. top() returns a std::tuple of three; binding only two names is a real "only 2 names
provided for structured binding" error; three names print Amy 91 A. Bindings in a range-for
over pairs print Ben=64 Cat=80. Run `python3 video91.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 91
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-04"
FINAL = (CODE / "bind.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
TOP = "std::tuple<std::string, int, char> top() {\n    return {\"Amy\", 91, 'A'};\n}\n\n"
TUP = "    auto [name, mark, grade] = top();\n    std::cout << name << ' ' << mark << ' ' << grade << '\\n';\n"
TUP_BAD = "    auto [name, mark] = top();\n    std::cout << name << ' ' << mark << '\\n';\n"
LIST = "    std::vector<std::pair" + FINAL.split("    std::vector<std::pair")[1].rsplit("}\n", 1)[0]
BIND = "    auto [lo, hi] = minMax(marks);\n    std::cout << lo << ' ' << hi << '\\n';\n"
INCS = "#include <string>\n#include <tuple>\n"
V4 = FINAL.replace(LIST, "")
BAD = V4.replace(TUP, TUP_BAD)
V2 = V4.replace(TOP, "").replace(TUP, "").replace(INCS, "")
V1 = V2.replace(BIND, "")
CC = "g++ -std=c++20 -Wall -Wextra bind.cpp -o bind"

(c1, r1, c2, r2, clr, c3, clr2, c4, r4, cch, rch) = cpp.session({"bind.cpp": V1}, [
    CC, "./bind", Write("bind.cpp", V2), CC, "./bind", "clear", Write("bind.cpp", BAD), CC, "clear", Write("bind.cpp", FINAL), CC, "./bind",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "58 91\n" and r2.output == "58 91\n58 91\n" and r4.output == "58 91\n58 91\nAmy 91 A\nBen=64 Cat=80 \n", r4.output
assert "only 2 names provided for structured binding" in cpp.visible(c3.output) and "decomposes into 3 elements" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "3 2\n"

SAY = {"std::pair": "S T D pair", "std::tuple": "S T D tuple", "std::pair<int, int>": "pair int int", "p.first": "p 點 first",
       "p.second": "p 點 second", "auto [lo, hi]": "auto 中括號 lo hi", "structured bindings": "structured bindings",
       "structured binding": "structured binding", "minMax": "min max", "std::get<0>": "S T D get 零", "top()": "top", "lo": "lo", "hi": "hi",
       "Amy": "Amy", "Ben": "Ben", "Cat": "Cat", "divide": "divide"}

s = Stage({"bind.cpp": V1}, title="pair、tuple、structured bindings", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！一個函數想回傳兩個值，例如最細同最大，點算？今集學 std::pair、std::tuple，同埋 C++17 嘅 structured bindings，一次過拆開佢哋。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "pair · tuple · auto [a, b]")),
    Scene("goal",
          "今集會講：[[b1]]pair 裝兩個值；[[b2]]structured bindings 拆開；[[b3]]tuple 裝幾個都得；[[b4]]喺 range-for 入面拆。",
          BulletCard("今集學識", [("std::pair", "b1"), ("auto [lo, hi] = …", "b2"), ("std::tuple", "b3"), ("for (auto& [n, m] : list)", "b4")])),
    Scene("pair",
          "[[fn]]minMax 行一次，搵最細同最大，[[ret]]用 pair int int 一齊回傳，大括號入面就係兩個值。[[use]]用嘅時候，first 係第一個，second 係第二個。"
          "[[cc]]編譯運行，[[o]]五十八同九十一：最細同最大，一個函數一次過回傳。",
          s.scene(Open("bind.cpp", at="fn"), Mark(6, at="fn"), Mark(13, at="ret"), Mark((18, 19), at="use"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("bind",
          "first、second 唔知講緊乜。[[type]]用 structured bindings：auto 中括號 lo、hi，等於 minMax，[[name]]pair 就即刻拆開做兩個有名嘅變數。"
          "[[cc]]運行，[[o]]一樣係五十八同九十一，但係易讀好多。",
          s.scene(Mark(None), Type("bind.cpp", BIND, before="}", last=True, at="type", rate=40), Expect("bind.cpp", V2), Mark(20, at="name"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("tuple",
          "三個值就用 tuple。[[type]]top 回傳名、分數同等級。[[bad]]拆嘅時候，唔小心只寫咗兩個名。[[cc]]編譯：[[err]]錯誤：tuple 有三個元素，只提供咗兩個名。名嘅數量一定要啱。",
          s.scene(Run(clr, at="type"), Replace("bind.cpp", "#include <iostream>\n", "#include <iostream>\n" + INCS, at="type", rate=40),
                  Type("bind.cpp", TOP, before="int main", rate=40), Type("bind.cpp", TUP_BAD, before="}", last=True, at="bad", rate=40),
                  Expect("bind.cpp", BAD), Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("fix",
          "[[type]]補返第三個名 grade。[[loop]]再試吓喺 range-for 入面拆：一個 vector 裝住幾個名同分數嘅 pair，每個 pair 拆做 n 同 m。"
          "[[cc]]編譯運行，[[o]]Amy 九十一 A；Ben 等於六十四，Cat 等於八十。",
          s.scene(Run(clr2, at="type"), Replace("bind.cpp", TUP_BAD, TUP, at="type", rate=30),
                  Type("bind.cpp", LIST, before="}", last=True, at="loop", rate=60), Expect("bind.cpp", FINAL), Mark(32, at="loop"),
                  Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("compare",
          "[[p]]pair 固定兩個，用 first、second；[[t]]tuple 幾多個都得，用 std::get 加位置；[[b]]兩樣都可以用 structured bindings 拆開，最易讀。",
          TableCard("點樣攞值？", ["", "寫法"], [
              (["pair", "p.first、p.second"], "p"),
              (["tuple", "std::get<0>(t)、std::get<1>(t)"], "t"),
              (["structured bindings", "auto [a, b, c] = …;"], "b", GREEN),
          ], widths=[1.1, 1.8], code_cols=(1,), size=38)),
    Scene("recap",
          "總結：[[r1]]pair 裝兩個值，tuple 裝幾個都得；[[r2]]用嚟一次過回傳幾個值；[[r3]]auto 中括號拆開，名嘅數量要啱；[[r4]]range-for 都可以拆。",
          BulletCard("今集重點", [("pair、tuple", "r1"), ("一次回傳幾個值", "r2"), ("auto [a, b] = …：數量要啱", "r3"),
                                ("for (const auto& [n, m] : list)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 divide，回傳商同餘數，用 structured bindings 接住。[[next]]下一集：map。多謝收睇，下次見！",
          EndCard("寫 std::pair<int, int> divide(int a, int b)，回傳 {商, 餘數}；auto [q, r] = divide(17, 5);",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

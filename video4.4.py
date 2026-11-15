#!/usr/bin/env python3
"""Video 45 (syllabus 4.4): 二維 vector

A cinema seating plan as a vector of vectors (3 rows of 4 seats), printed with nested
range-for loops; booking with seats[c][r] instead of seats[r][c] really puts the X in the wrong
seat; the fix. Run `python3 video4.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 45
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-04"
FINAL = (CODE / "seats.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
MAKE = ("    const int rows = 3;\n    const int cols = 4;\n    std::vector<char> row(cols, '.');\n"
        "    std::vector<std::vector<char>> seats(rows, row);\n")
BOOK = ("    int r{};\n    int c{};\n    std::cout << \"Row and seat: \";\n    std::cin >> r >> c;\n"
        "    seats[r][c] = 'X';\n")
PRINT = ("    for (const auto& line : seats) {\n        for (char s : line) {\n            std::cout << s << ' ';\n"
         "        }\n        std::cout << '\\n';\n    }\n")
SKEL = "#include <iostream>\n#include <vector>\n\nint main() {\n}\n"
assert SKEL.replace("}\n", MAKE + BOOK + PRINT + "}\n") == FINAL
V1 = SKEL.replace("}\n", MAKE + PRINT + "}\n")
BUG = FINAL.replace("seats[r][c]", "seats[c][r]")
CC = "g++ -std=c++20 -Wall -Wextra seats.cpp -o seats"

(c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"seats.cpp": V1}, [
    CC, "./seats", Write("seats.cpp", BUG), CC, Input("./seats", ["0 2"]),
    Write("seats.cpp", FINAL), "clear", CC, Input("./seats", ["0 2"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == ". . . . \n" * 3
assert r2.output.endswith(". . . . \n. . . . \nX . . . \n"), r2.output
assert r3.output.endswith(". . X . \n. . . . \n. . . . \n"), r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.split("\n")[0] == "X . . . . "

SAY = {"seats[r][c]": "seats r c", "seats[c][r]": "seats c r", "seats[0][2]": "seats 零 二", "seats[0]": "seats 零",
       "std::vector<std::vector<char>>": "vector 入面裝 vector", "vector": "vector"}

s = Stage({"seats.cpp": SKEL}, title="二維 vector：戲院座位", code_px=22)

grid = BoxesCard("seats：3 行 × 4 個座位", [
    BoxRow([Box("", ".", f"[{r}][{c}]", at=("rows", 0.3 * r), w=150, color=AMBER if (r, c) == (0, 2) else BLUE)
            for c in range(4)], label=f"seats[{r}]", gap=16, at=("rows", 0.3 * r)) for r in range(3)
], top=CONTENT_TOP - 30, row_h=150, box_h=80, size=44,
    notes=[("seats[0][2]：第一行、第三個位（先行，後列）", "cell")])

scenes = [
    Scene("intro",
          "歡迎返嚟！戲院座位、棋盤、試算表：好多資料都係一格一格嘅表。今集學二維 vector：vector 入面，再裝 vector。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "vector 入面裝 vector")),
    Scene("goal",
          "今集會講：[[b1]]建立一個二維 vector；[[b2]]用兩個中括號，先行，後列；[[b3]]用巢狀迴圈印出成個表。",
          BulletCard("今集學識", [("建立二維 vector", "b1"), ("[行][列]：先行後列", "b2"), ("巢狀迴圈印出", "b3")])),
    Scene("create",
          "[[size]]戲院有三行，每行四個座位。[[row]]先整一行：vector<char>，括號入面係四同一個點，即係四個點。"
          "[[grid]]再整一個 vector，入面裝三行：呢個就係二維 vector。",
          s.scene(Open("seats.cpp", mode="instant"), Type("seats.cpp", "".join(MAKE.splitlines(True)[:2]), before="}", last=True, at="size", rate=24),
                  Type("seats.cpp", MAKE.splitlines(True)[2], before="}", last=True, at="row", rate=24),
                  Type("seats.cpp", MAKE.splitlines(True)[3], before="}", last=True, at="grid", rate=26))),
    Scene("grid",
          "[[rows]]seats[0] 係第一行，seats[1] 係第二行。[[cell]]再加一個中括號，就係嗰行入面嘅座位：seats[0][2]，係第一行嘅第三個位。"
          "[[rule]]記住：先行，後列，兩個都由零開始。",
          grid),
    Scene("print",
          "[[loop]]印出成個表：外層迴圈逐行攞，[[inner]]內層迴圈逐個座位印，[[nl]]每行印完就換行。[[cc]]編譯運行，[[o]]三行，每行四個空位，用點代表。外層行咗三次，內層每次就行四次。",
          s.scene(Type("seats.cpp", PRINT.splitlines(True)[0], before="}", last=True, at="loop", rate=26),
                  Type("seats.cpp", "".join(PRINT.splitlines(True)[1:4]), before="}", last=True, at="inner", rate=30),
                  Type("seats.cpp", "".join(PRINT.splitlines(True)[4:]), before="}", last=True, at="nl", rate=30),
                  Expect("seats.cpp", V1), Run(c1, at="cc"), Run(r1))),
    Scene("book",
          "而家劃位。[[read]]讀入行同座位號，[[set]]將嗰格改做 X。寫嘅時候，好容易寫咗 seats[c][r]。[[cc]]編譯運行，"
          "[[t]]劃第零行、第二個位，[[o]]X 竟然出咗喺第三行嘅第一個位！",
          s.scene(Type("seats.cpp", "".join(BOOK.splitlines(True)[:4]), before="    for (const auto& line", at="read", rate=30),
                  Type("seats.cpp", BOOK.splitlines(True)[4].replace("[r][c]", "[c][r]"), before="    for (const auto& line", at="set"),
                  Expect("seats.cpp", BUG), Run(c2, at="cc", recall=True), Run(r2, keys=("t",)),
                  Note("想要 [0][2]\n出咗 [2][0]！", at="o", where="editor"))),
    Scene("fix",
          "[[why]]因為中括號嘅次序調轉咗：第一個中括號係行，第二個先係座位。[[fix]]改返 seats[r][c]。[[cc]]再運行，"
          "[[t]]同樣劃第零行第二個位，[[o]]今次啱晒。記住：先行，後座位。",
          s.scene(Note(None), Mark(13, at="why"), Replace("seats.cpp", "seats[c][r]", "seats[r][c]", at="fix"), Expect("seats.cpp", FINAL),
                  Mark(None, at="cc"), Run(clr, at="cc"), Run(c3, recall=True), Run(r3, recall=True, keys=("t",)))),
    Scene("recap",
          "總結：[[r1]]二維 vector 就係 vector 入面裝 vector；[[r2]]第一個中括號揀行，第二個揀列，都由零開始；"
          "[[r3]]用巢狀迴圈逐行逐格處理。",
          BulletCard("今集重點", [("vector 入面裝 vector", "r1"), ("seats[行][列]，由 0 開始", "r2"), ("巢狀迴圈逐行逐格", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個五乘五嘅格仔，喺對角線放 X，其他係點。[[next]]下一集，我哋睇吓 C 語言留落嚟嘅陣列。多謝收睇，下次見！",
          EndCard("整一個 5 × 5 嘅格仔，喺對角線（[0][0]、[1][1] …）放 X，其他係點。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

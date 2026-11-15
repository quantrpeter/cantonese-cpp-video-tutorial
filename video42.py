#!/usr/bin/env python3
"""Video 42 (syllabus 4.1): vector 入門

Class marks in a std::vector<int>: push_back, size(), [] (boxes with indexes); a for loop with
`int i < marks.size()` is a real -Wsign-compare warning, std::size_t fixes it; finally the marks
are read until -1 and the vector grows by itself. Run `python3 video42.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 42
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-01"
FINAL = (CODE / "marks.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
READ = ("    int m{};\n    std::cout << \"Marks (-1 to end): \";\n    while (std::cin >> m && m >= 0) {\n"
        "        marks.push_back(m);\n    }\n")
PUSH = "    marks.push_back(72);\n    marks.push_back(85);\n    marks.push_back(64);\n"
LOOP = ("    int total{0};\n    for (std::size_t i = 0; i < marks.size(); i++) {\n        total += marks[i];\n    }\n"
        "    double avg = static_cast<double>(total) / marks.size();\n    std::cout << \"Average: \" << avg << '\\n';\n")
S3 = FINAL.replace(READ, PUSH)
S2 = S3.replace("std::size_t i", "int i")
S1 = S3.replace(LOOP, "")
SKEL = "#include <iostream>\n#include <vector>\n\nint main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra marks.cpp -o marks"

(c1, r1, c2, r2, c3, clr, c4, r4, cch, rch) = cpp.session({"marks.cpp": S1}, [
    CC, "./marks", Write("marks.cpp", S2), CC, "./marks", Write("marks.cpp", S3), CC,
    Write("marks.cpp", FINAL), "clear", CC, Input("./marks", ["72 85 64 91 58 -1"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["72 85 64 91 58 -1"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Count: 3\nFirst: 72\n" and r2.output.endswith("Average: 73.6667\n")
assert "comparison of integer expressions of different signedness" in cpp.visible(c2.output), c2.output
assert c3.output.strip() == "" and r4.output.endswith("Count: 5\nFirst: 72\nAverage: 74\n"), r4.output
assert c1.code == c4.code == cch.code == 0 and rch.output.endswith("Best: 91\n")

SAY = {"std::vector<int>": "S T D vector int", "vector": "vector", "push_back": "push back", "size()": "size",
       "marks[0]": "marks 零", "std::size_t": "S T D size T", "size_t": "size T"}

s = Stage({"marks.cpp": SKEL}, title="vector 入門", code_px=22)

scenes = [
    Scene("intro",
          "歡迎嚟到第四章！一班有三十個學生，難道要寫三十個變數？今集學 vector：一個可以裝好多個值、仲識自己變大嘅清單。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::vector · push_back · size · []")),
    Scene("goal",
          "今集會講：[[b1]]建立一個 vector；[[b2]]用 push_back 加入資料；[[b3]]size 同中括號；[[b4]]用迴圈逐個處理。",
          BulletCard("今集學識", [("建立 std::vector", "b1"), ("push_back 加入", "b2"), ("size() 同 []", "b3"), ("用迴圈逐個處理", "b4")])),
    Scene("why",
          "[[bad]]如果每個分數一個變數，三十個學生就要三十個名，迴圈都用唔到。[[good]]vector 用一個名，就裝晒所有分數，要幾多就裝幾多。",
          TileCard("點解要 vector？", [
              Tile("😵", "一個分數一個變數", "mark1、mark2 … mark30\n寫唔完，亦都唔可以用迴圈", "bad", RED),
              Tile("📦", "一個 vector", "std::vector<int> marks\n一個名，裝晒，仲會變大", "good", GREEN),
          ], cols=2, height=380)),
    Scene("create",
          "[[inc]]用 vector 要 include vector。[[decl]]std::vector<int> marks：角括號入面係裝咩型別，今次係 int；一開始係空嘅。"
          "[[push]]push_back 將一個值加喺最尾，加三個分數。[[out]]size 係有幾多個，中括號零，就係第一個。記住，第一個嘅位置係零，唔係一。",
          s.scene(Open("marks.cpp", mode="instant"), Type("marks.cpp", "    std::vector<int> marks;\n", before="}", last=True, at="decl"),
                  Type("marks.cpp", PUSH, before="}", last=True, at="push", rate=26),
                  Type("marks.cpp", "    std::cout << \"Count: \" << marks.size() << '\\n';\n"
                                    "    std::cout << \"First: \" << marks[0] << '\\n';\n", before="}", last=True, at="out", rate=28),
                  Expect("marks.cpp", S1))),
    Scene("run1",
          "[[cc]]編譯運行，[[o]]Count 三，即係有三個分數；First 七十二，就係第一個分數。",
          s.scene(Run(c1, at="cc"), Run(r1))),
    Scene("boxes",
          "用盒嚟睇：[[p1]]每次 push_back，vector 就長多一格：[[p2]]七十二、八十五、[[p3]]六十四。[[size]]size 係格數，即係三；"
          "[[idx]]位置同字串一樣，由零開始，所以 marks[0] 係七十二，最後一格係 marks[2]。",
          BoxesCard("std::vector<int> marks", [BoxRow([
              Box("", "72", "[0]", at="p1", color=AMBER, w=220), Box("", "85", "[1]", at="p2", w=220),
              Box("", "64", "[2]", at="p3", w=220)], gap=0)], top=CONTENT_TOP + 90, box_h=140, size=64,
              notes=[("marks.size() 係 3", "size"), ("marks[0] 係 72；最後一個係 marks[2]", "idx")])),
    Scene("loop",
          "[[loop]]計平均分：用 for 迴圈，i 由零行到 size 減一，逐個加埋。[[avg]]再除 size。[[cc]]編譯，[[warn]]有個警告："
          "比較兩個正負號唔同嘅整數。",
          s.scene(Type("marks.cpp", LOOP.replace("std::size_t i", "int i").split("    double")[0], before="}", last=True, at="loop", rate=30),
                  Type("marks.cpp", "    double" + LOOP.split("    double")[1], before="}", last=True, at="avg", rate=30),
                  Expect("marks.cpp", S2), Run(c2, at="cc", recall=True))),
    Scene("sizet",
          "因為 size 回傳嘅，係一種冇負數嘅整數，叫 std::size_t；同有正負號嘅 int 比較，有機會出事。[[fix]]將 i 改做 std::size_t，"
          "[[cc]]再編譯，[[ok]]警告冇咗。下一集仲有更簡單嘅寫法。",
          s.scene(Replace("marks.cpp", "int i", "std::size_t i", at="fix"), Expect("marks.cpp", S3), Run(c3, at="cc", recall=True))),
    Scene("input",
          "實際上，分數應該由使用者輸入。[[read]]用 while 讀，讀到負一就停，每讀到一個，就 push_back。[[cc]]編譯運行，"
          "[[t]]一次過輸入五個分數，再加負一。[[o]]Count 五，平均七十四：vector 自己變大咗。我哋完全唔使理佢要幾大。",
          s.scene(Run(clr, at="read"), Replace("marks.cpp", PUSH, READ, at="read", rate=30), Expect("marks.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4, keys=("t",), type_rate=12))),
    Scene("recap",
          "總結：[[r1]]std::vector 係一個會變大嘅清單；[[r2]]push_back 加喺最尾；[[r3]]size 係有幾多個，中括號由零開始；"
          "[[r4]]迴圈用 std::size_t，或者下一集嘅 range-based for。",
          BulletCard("今集重點", [("std::vector<int>：會變大嘅清單", "r1"), ("push_back：加喺最尾", "r2"),
                                ("size()；[0] 由 0 開始", "r3"), ("迴圈用 std::size_t", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入幾個分數，用迴圈搵出最高分。[[next]]下一集，我哋學一個更簡單嘅迴圈：range-based for。多謝收睇，下次見！",
          EndCard("讀入幾個分數（-1 結束），用迴圈搵出最高分。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

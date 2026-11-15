#!/usr/bin/env python3
"""Video 14 (syllabus 1.8): 型別轉換

The average of 80 and 95 really prints 87 (int division happens before the value reaches the
double); static_cast<double> fixes it; implicit conversions; char <-> int with ASCII codes
('A' + 1 prints 66, static_cast<char> gives B). Run `python3 video1.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 14
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-08"
AVG = (CODE / "avg.cpp").read_text()
LET = (CODE / "letters.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = AVG.replace("static_cast<double>(a + b) / 2", "(a + b) / 2")
CA = "g++ -std=c++20 -Wall -Wextra avg.cpp -o avg"
CL = "g++ -std=c++20 -Wall -Wextra letters.cpp -o let"

(a1, ra1, a2, ra2, clr, l1, rl1, cch, rch) = cpp.session({"avg.cpp": BAD, "letters.cpp": LET}, [
    CA, "./avg", Write("avg.cpp", AVG), CA, "./avg",
    "clear", CL, "./let",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["q"]),
], refresh=opts.fresh_runs, cols=48)
assert ra1.output.strip() == "Average: 87" and ra2.output.strip() == "Average: 87.5"
assert rl1.output.split() == ["65", "66", "B"], rl1.output
assert all(r.code == 0 for r in (a1, a2, l1, cch)) and rch.output.endswith("Q\n")

SAY = {"static_cast<double>": "static cast double", "static_cast<char>": "static cast char",
       "static_cast<int>": "static cast int", "static_cast": "static cast", "ASCII": "ASCII"}

s = Stage({"avg.cpp": BAD, "letters.cpp": LET}, title="型別轉換")

scenes = [
    Scene("intro",
          "歡迎返嚟！int 同 double 撈埋一齊計，會發生咩事？今集講型別轉換，同埋字元背後嘅數字。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "static_cast · ASCII")),
    Scene("goal",
          "今集會講：[[b1]]C++ 幾時會自動轉換型別；[[b2]]用 static_cast 自己轉換；[[b3]]char 同 int 之間嘅關係。",
          BulletCard("今集學識", [("自動轉換", "b1"), ("static_cast：自己轉換", "b2"), ("char 同 int：ASCII", "b3")])),
    Scene("avg1",
          "[[open]]兩科分數，八十同九十五，計平均分，放入一個 double。[[cc]]編譯運行，[[out]]平均分竟然係八十七，"
          "唔係八十七點五！",
          s.scene(Open("avg.cpp", at="open"), Mark(6, at=("open", 1.0)), Run(a1, at="cc"), Run(ra1),
                  Note("應該係 87.5？", at="out", where="editor"))),
    Scene("why",
          "原因係計數嘅次序。[[sum]]a 加 b，兩個都係 int，得一百七十五；[[div]]再除二，int 除 int，答案係八十七，"
          "小數已經切走咗；[[store]]最後先放入 double，變成八十七點零，已經太遲。",
          FlowCard("(a + b) / 2 點樣計？", [Row("步驟", "由左到右", RED, [
              Node("a + b", "175（int）", "sum"), Node("÷ 2", "87（int）", "div"),
              Node("放入 double", "87.0", "store"),
          ], note="除數嗰陣仲係 int，已經太遲", note_at="store")])),
    Scene("fix",
          "要喺除之前，將個數轉做 double。[[type]]用 static_cast<double>，即係話俾編譯器聽：將呢個值轉做 double。"
          "[[cc]]編譯運行，[[out]]八十七點五，啱晒。",
          s.scene(Note(None), Replace("avg.cpp", "(a + b) / 2", "static_cast<double>(a + b) / 2", at="type"),
                  Expect("avg.cpp", AVG), Run(a2, at="cc", recall=True), Run(ra2))),
    Scene("anatomy",
          "[[sc]]static_cast 係轉換嘅意思；[[ty]]角括號入面，寫你想轉做嘅型別；[[val]]圓括號入面，就係要轉換嘅值。"
          "[[why]]a 加 b 變咗 double，double 除 int，就會用 double 計，保留小數。",
          AnatomyCard("static_cast", [
              Part("static_cast", "轉換", BLUE, "sc"),
              Part("<double>", "轉做乜型別", PURPLE, "ty"),
              Part("(a + b)", "轉邊個值", GREEN, "val"),
              Part(" / 2", "", MUTED, "why"),
          ], size=80, note=("double ÷ int → 用 double 計，保留小數", "why"))),
    Scene("implicit",
          "其實好多時，C++ 會自動幫你轉換，叫做隱式轉換。[[r1]]int 轉 double，冇問題；[[r2]]double 轉 int，小數會切走；"
          "[[r3]]char 轉 int，就變成佢嘅字元編號。[[r4]]自動轉換有時會偷偷失去資料，想清楚啲，就用 static_cast 寫明。",
          TableCard("自動轉換", ["由", "轉做", "例子", "結果"], [
              (["int", "double", "5", "5.0（冇問題）"], "r1", GREEN),
              (["double", "int", "87.5", "87（小數切走）"], "r2", RED),
              (["char", "int", "'A'", "65（字元編號）"], "r3"),
          ], widths=[0.8, 0.8, 0.7, 1.6], code_cols=(0, 1, 2), size=42,
              note=("想清楚啲：用 static_cast 寫明", "r4"))),
    Scene("letters",
          "講開字元：每個字元喺電腦入面，其實係一個數字。[[open]]將字元 A 轉做 int，[[cc]]運行，[[out1]]係六十五。"
          "[[out2]]A 加一，印出六十六，因為 char 加 int，結果係 int。[[out3]]想要返字元，就用 static_cast<char>，得到 B。",
          s.scene(Run(clr), Open("letters.cpp", at="open"), Mark((5, 6), at="open"), Run(l1, at="cc"), Run(rl1),
                  Mark(7, at="out2"), Mark((8, 9), at="out3"))),
    Scene("ascii",
          "呢套編號叫 ASCII。記住幾個：[[A]]大楷 A 係六十五，跟住 B、C 順住加一，[[Z]]Z 係九十；"
          "[[a]]細楷 a 係九十七，即係大楷加三十二；[[zero]]數字零呢個字元，係四十八。",
          TableCard("ASCII 編號", ["字元", "編號"], [
              (["'A'", str(ord("A"))], "A"), (["'B'", str(ord("B"))], ("A", 0.6)), (["'Z'", str(ord("Z"))], "Z"),
              (["'a'", str(ord("a"))], "a"), (["'0'", str(ord("0"))], "zero"),
          ], widths=[1, 1], code_cols=(0, 1), size=44, note=("細楷 = 大楷 + 32", "a"))),
    Scene("recap",
          "總結：[[r1]]int 除 int 會先切走小數，之後先轉 double 已經太遲；[[r2]]用 static_cast 喺計數之前轉換；"
          "[[r3]]自動轉換可能會失去資料；[[r4]]每個 char 都係一個數字，A 係六十五。",
          BulletCard("今集重點", [("int ÷ int 先切走小數，之後先轉太遲", "r1"), ("static_cast<double>(x) 喺計之前轉", "r2"),
                                ("自動轉換可能失去資料", "r3"), ("char 係數字：'A' = 65", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一個細楷字母，印出佢嘅大楷。提示：大細楷相差三十二。"
          "[[next]]下一集，我哋講 const 同 constexpr，用有名嘅常數取代神秘數字。多謝收睇，下次見！",
          EndCard("讀入一個細楷字母，印出佢嘅大楷。提示：大細楷相差 32。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

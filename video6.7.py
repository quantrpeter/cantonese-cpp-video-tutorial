#!/usr/bin/env python3
"""Video 69 (syllabus 6.7): static 成員

Robots count themselves with static members: without inline, `static int created_ = 0;` is a
real "ISO C++ forbids in-class initialization of non-const static member" error; with
static inline the real run shows alive 2, robot c is #3, alive 3, then 2 after c's block;
Robot::alive() is a static member function. Run `python3 video69.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 69
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-07"
FINAL = (CODE / "robot.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = FINAL.replace("static inline int", "static int")
CLASS = "class Robot" + BAD.split("class Robot")[1].split("int main")[0]
SHOWN_BAD = "#include <iostream>\n\n" + CLASS + "int main() {\n}\n"          # what is on screen at the error
MAIN = "int main" + FINAL.split("int main")[1]
CC = "g++ -std=c++20 -Wall -Wextra robot.cpp -o robot"

(c1, clr, c2, r2, cch, rch) = cpp.session({"robot.cpp": SHOWN_BAD}, [
    CC, "clear", Write("robot.cpp", FINAL), CC, "./robot",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "in-class initialization of non-const static member" in cpp.visible(c1.output), c1.output[:300]
assert r2.output == "alive: 2\nc is #3\nalive: 3\nalive: 2\n" and c2.code == cch.code == 0 and rch.output.strip() == "3"

SAY = {"static": "static", "inline": "inline", "static inline": "static inline", "Robot::alive()": "Robot 兩個冒號 alive",
       "created_": "created 底線", "alive_": "alive 底線", "id_": "id 底線", "Robot": "Robot", "c.id()": "c 點 id"}

s = Stage({"robot.cpp": "#include <iostream>\n\nint main() {\n}\n"}, title="static 成員", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！如果想知一共整咗幾多部 Robot，呢個數應該放喺邊？放喺每部 Robot 入面唔啱，今集學 static 成員：成個 class 共用一份。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "static · 成個 class 共用")),
    Scene("goal",
          "今集會講：[[b1]]static 資料成員；[[b2]]static 成員函數；[[b3]]用 class 名加兩個冒號呼叫。",
          BulletCard("今集學識", [("static 資料成員", "b1"), ("static 成員函數", "b2"), ("Robot::alive()", "b3")])),
    Scene("class",
          "[[ctor]]每次建構，created 底線加一，用嚟做呢部 Robot 嘅編號，alive 底線亦加一；[[dtor]]解構嗰陣，alive 減一。"
          "[[st]]created 同 alive 前面加 static：唔係每部 Robot 一份，而係成個 class 共用一份。[[cc]]編譯：[[err]]出錯！兩個 static 嘅行都有問題。我哋睇吓點解。",
          s.scene(Open("robot.cpp", mode="instant"), Type("robot.cpp", CLASS, before="int main", at="ctor", rate=70),
                  Mark((5, 7), at="ctor"), Mark((8, 10), at="dtor"), Mark((20, 21), at="st"), Mark(None, at="cc"), Expect("robot.cpp", SHOWN_BAD), Run(c1, at="cc"))),
    Scene("inline",
          "[[why]]普通嘅 static 資料成員，唔可以喺 class 入面直接設初始值。[[fix]]C++17 開始，加 inline 就得。",
          s.scene(Note("static 資料：要加 inline\n先可以喺 class 入面初始化", at="why", where="editor"),
                  Note(None, at="fix"), Replace("robot.cpp", "static int created_", "static inline int created_", at="fix"),
                  Replace("robot.cpp", "static int alive_", "static inline int alive_"))),
    Scene("main",
          "[[ab]]main 整 a 同 b，[[call]]用 Robot 兩個冒號 alive 問有幾多部，唔使經任何一部 Robot。[[block]]大括號入面再整 c，印佢嘅編號。"
          "[[cc]]編譯運行：[[o]]兩部；c 係第三號，三部；c 消失之後，返返兩部。",
          s.scene(Replace("robot.cpp", "int main() {\n}", MAIN.rstrip("\n"), at="ab", rate=60), Expect("robot.cpp", FINAL),
                  Mark(27, at="call"), Mark((28, 32), at="block"), Mark(None, at="cc"), Run(clr, at="cc"), Run(c2, recall=True), Run(r2))),
    Scene("boxes",
          "[[own]]id 底線冇 static：每部 Robot 都有自己一份，一、二、三。[[shared]]created 同 alive 有 static：成個 class 得一份，大家共用。",
          BoxesCard("自己一份 vs 共用一份", [
              BoxRow([Box("a.id_", "1", "", at="own", w=180), Box("b.id_", "2", "", at="own", w=180),
                      Box("c.id_", "3", "", at="own", w=180)], label="每部一份"),
              BoxRow([Box("created_", "3", "static", at="shared", color=PURPLE, w=260),
                      Box("alive_", [("3", "shared"), ("2", ("shared", 1.2))], "static", at="shared", color=PURPLE, w=260)],
                     label="成個 class 一份", at="shared"),
          ], top=CONTENT_TOP + 20, row_h=250, box_h=110, size=48)),
    Scene("func",
          "[[sf]]alive 都係 static 成員函數：唔使物件就可以呼叫，用 class 名加兩個冒號。[[limit]]所以佢入面冇 this，"
          "只可以用 static 嘅成員，用唔到 id 底線。",
          s.scene(Mark((14, 16), at="sf"), Note("static 函數：冇 this\n只可以用 static 成員", at="limit", where="editor"))),
    Scene("recap",
          "總結：[[r1]]static 資料成員，成個 class 共用一份；[[r2]]喺 class 入面初始化，要加 inline；[[r3]]static 成員函數冇 this，"
          "用 class 名加兩個冒號呼叫。",
          BulletCard("今集重點", [("static 資料：共用一份", "r1"), ("static inline int x = 0;", "r2"), ("static 函數：Robot::alive()", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 static 函數 created，回傳總共整過幾多部 Robot，包括已經消失咗嘅。[[next]]下一集：運算子多載。多謝收睇，下次見！",
          EndCard("加 static 函數 created()，回傳總共整過幾多部 Robot（包括已經消失咗嘅）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

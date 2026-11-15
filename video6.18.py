#!/usr/bin/env python3
"""Video 80 (syllabus 6.18): 小項目：圖形面積計算器

Part 6 together: an abstract Shape (virtual destructor, pure virtual area() and name()), Circle
and Rect, readShape() returning std::unique_ptr<Shape>, and a std::vector of them.
push_back(s) without std::move is a real, very long template error whose one useful line is
"shapes.cpp:60:25: required from here" (unique_ptr cannot be copied); with std::move the real session (c 1, r 2 3, x, q) prints unknown shape, circle 3.14159,
rect 6, total 9.14159. Run `python3 video6.18.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 80
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-18"
FINAL = (CODE / "shapes.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = FINAL.split("const double pi")[0]
PI = "const double pi = 3.14159;\n\n"
SHAPE = "class Shape" + FINAL.split("class Shape")[1].split("class Circle")[0]
KINDS = "class Circle" + FINAL.split("class Circle")[1].split("std::unique_ptr<Shape> readShape")[0]
READ = "std::unique_ptr<Shape> readShape" + FINAL.split("std::unique_ptr<Shape> readShape")[1].split("int main")[0]
MAIN = "int main" + FINAL.split("int main")[1]
SKEL = HEAD + "int main() {\n}\n"
BAD = FINAL.replace("shapes.push_back(std::move(s));", "shapes.push_back(s);")
assert HEAD + PI + SHAPE + KINDS + READ + MAIN == FINAL
CC = "g++ -std=c++20 -Wall -Wextra shapes.cpp -o sh"
IN = ["c 1", "r 2 3", "x", "q"]

(c1, clr, c2, r2, cch, rch) = cpp.session({"shapes.cpp": BAD}, [
    CC, "clear", Write("shapes.cpp", FINAL), CC, Input("./sh", IN),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["t 3 4", "c 1", "q"]),
], refresh=opts.fresh_runs, cols=48)
assert "shapes.cpp:60:25:   required from here" in cpp.visible(c1.output) and c1.code != 0, c1.output[:400]
assert r2.output == "c 1\nr 2 3\nx\nunknown shape\nq\ncircle 3.14159\nrect 6\ntotal 9.14159\n", r2.output
assert c2.code == cch.code == 0 and "total 9.14159" in rch.output, rch.output

SAY = {"std::unique_ptr<Shape>": "unique pointer Shape", "unique_ptr": "unique pointer", "std::make_unique": "make unique",
       "std::move": "S T D move", "push_back": "push back", "required from here": "required from here", "shapes.cpp": "shapes 點 c p p", "readShape": "read shape", "nullptr": "null pointer",
       "virtual": "virtual", "override": "override", "= 0": "等如零", "= default": "等如 default", "Shape": "Shape",
       "Circle": "Circle", "Rect": "Rect", "area()": "area", "name()": "name", "s->area()": "s 箭咀 area", "pi": "pi"}

s = Stage({"shapes.cpp": SKEL}, title="小項目：圖形面積計算器", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第六部分最後一集，做一個小項目：圖形面積計算器。輸入一個個圖形，最後印出每個嘅面積同總和。會用到抽象類別、多型、unique_ptr 同 vector。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "多型 · unique_ptr · vector")),
    Scene("plan",
          "計劃：[[b1]]一個抽象嘅 Shape；[[b2]]Circle 同 Rect 實作佢；[[b3]]readShape 讀一行，整一個圖形；[[b4]]main 用 vector 裝住，最後計總和。",
          BulletCard("計劃", [("抽象 Shape：area()、name()", "b1"), ("Circle、Rect", "b2"), ("readShape：輸入 → unique_ptr", "b3"),
                            ("main：vector 裝住，計總和", "b4")])),
    Scene("shape",
          "[[type]]先寫 pi。[[base]]Shape：virtual 解構子，因為會經 Shape 指標刪除；[[pure]]area 同 name 都係純虛擬，每個圖形自己答。",
          s.scene(Open("shapes.cpp", mode="instant"), Type("shapes.cpp", PI + SHAPE, before="int main", at="type", rate=60),
                  Mark(11, at="base"), Mark((12, 13), at="pure"))),
    Scene("kinds",
          "[[type]]Circle 存半徑，面積係 pi r 二次方；[[rect]]Rect 存闊同高，面積係闊乘高。兩個都用 override，寫錯編譯器會捉。name 就回傳自己嘅名，最後印出嚟用。",
          s.scene(Mark(None), Type("shapes.cpp", KINDS, before="int main", at="type", rate=80), Mark((16, 24), at="type"),
                  Mark((26, 35), at="rect"))),
    Scene("read",
          "[[type]]readShape：c 就再讀一個半徑，整一個 Circle；[[r]]r 就讀闊同高，整一個 Rect；[[none]]唔識嘅字母，就回傳 nullptr。"
          "[[own]]回傳 unique_ptr，表示呢個圖形嘅擁有權交俾呼叫嘅人。",
          s.scene(Mark(None), Type("shapes.cpp", READ, before="int main", at="type", rate=70), Mark((38, 42), at="type"),
                  Mark((43, 47), at="r"), Mark(48, at="none"), Mark(37, at="own"))),
    Scene("main",
          "[[type]]main：一個裝 unique_ptr 嘅 vector。[[loop]]不斷讀字母，直到 q；唔識嘅就印 unknown shape。[[push]]識嘅就 push back 入 vector。"
          "[[cc]]編譯：[[err]]一大堆錯誤！vector 嘅錯誤好長，[[here]]搵自己個檔名：shapes.cpp 第六十行，required from here，就係 push back s。",
          s.scene(Mark(None), Replace("shapes.cpp", "int main() {\n}", ("int main" + BAD.split("int main")[1]).rstrip("\n"),
                                      at="type", rate=80),
                  Expect("shapes.cpp", BAD), Mark((54, 59), at="loop"), Mark(60, at="push"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Scroll(at="here", find="required from here"), Mark(60, at="here"))),
    Scene("move",
          "[[why]]因為 unique_ptr 唔可以複製：一個圖形只可以有一個主人。[[fix]]要用 std::move，將 s 搬入 vector。",
          s.scene(Note("unique_ptr：唔可以複製\n只可以搬", at="why", where="editor"), Note(None, at="fix"),
                  Replace("shapes.cpp", "push_back(s)", "push_back(std::move(s))", at="fix"), Expect("shapes.cpp", FINAL), Mark(60, at="fix"))),
    Scene("run",
          "[[cc]]編譯運行。[[in]]輸入：c 一，r 二 三，再亂打一個 x，最後 q。[[o]]x 係 unknown shape；然後圓形三點一四一五九，長方形六，"
          "總和九點一四一五九。[[loop]]印嘅迴圈只係叫 s 箭咀 area，唔理係乜形狀。",
          s.scene(Mark(None), Run(clr, at="cc"), Run(c2, recall=True), Run(r2, at="in"), Mark((63, 66), at="loop"))),
    Scene("parts",
          "呢個小項目用咗第六部分好多嘢：[[a]]抽象類別同純虛擬函數；[[b]]virtual 解構子；[[c]]override；[[d]]unique_ptr 同 std::move。",
          TableCard("用咗乜？", ["概念", "喺邊度"], [
              (["抽象類別：= 0", "Shape::area()、name()"], "a"),
              (["virtual destructor", "virtual ~Shape()"], "b"),
              (["override", "Circle、Rect"], "c"),
              (["unique_ptr + std::move", "readShape、push_back"], "d"),
          ], widths=[1.3, 1.5], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]用抽象類別定規矩；[[r2]]每個圖形自己實作 area 同 name；[[r3]]vector 入面裝 unique_ptr，加入嘅時候要 std::move；"
          "[[r4]]經基底指標呼叫，就係多型。第六部分完成！",
          BulletCard("今集重點", [("抽象 Shape 定規矩", "r1"), ("Circle、Rect 自己實作", "r2"), ("vector<unique_ptr<Shape>> + std::move", "r3"),
                                ("s->area()：多型", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 Triangle，輸入 t 底 高，面積係底乘高除二。[[next]]下一集開始第七部分：函數模板。多謝收睇，下次見！",
          EndCard("加 class Triangle：輸入 t b h，面積 0.5 × b × h；readShape 識得處理 't'。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

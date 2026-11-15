#!/usr/bin/env python3
"""Video 76 (syllabus 6.14): 抽象類別

Shape::area() is pure virtual (= 0): report(c) really prints 3.14159 for a Circle; `Shape s;`
is a real "abstract type 'Shape'" error; a Square that forgets area() is abstract too (real
error naming the pure virtual it lacks); once it has area() the run prints 3.14159 and 4.
Run `python3 video6.14.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 76
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-14"
FINAL = (CODE / "shape.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SQUARE = "class Square" + FINAL.split("class Square")[1].split("void report")[0]
AREA = "    double area() const override {\n        return s_ * s_;\n    }\n"
SQ_NOAREA = SQUARE.replace(AREA, "")
A = FINAL.replace(SQUARE, "").replace("    Square q{2.0};\n", "").replace("    report(q);\n", "")
B = A.replace("    Circle c{1.0};\n", "    Circle c{1.0};\n    Shape s;\n")
C = FINAL.replace(AREA, "")
CC = "g++ -std=c++20 -Wall -Wextra shape.cpp -o shape"

(c1, r1, clr, c2, clr2, c3, clr3, c4, r4, cch, rch) = cpp.session({"shape.cpp": A}, [
    CC, "./shape", "clear", Write("shape.cpp", B), CC, "clear", Write("shape.cpp", C), CC, "clear", Write("shape.cpp", FINAL), CC, "./shape",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "3.14159\n" and r4.output == "3.14159\n4\n", (r1.output, r4.output)
assert "abstract type 'Shape'" in cpp.visible(c2.output), c2.output[:400]
assert "abstract type 'Square'" in cpp.visible(c3.output) and "Shape::area() const" in cpp.visible(c3.output), c3.output[:600]
assert c1.code == c4.code == cch.code == 0 and rch.output == "3.14159\n4\n6\n"

SAY = {"= 0": "等如零", "pure virtual": "pure virtual", "virtual": "virtual", "override": "override", "area()": "area",
       "Shape": "Shape", "Circle": "Circle", "Square": "Square", "report": "report", "abstract": "abstract", "3.14159": "三點一四一五九"}

s = Stage({"shape.cpp": A}, title="抽象類別", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！圓形有面積，正方形有面積，但係一個淨係叫做「形狀」嘅嘢，面積係幾多？答唔到。今集學抽象類別：一個只係講規矩，唔可以直接整出嚟嘅 class。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "= 0 · pure virtual · interface")),
    Scene("goal",
          "今集會講：[[b1]]純虛擬函數，等如零；[[b2]]抽象類別唔可以直接整；[[b3]]子類別一定要實作晒；[[b4]]interface 嘅概念。",
          BulletCard("今集學識", [("純虛擬函數：= 0", "b1"), ("抽象類別：唔可以直接整", "b2"), ("子類別要實作晒", "b3"),
                                ("interface：只講規矩", "b4")])),
    Scene("pure",
          "[[open]]Shape 嘅 area，後面寫等如零，叫做純虛擬函數：Shape 冇自己嘅答案，只係規定每個形狀都要有 area。[[circle]]Circle 就實作佢："
          "π r 二次方。[[cc]]report 收一個 Shape reference，印佢嘅面積。編譯運行，[[o]]半徑一嘅圓形，面積係三點一四一五九。",
          s.scene(Open("shape.cpp", at="open"), Mark(5, at="open"), Mark((11, 13), at="circle"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("noshape",
          "[[type]]如果直接整一個 Shape 呢？[[cc]]編譯：[[err]]錯誤！唔可以宣告一個抽象類型嘅變數。佢連面積都計唔到，所以唔俾整。",
          s.scene(Run(clr, at="type"), Type("shape.cpp", "    Shape s;\n", after="    Circle c{1.0};\n", at="type"), Expect("shape.cpp", B),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("square",
          "[[del]]刪返佢。[[type]]再寫一個 Square，但係唔記得寫 area。[[main]]main 整一個 q。[[cc]]編譯：[[err]]Square 都係抽象類型！"
          "因為 area 仲係純虛擬，g++ 仲話埋你知漏咗邊個。",
          s.scene(Replace("shape.cpp", "    Shape s;\n", "", at="del"), Run(clr2, at="type"),
                  Type("shape.cpp", SQ_NOAREA, before="void report", at="type", rate=60),
                  Type("shape.cpp", "    Square q{2.0};\n", after="    Circle c{1.0};\n", at="main"),
                  Type("shape.cpp", "    report(q);\n", after="    report(c);\n"), Expect("shape.cpp", C),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("fix",
          "[[type]]幫 Square 寫 area：邊長乘邊長。[[cc]]編譯運行：[[o]]三點一四一五九，同埋四。report 只認 Shape，唔理係乜形狀。",
          s.scene(Run(clr3, at="type"), Type("shape.cpp", AREA, after="    Square(double s) : s_{s} {}\n", at="type"), Expect("shape.cpp", FINAL),
                  Mark((22, 24), at="type"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("iface",
          "[[rule]]Shape 好似一份合約：[[must]]想做形狀，就要有 area。[[use]]用嘅人只需要識 Shape，[[add]]第日加三角形，report 一行都唔使改。",
          BoxesCard("Shape：一份合約", [
              BoxRow([Box("Shape", "area() = 0", "抽象：只講規矩", at="rule", color=PURPLE, w=420, key="s")]),
              BoxRow([Box("Circle", "area()", "π r²", at="must", color=BLUE, w=260, key="c"),
                      Box("Square", "area()", "s × s", at="must", color=BLUE, w=260, key="q"),
                      Box("Triangle", "area()", "第日加", at="add", color=GREEN, w=260, key="t")], gap=40),
          ], arrows=[("c", "s", "must", BLUE), ("q", "s", "must", BLUE), ("t", "s", "add", GREEN)],
              notes=[("report(const Shape&)：只認合約", "use")], row_h=300, box_h=110, size=40)),
    Scene("recap",
          "總結：[[r1]]函數後面寫等如零，係純虛擬函數；[[r2]]有純虛擬函數嘅 class 係抽象類別，唔可以直接整；"
          "[[r3]]子類別要實作晒，先可以整；[[r4]]抽象類別就好似一份合約，用嘅人只認合約。",
          BulletCard("今集重點", [("virtual ... = 0", "r1"), ("抽象類別：唔可以整", "r2"), ("子類別：實作晒先整得", "r3"),
                                ("interface：一份合約", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 Triangle，有底同高，面積係底乘高除二；report 一個底三高四嘅三角形。[[next]]下一集：virtual destructor 同 final。"
          "多謝收睇，下次見！",
          EndCard("加 class Triangle（底 b、高 h，面積 0.5 × b × h），report(Triangle{3.0, 4.0}) 應該印 6。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

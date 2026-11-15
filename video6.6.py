#!/usr/bin/env python3
"""Video 68 (syllabus 6.6): this 同 const 成員函數

this points at the object a member function was called on; add() returns *this so calls chain
(add(3).add(4) really gives 7); report(const Counter&) calling a non-const show() is a real
"discards qualifiers" error; marking show() and count() const fixes it.
Run `python3 video6.6.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 68
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-06"
FINAL = (CODE / "counter.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
REPORT = "void report(const Counter& c) {\n    c.show();\n}\n\n"
NOCONST = FINAL.replace("int count() const {", "int count() {").replace("void show() const {", "void show() {")
BAD = NOCONST
S1 = NOCONST.replace(REPORT, "").replace("    report(steps);\n", "    steps.show();\n")
CC = "g++ -std=c++20 -Wall -Wextra counter.cpp -o cnt"

(c1, r1, c2, clr, c3, r3, cch, rch) = cpp.session({"counter.cpp": S1}, [
    CC, "./cnt", Write("counter.cpp", BAD), CC, "clear", Write("counter.cpp", FINAL), CC, "./cnt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Steps: 7\n" and r3.output == "Steps: 7\n"
assert "discards qualifiers" in cpp.visible(c2.output), c2.output[:400]
assert c1.code == c3.code == cch.code == 0 and rch.output.strip() == "2"

SAY = {"this": "this", "*this": "星 this", "const": "const", "add(3).add(4)": "add 三，再 add 四", "Counter": "Counter",
       "report": "report", "show()": "show", "count()": "count", "discards qualifiers": "discards qualifiers"}

s = Stage({"counter.cpp": S1}, title="this 同 const 成員函數", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！成員函數點樣知道，自己係俾邊個物件呼叫？今集講 this，同埋 const 成員函數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "this · *this · const")),
    Scene("goal",
          "今集會講：[[b1]]this 係乜；[[b2]]回傳星號 this，令呼叫可以接落去；[[b3]]const 成員函數；[[b4]]點解 const 物件需要佢哋。",
          BulletCard("今集學識", [("this：自己嘅地址", "b1"), ("return *this：鏈式呼叫", "b2"), ("const 成員函數", "b3"),
                                ("const 物件只可以用 const 函數", "b4")])),
    Scene("this",
          "[[open]]Counter 記住一個數。[[add]]add 將數加上去，跟住回傳星號 this。[[what]]this 係一個指標，指住而家呢個物件，"
          "即係邊個呼叫 add，this 就指住邊個；星號 this，就係物件本身。",
          s.scene(Open("counter.cpp", at="open"), Mark((7, 10), at="add"), Mark(9, at="what"),
                  Note("this：指住呼叫嘅物件\n*this：物件本身", at="what", where="editor"))),
    Scene("chain",
          "[[ret]]因為 add 回傳物件本身嘅 reference，[[chain]]steps.add(3) 嘅結果仍然係 steps，可以再接 add(4)。"
          "[[cc]]編譯運行，[[o]]Steps，七：三加四，兩次都加落同一個物件度。",
          s.scene(Note(None), Mark(None), Mark(25, at="chain"), Run(c1, at="cc"), Run(r1))),
    Scene("report",
          "而家寫一個 report 函數，[[param]]參數用 3.6 學嘅 const reference，唔複製，又唔改。[[call]]入面呼叫 show。"
          "[[cc]]編譯：[[err]]出錯！話傳咗一個 const Counter 做 this，會丟失 const。",
          s.scene(Mark(None), Type("counter.cpp", REPORT, before="int main", at="param", rate=40),
                  Replace("counter.cpp", "    steps.show();\n", "    report(steps);\n", at="call"), Expect("counter.cpp", BAD),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("why",
          "因為 c 係 const，承諾唔會改；[[unknown]]但係 show 冇講明自己唔會改物件，編譯器唔敢俾你用。"
          "[[fix]]喺 show 同 count 嘅括號後面加 const，即係承諾：呢個函數唔會改成員。",
          s.scene(Note("const 物件：\n只可以用 const 成員函數", at="unknown", where="editor"), Note(None, at="fix"),
                  Replace("counter.cpp", "int count() {", "int count() const {", at="fix"),
                  Replace("counter.cpp", "void show() {", "void show() const {"), Expect("counter.cpp", FINAL), Mark((11, 16), at="fix"))),
    Scene("run2",
          "[[cc]]再編譯運行，[[o]]Steps，七。[[guard]]如果喺 const 函數入面試圖改成員，編譯器就會阻止你，所以亦都係一種保護。",
          s.scene(Mark(None), Run(clr, at="cc"), Run(c3, recall=True), Run(r3))),
    Scene("rule",
          "習慣：[[read]]唔改成員嘅函數，好似 show 同 count，一律加 const；[[write]]會改嘅，好似 add，就唔加。",
          TableCard("加唔加 const？", ["成員函數", "改唔改成員", "寫法"], [
              (["show / count", "唔改", "void show() const"], "read", GREEN),
              (["add", "改", "Counter& add(int n)"], "write"),
          ], widths=[1, 0.9, 1.6], code_cols=(0, 2), size=40)),
    Scene("recap",
          "總結：[[r1]]this 係指住而家呢個物件嘅指標；[[r2]]回傳星號 this，可以一路接落去呼叫；[[r3]]const 成員函數承諾唔改成員；"
          "[[r4]]const 物件同 const reference，只可以用 const 成員函數。",
          BulletCard("今集重點", [("this：指住而家嘅物件", "r1"), ("return *this：鏈式呼叫", "r2"), ("() const：承諾唔改", "r3"),
                                ("const 物件：只用 const 函數", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 reset 成員函數，將數歸零，都回傳星號 this，試吓 add(5).reset().add(2)。"
          "[[next]]下一集：static 成員。多謝收睇，下次見！",
          EndCard("加 Counter& reset()：歸零並回傳 *this。試吓連住呼叫 add(5)、reset()、add(2)，答案應該係 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

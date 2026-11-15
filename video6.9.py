#!/usr/bin/env python3
"""Video 71 (syllabus 6.9): 複製

A Buffer that owns a new[] array. The compiler's copy only copies the pointer: changing b really
changes a too (99 99) and the run ends with a real "free(): double free detected" abort. A copy
constructor that copies the data fixes it (42 99); then c = a crashes the same way until a copy
assignment operator exists: the rule of three. Run `python3 video71.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 71
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-09"
FINAL = (CODE / "buffer.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
COPYCTOR = ("    Buffer(const Buffer& other)\n        : size_{other.size_}, data_{new int[other.size_]} {\n"
            "        copyFrom(other);\n    }\n")
ASSIGN = "    Buffer& operator=" + FINAL.split("    Buffer& operator=")[1].split("    ~Buffer")[0]
COPYFROM = "    void copyFrom" + FINAL.split("    void copyFrom")[1].split("    int size_;")[0]
for part in (COPYCTOR, ASSIGN, COPYFROM):
    assert part in FINAL
MAIN_F = "int main() {\n" + FINAL.split("int main() {\n")[1]
MAIN_S = ("int main() {\n    Buffer a{3};\n    a.set(0, 42);\n    Buffer b = a;\n    b.set(0, 99);\n"
          "    std::cout << a.get(0) << ' ' << b.get(0) << '\\n';\n}\n")
SHALLOW = FINAL.replace(COPYCTOR, "").replace(ASSIGN, "").replace(COPYFROM, "").replace(MAIN_F, MAIN_S)
DEEP = FINAL.replace(ASSIGN, "").replace(MAIN_F, MAIN_S)
NOASSIGN = FINAL.replace(ASSIGN, "")
CC = "g++ -std=c++20 -Wall -Wextra buffer.cpp -o buf"
C_LINES = "    Buffer c{1};\n    c = a;\n"

(c1, r1, clr, c2, r2, c3, r3, clr2, c4, r4, cch, rch) = cpp.session({"buffer.cpp": SHALLOW}, [
    CC, "./buf", "clear", Write("buffer.cpp", DEEP), CC, "./buf", Write("buffer.cpp", NOASSIGN), CC, "./buf",
    "clear", Write("buffer.cpp", FINAL), CC, "./buf",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.startswith("99 99\n") and "double free" in r1.output and r1.code != 0, r1.output
crash = r1.output.strip().split("\n")[1]
assert r2.output == "42 99\n" and r2.code == 0
assert r3.output.startswith("42 99 42\n") and "double free" in r3.output and r3.code != 0
assert "-Wdeprecated-copy" in cpp.visible(c3.output)
assert r4.output == "42 99 42\n" and all(r.code == 0 for r in (c1, c2, c3, c4, cch)) and rch.output.strip() == "7 1"

SAY = {"Buffer b = a": "Buffer b 等如 a", "c = a": "c 等如 a", "copy constructor": "copy constructor", "operator=": "operator 等號",
       "data_": "data 底線", "double free": "double free", "copyFrom": "copy from", "rule of three": "rule of three", "this": "this"}

s = Stage({"buffer.cpp": SHALLOW}, title="複製：淺複製 vs 深複製", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！複製一個物件，好似好簡單。但係如果物件入面有指標，就會出大事。今集講複製建構子、複製賦值，同埋 rule of three。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "淺複製 · 深複製 · rule of three")),
    Scene("goal",
          "今集會講：[[b1]]編譯器預設嘅複製做咗乜；[[b2]]淺複製嘅問題；[[b3]]自己寫複製建構子同複製賦值；[[b4]]rule of three。",
          BulletCard("今集學識", [("預設複製：逐個成員複製", "b1"), ("淺複製：兩個物件共用", "b2"), ("複製建構子、operator=", "b3"),
                                ("rule of three", "b4")])),
    Scene("shallow",
          "[[open]]Buffer 用 new 開一排 int，解構子 delete。[[copy]]main 整 a，第一格放四十二，再複製一份做 b，改 b 嘅第一格。"
          "[[cc]]編譯運行：[[o]]a 都變咗九十九？最後仲當機：double free。到底發生咩事？",
          s.scene(Open("buffer.cpp", at="open"), Mark(5, at="open"), Mark((6, 8), at=("open", 1.5)),
                  Mark((22, 25), at="copy"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note(f"a 都變咗 99？\n{crash}", at="o", where="editor"))),
    Scene("why",
          "因為編譯器預設嘅複製，只係逐個成員照抄：[[ptr]]data 底線係一個指標，抄嘅只係地址，[[same]]a 同 b 指住同一排記憶體。"
          "[[twice]]程式完嗰陣，兩個解構子都 delete 同一排，就係 double free。",
          BoxesCard("淺複製：兩個指標，一排記憶體", [
              BoxRow([Box("a.data_", "地址", "int*", at="ptr", color=PURPLE, w=260, key="a"),
                      Box("b.data_", "同一個地址", "int*", at="ptr", color=RED, w=300, key="b")], gap=200),
              BoxRow([Box("", "99", "[0]", at="same", color=AMBER, w=140, key="h0"), Box("", "0", "[1]", at="same", w=140),
                      Box("", "0", "[2]", at="same", w=140)], gap=0, at="same"),
          ], arrows=[("a", "h0", "same", PURPLE), ("b", "h0", "same", RED)], top=CONTENT_TOP + 10, row_h=250, box_h=110, size=46,
              notes=[("兩個解構子都 delete 同一排：double free", "twice")])),
    Scene("ctor",
          "[[type]]解決方法：自己寫複製建構子，參數係 const Buffer reference。[[new]]佢自己 new 一排新嘅記憶體，[[copy]]再逐格抄過去，呢個叫深複製。"
          "[[cc]]編譯運行，[[o]]a 仲係四十二，b 係九十九，冇再當機。",
          s.scene(Note(None), Mark(None), Run(clr, at="type"), Type("buffer.cpp", COPYCTOR, after="new int[n]{}} {}\n", at="type", rate=50),
                  Mark((6, 7), at="new"), Type("buffer.cpp", COPYFROM, after="private:\n", at="copy", rate=60), Expect("buffer.cpp", DEEP),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("assign",
          "仲未完。[[type]]如果係一個已經存在嘅 c，再用等號 c 等於 a 呢？[[cc]]編譯，g++ 已經警告預設嘅等號過時；運行：[[o]]又係 double free！"
          "[[why]]等號用嘅唔係複製建構子，而係複製賦值 operator 等號，佢都係預設淺複製。",
          s.scene(Type("buffer.cpp", C_LINES, after="    b.set(0, 99);\n", at="type"),
                  Replace("buffer.cpp", "<< b.get(0) << '\\n';", "<< b.get(0) << ' ' << c.get(0) << '\\n';"), Expect("buffer.cpp", NOASSIGN),
                  Run(c3, at="cc", recall=True), Run(r3), Note("c = a：用嘅係 operator=\n都係淺複製", at="why", where="editor"))),
    Scene("opassign",
          "[[type]]寫埋 operator 等號：[[self]]先檢查唔係自己抄自己；[[free]]delete 舊嗰排；[[copy]]再 new 新嘅，抄過去；[[ret]]最後回傳星號 this。"
          "[[cc]]運行，[[o]]四十二、九十九、四十二，冇再當機。",
          s.scene(Note(None), Run(clr2, at="type"), Type("buffer.cpp", ASSIGN, after="copyFrom(other);\n    }\n", at="type", rate=60),
                  Expect("buffer.cpp", FINAL), Mark(11, at="self"), Mark(12, at="free"), Mark((13, 15), at="copy"), Mark(17, at="ret"),
                  Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("three",
          "呢個就係 rule of three：[[d]]如果一個 class 要自己寫解構子，[[c]]通常都要自己寫複製建構子，[[a]]同埋複製賦值。三個一齊出現。"
          "[[next]]下兩集會見到，用 vector 呢啲工具，其實可以一個都唔使寫。",
          BulletCard("rule of three", [("解構子 ~Buffer()", "d"), ("複製建構子 Buffer(const Buffer&)", "c"),
                                     ("複製賦值 operator=(const Buffer&)", "a"), ("6.11：用 vector，一個都唔使寫", "next")])),
    Scene("recap",
          "總結：[[r1]]預設複製係淺複製，指標只抄地址；[[r2]]兩個物件共用記憶體，就會互相影響，仲會 double free；"
          "[[r3]]自己寫深複製：複製建構子同 operator 等號；[[r4]]記住 rule of three。",
          BulletCard("今集重點", [("預設：淺複製", "r1"), ("共用記憶體 → double free", "r2"), ("深複製：自己 new 再抄", "r3"),
                                ("rule of three", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 fill 成員函數，將所有格填入同一個數；複製之後填其中一個，確保另一個冇變。"
          "[[next]]下一集：move semantics，搬走而唔係複製。多謝收睇，下次見！",
          EndCard("加成員函數 fill(int v)；Buffer b = a; 之後 b.fill(1)，確保 a 冇變。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

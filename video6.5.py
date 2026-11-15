#!/usr/bin/env python3
"""Video 67 (syllabus 6.5): Destructor

A Tracer prints "+ name" when constructed and "- name" when destroyed; the real run shows b and c
destroyed in reverse order at the end of their block, a function's local destroyed on return,
and a last; an object made with new really never prints "- heap" (never destroyed) until it is
owned by a unique_ptr. Run `python3 video67.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 67
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-05"
FINAL = (CODE / "tracer.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
UNIQUE = "    auto h = std::make_unique<Tracer>(\"heap\");\n"
NEW = "    Tracer* h = new Tracer{\"heap\"};\n"
V1 = FINAL.replace(UNIQUE, "")
BAD = FINAL.replace(UNIQUE, NEW)
CLASS = "class Tracer" + FINAL.split("class Tracer")[1].split("void f")[0]
REST = "void f" + V1.split("void f")[1]
HEAD = "#include <iostream>\n#include <memory>\n#include <string>\n\n"
SKEL = HEAD.rstrip("\n")
CC = "g++ -std=c++20 -Wall -Wextra tracer.cpp -o tr"

(c1, r1, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"tracer.cpp": V1}, [
    CC, "./tr", "clear", Write("tracer.cpp", BAD), CC, "./tr", Write("tracer.cpp", FINAL), CC, "./tr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
base = ["main starts", "+ a", "+ b", "+ c", "- c", "- b", "+ in f", "- in f"]
assert r1.output.split("\n")[:-1] == base + ["main ends", "- a"], r1.output
assert r2.output.split("\n")[:-1] == base + ["+ heap", "main ends", "- a"], r2.output
assert r3.output.split("\n")[:-1] == base + ["+ heap", "main ends", "- heap", "- a"], r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.count("- loop") == 3

SAY = {"destructor": "destructor", "~Tracer": "波浪號 Tracer", "Tracer": "Tracer", "new": "new", "unique_ptr": "unique pointer",
       "make_unique": "make unique", "heap": "heap"}

s = Stage({"tracer.cpp": V1}, title="Destructor 解構子", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！5.8 見過解構子：物件消失嗰陣自動行。今集睇清楚佢究竟幾時行，同埋行嘅次序。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "~Tracer · 幾時行 · 次序")),
    Scene("goal",
          "今集會講：[[b1]]解構子點寫；[[b2]]物件幾時消失；[[b3]]幾個物件消失嘅次序；[[b4]]new 出嚟嘅物件會點。",
          BulletCard("今集學識", [("~Tracer()：解構子", "b1"), ("幾時消失", "b2"), ("消失嘅次序", "b3"), ("new 出嚟嘅物件", "b4")])),
    Scene("class",
          "[[ctor]]Tracer 建構嗰陣印加號同名，[[dtor]]解構嗰陣印減號同名。解構子係波浪號加 class 名，冇參數，冇回傳型別。",
          s.scene(Open("tracer.cpp", mode="empty"), Type("tracer.cpp", HEAD + CLASS, at="ctor", rate=60), Mark(10, at="dtor"))),
    Scene("main",
          "[[a]]main 入面先整 a；[[block]]再喺一對大括號入面整 b 同 c；[[f]]跟住呼叫 f，f 入面又整一個 Tracer。",
          s.scene(Mark(None), Type("tracer.cpp", REST.rstrip("\n"), at="a", rate=60), Expect("tracer.cpp", V1), Mark((25, 28), at="block"),
                  Mark(29, at="f"))),
    Scene("run1",
          "[[cc]]編譯運行，逐行睇：[[o1]]a、b、c 順序出世；[[o2]]大括號完，c 先消失，再到 b：次序同出世相反；"
          "[[o3]]f 入面嗰個，f 一完就消失；[[o4]]最後 main 完，a 先消失。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1), Note("後出世，先消失", at="o2", where="editor"))),
    Scene("rule",
          "記住兩條規則：[[scope]]物件喺離開佢嘅大括號嗰陣消失；[[rev]]同一個範圍入面，後建立嘅先消失，好似疊碟，最後放上去嘅最先攞走。",
          TableCard("真實嘅次序", ["行", "發生咩事"], [
              (["+ a, + b, + c", "a、b、c 依次建立"], "scope"),
              (["- c, - b", "大括號完：c 先，b 後"], "rev"),
              (["+ in f, - in f", "f 完：t 消失"], ("rev", 0.8)),
              (["main ends, - a", "main 完：a 消失"], ("rev", 1.6)),
          ], widths=[1.2, 1.6], code_cols=(0,), size=40)),
    Scene("heap",
          "[[type]]如果用 new 建立一個 Tracer 呢？[[cc]]編譯運行：g++ 警告 h 冇用到，唔緊要；[[o]]有加號 heap，但係直到程式完，都冇減號 heap！"
          "[[why]]new 出嚟嘅物件，唔會自己消失，冇 delete，解構子永遠唔會行。",
          s.scene(Run(clr, at="type"), Type("tracer.cpp", NEW, before="    std::cout << \"main ends", at="type"), Expect("tracer.cpp", BAD),
                  Run(c2, at="cc", recall=True), Run(r2), Note("冇 - heap：\n解構子冇行過", at="why", where="editor"))),
    Scene("fix",
          "[[fix]]改用 make_unique，交俾 unique_ptr 管。[[cc]]運行，[[o]]main 完嗰陣，減號 heap 出現咗：h 比 a 遲建立，所以比 a 早消失。",
          s.scene(Note(None), Replace("tracer.cpp", NEW, UNIQUE, at="fix"), Expect("tracer.cpp", FINAL), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]解構子係波浪號加 class 名，物件消失嗰陣自動行；[[r2]]離開大括號，物件就消失；[[r3]]後建立嘅先消失；"
          "[[r4]]new 出嚟嘅物件，要 delete，或者交俾智能指標管。",
          BulletCard("今集重點", [("~類名()：消失時自動行", "r1"), ("離開 { } 就消失", "r2"), ("後建立，先消失", "r3"),
                                ("new 出嚟：交俾 unique_ptr", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]喺一個 for 迴圈入面建立 Tracer，迴圈行三次，估吓會印乜，再運行驗證。[[next]]下一集：this 同 const 成員函數。多謝收睇，下次見！",
          EndCard("喺 for 迴圈入面建立 Tracer（行三次）。先估會印乜，再運行驗證。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

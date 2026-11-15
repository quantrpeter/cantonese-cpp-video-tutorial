#!/usr/bin/env python3
"""Video 84 (syllabus 7.4): Concepts

The same mistake twice: maxOf(p, q) with a Point that has no >. Unconstrained, g++ 15 really
reports "no match for 'operator>'" at line 5 inside maxOf, i.e. inside the template's own code.
With a concept Comparable (requires a > b) the real error is at the call: "constraints not
satisfied ... the required expression '(a > b)' is invalid". std::integral on isEven; the
final run prints 7 1. Run `python3 video7.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 84
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-04"
FINAL = (CODE / "concept.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CONCEPT = "template <typename T>\nconcept Comparable = requires(T a, T b) {\n    a > b;\n};\n\n"
ISEVEN = "template <std::integral T>\nbool isEven(T n) {\n    return n % 2 == 0;\n}\n\n"
PQ = "    Point p{1, 2}, q{3, 4};\n    maxOf(p, q);\n"
MAINF = "    std::cout << maxOf(3, 7) << ' ' << isEven(10) << '\\n';\n"
V2 = FINAL.replace("#include <concepts>\n", "").replace(ISEVEN, "").replace(MAINF, PQ)
V1 = V2.replace(CONCEPT, "").replace("template <Comparable T>", "template <typename T>")
CC = "g++ -std=c++20 -Wall -Wextra concept.cpp -o cn"

(c1, clr, c2, clr2, c3, r3, cch, rch) = cpp.session({"concept.cpp": V1}, [
    CC, "clear", Write("concept.cpp", V2), CC, "clear", Write("concept.cpp", FINAL), CC, "./cn",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
e1, e2 = cpp.visible(c1.output), cpp.visible(c2.output)
assert "concept.cpp:5:11: error: no match for 'operator>' (operand types are 'Point' and 'Point')" in e1, e1
assert "constraints not satisfied" in e2 and "the required expression '(a > b)' is invalid" in e2 and "concept.cpp:23:10" in e2, e2
assert r3.output == "7 1\n" and c3.code == cch.code == 0 and rch.output == "3\n"

SAY = {"concept": "concept", "concepts": "concepts", "Comparable": "Comparable", "requires": "requires", "a > b": "a 大過 b",
       "std::integral": "S T D integral", "std::floating_point": "S T D floating point", "std::totally_ordered": "S T D totally ordered",
       "isEven": "is even", "maxOf": "max of", "Point": "Point", "operator>": "operator 大過", "T": "T", "typename": "typename",
       "maxOf(p, q)": "max of p q", "<concepts>": "concepts"}

s = Stage({"concept.cpp": V1}, title="Concepts", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！7.1 講過，maxOf 要求 T 識比較大細，但係呢個要求只係寫喺我哋心入面。C++20 嘅 concepts，可以將要求寫落 code，等編譯器幫你檢查。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "concept · requires · C++20")),
    Scene("goal",
          "今集會講：[[b1]]冇 concept 嘅錯誤；[[b2]]寫自己嘅 concept；[[b3]]有 concept 嘅錯誤；[[b4]]標準庫嘅 concepts。",
          BulletCard("今集學識", [("同一個錯：冇 concept", "b1"), ("concept Comparable", "b2"), ("同一個錯：有 concept", "b3"),
                                ("std::integral 等等", "b4")])),
    Scene("before",
          "[[open]]Point 冇大過號。[[call]]main 照樣叫 maxOf p q。[[cc]]編譯：[[err]]錯誤講 operator 大過號唔夾，但係指住第五行，即係 maxOf 自己入面。"
          "[[why]]用嘅人要去讀人哋模板入面嘅 code，先知自己錯咗乜。",
          s.scene(Open("concept.cpp", at="open"), Mark((11, 14), at="open"), Mark(18, at="call"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Mark(5, at="err"), Note("錯誤喺 maxOf 入面\n唔係喺你叫佢嗰行", at="why"))),
    Scene("concept",
          "[[type]]寫一個 concept，叫 Comparable：requires 兩個 T，a 同 b，a 大過 b 要成立。[[use]]再將 typename 換做 Comparable："
          "T 一定要符合 Comparable。",
          s.scene(Note(None), Mark(None), Run(clr, at="type"), Type("concept.cpp", CONCEPT, before="template <typename T>\nT maxOf", at="type", rate=30),
                  Replace("concept.cpp", "template <typename T>\nT maxOf", "template <Comparable T>\nT maxOf", at="use"), Expect("concept.cpp", V2),
                  Mark((3, 6), at="type"), Mark(8, at="use"))),
    Scene("after",
          "[[cc]]同一個錯，再編譯：[[err]]今次錯誤指住第二十三行，即係叫 maxOf 嗰行；[[req]]仲講明原因：Comparable 唔滿足，a 大過 b 呢個表達式唔成立。"
          "[[good]]用嘅人唔使讀 maxOf 入面寫乜。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Scroll(at="err"), Mark(23, at="err"), Scroll(at="req", find="required expression"),
                  Note("錯誤喺你叫佢嗰行\n仲講明要乜", at="good"))),
    Scene("std",
          "標準庫已經有好多現成嘅 concepts：[[i]]std::integral，整數；[[f]]std::floating_point，浮點數；[[o]]std::totally_ordered，識晒比較。"
          "要 include concepts。",
          TableCard("標準 concepts（<concepts>）", ["concept", "意思"], [
              (["std::integral", "整數：int、long、char…"], "i"),
              (["std::floating_point", "浮點數：double、float"], "f"),
              (["std::totally_ordered", "識 <、>、== 晒"], "o"),
          ], widths=[1.4, 1.5], code_cols=(0,), size=40)),
    Scene("integral",
          "[[type]]寫一個 isEven，T 一定要係整數：std::integral，因為浮點數講單雙冇意思。[[main]]main 改做 maxOf 三、七，同 isEven 十。"
          "[[cc]]編譯運行，[[o]]七同一。如果傳 二點五 入 isEven，就會俾 concept 擋住。",
          s.scene(Note(None), Mark(None), Run(clr2, at="type"), Replace("concept.cpp", "#include <iostream>\n", "#include <concepts>\n#include <iostream>\n", at="type"),
                  Type("concept.cpp", ISEVEN, before="struct Point", rate=40), Replace("concept.cpp", PQ, MAINF, at="main"),
                  Expect("concept.cpp", FINAL), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("forms",
          "concept 有兩種常見寫法：[[a]]直接放喺角括號，代替 typename；[[b]]或者 typename T 之後，再寫 requires 子句。意思一樣。",
          TableCard("兩種寫法", ["寫法", "例子"], [
              (["代替 typename", "template <Comparable T>"], "a"),
              (["requires 子句", "template <typename T> requires Comparable<T>"], "b"),
          ], widths=[0.9, 2.2], code_cols=(1,), size=34)),
    Scene("recap",
          "總結：[[r1]]concept 將對類型嘅要求寫落 code；[[r2]]冇 concept，錯誤喺模板入面；[[r3]]有 concept，錯誤喺呼叫嗰行，仲講明要乜；"
          "[[r4]]標準庫有 std::integral 呢啲現成嘅 concepts。",
          BulletCard("今集重點", [("concept：寫低要求", "r1"), ("冇：錯喺模板入面", "r2"), ("有：錯喺呼叫，講明原因", "r3"),
                                ("<concepts>：std::integral…", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 Point 加 operator 大過號，比較 x，令 maxOf p q 編譯得到，印出大嗰個嘅 x。[[next]]下一集：constexpr 同 if constexpr。"
          "多謝收睇，下次見！",
          EndCard("幫 Point 加 bool operator>(const Point&) const（比 x），令 maxOf(p, q) 編譯到，印出 .x。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

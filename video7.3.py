#!/usr/bin/env python3
"""Video 83 (syllabus 7.3): 推導同 CTAD

Explicit std::vector<int>, std::pair<int, double> and Box<double> really print 3 2.5 / 3.5; with
the angle brackets removed (class template argument deduction) the output is the same. The
pitfall: std::vector names{"Amy", "Ben"} deduces const char*, so names[0] + names[1] is a real
"invalid operands ... {aka 'const char*'}" error; std::vector<std::string> prints AmyBen.
Run `python3 video7.3.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 83
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-03"
FINAL = (CODE / "ctad.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
NAMES = "    std::vector<std::string> names{\"Amy\", \"Ben\"};\n    std::cout << names[0] + names[1] << '\\n';\n"
V2 = FINAL.replace(NAMES, "").replace("#include <string>\n", "")
V1 = (V2.replace("std::vector v{", "std::vector<int> v{").replace("std::pair p{", "std::pair<int, double> p{")
      .replace("Box b{", "Box<double> b{"))
BAD = FINAL.replace("std::vector<std::string> names", "std::vector names")
CC = "g++ -std=c++20 -Wall -Wextra ctad.cpp -o ctad"

(c1, r1, clr, c2, r2, clr2, c3, clr3, c4, r4, cch, rch) = cpp.session({"ctad.cpp": V1}, [
    CC, "./ctad", "clear", Write("ctad.cpp", V2), CC, "./ctad", "clear", Write("ctad.cpp", BAD), CC,
    "clear", Write("ctad.cpp", FINAL), CC, "./ctad",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "3 2.5\n3.5\n" == r2.output and r4.output == "3 2.5\n3.5\nAmyBen\n", (r1.output, r4.output)
assert "{aka 'const char*'}" in cpp.visible(c3.output) and "to binary 'operator+'" in cpp.visible(c3.output), c3.output[:500]
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "hi A 7\n"

SAY = {"CTAD": "C T A D", "std::vector<int>": "vector 角括號 int", "std::pair<int, double>": "pair 角括號 int double",
       "Box<double>": "Box 角括號 double", "std::vector": "S T D vector", "std::pair": "S T D pair", "const char*": "const char 指標",
       "std::string": "S T D string", "Box": "Box", "T": "T", "Amy": "Amy", "Ben": "Ben", "maxOf": "max of",
       "names[0] + names[1]": "names 零 加 names 一", "p.second": "p 點 second"}

s = Stage({"ctad.cpp": V1}, title="推導同 CTAD", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！用模板嘅時候，角括號入面嘅類型，好多時其實可以唔寫，由編譯器自己推導出嚟。今集講模板參數推導，同埋 C++17 嘅 CTAD。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "推導 · CTAD · 陷阱")),
    Scene("goal",
          "今集會講：[[b1]]函數模板點樣推導；[[b2]]類別模板參數推導，CTAD；[[b3]]自己嘅 class 都得；[[b4]]字串常數嘅陷阱。",
          BulletCard("今集學識", [("函數模板：睇參數推導", "b1"), ("CTAD：class 都可以推導", "b2"), ("Box b{3.5}", "b3"),
                                ("陷阱：\"Amy\" 係 const char*", "b4")])),
    Scene("full",
          "[[box]]Box 係一個類別模板，建構子收一個 T。[[main]]main 整三樣嘢，每樣都寫明類型：vector 角括號 int，pair 角括號 int double，"
          "Box 角括號 double。[[cc]]印出 vector 嘅大小、pair 嘅第二個，同埋 Box 入面嘅值。編譯運行，[[o]]三，二點五，三點五。",
          s.scene(Open("ctad.cpp", at="box"), Mark((5, 15), at="box"), Mark((18, 20), at="main"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("deduce",
          "記得上一集 maxOf 三、七？[[fn]]函數模板會睇參數，自己推導出 T 係 int。[[cls]]C++17 開始，class 都得：睇建構子收到乜，推導出角括號入面嘅類型，"
          "叫做 CTAD。",
          TableCard("推導：睇參數", ["寫法", "推導出"], [
              (["maxOf(3, 7)", "T = int"], "fn"),
              (["std::vector v{1, 2, 3}", "std::vector<int>"], "cls"),
              (["Box b{3.5}", "Box<double>"], ("cls", 1.2)),
          ], widths=[1.4, 1.2], code_cols=(0, 1), size=40)),
    Scene("drop",
          "[[del]]所以三個角括號都可以刪走：[[v]]一、二、三係 int；[[p]]一同二點五，係 int 同 double；[[b]]三點五係 double，Box 嘅 T 就係 double。"
          "[[cc]]編譯運行，[[o]]結果一樣。",
          s.scene(Run(clr, at="del"), Replace("ctad.cpp", "std::vector<int> v{", "std::vector v{", at="v"),
                  Replace("ctad.cpp", "std::pair<int, double> p{", "std::pair p{", at="p"), Replace("ctad.cpp", "Box<double> b{", "Box b{", at="b"),
                  Expect("ctad.cpp", V2), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("trap",
          "陷阱嚟喇：[[type]]一個 vector 裝兩個名，Amy 同 Ben，再將兩個名加埋。[[cc]]編譯：[[err]]錯誤！兩個 const char 指標唔可以相加。"
          "[[why]]因為雙引號嘅字串常數，類型唔係 std::string，而係 const char 指標，CTAD 就照推導咗出嚟。",
          s.scene(Run(clr2, at="type"), Replace("ctad.cpp", "#include <iostream>\n", "#include <iostream>\n#include <string>\n", at="type"),
                  Type("ctad.cpp", NAMES.replace("std::vector<std::string> names", "std::vector names"), before="}", last=True, rate=30),
                  Expect("ctad.cpp", BAD), Run(c3, at="cc", recall=True), Scroll(at="err"),
                  Note("\"Amy\"：const char*\n唔係 std::string", at="why", where="editor"))),
    Scene("fix",
          "[[type]]呢個時候就要自己寫明：vector 角括號 std::string。[[cc]]編譯運行，[[o]]AmyBen，兩個字串駁埋。",
          s.scene(Note(None), Run(clr3, at="type"), Replace("ctad.cpp", "std::vector names", "std::vector<std::string> names", at="type"),
                  Expect("ctad.cpp", FINAL), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("when",
          "幾時要寫角括號？[[ok]]有初始值，而且類型清楚，可以省略；[[empty]]空嘅 vector 冇嘢推導，一定要寫；[[str]]字串常數想要 std::string，都要寫。",
          TableCard("寫唔寫角括號？", ["情況", "寫法"], [
              (["有值，類型清楚", "std::vector v{1, 2, 3};"], "ok", GREEN),
              (["空嘅", "std::vector<int> v;"], "empty", AMBER),
              (["想要 std::string", "std::vector<std::string> n{\"Amy\"};"], "str", AMBER),
          ], widths=[1, 1.9], code_cols=(1,), size=36)),
    Scene("recap",
          "總結：[[r1]]函數模板睇參數推導 T；[[r2]]C++17 嘅 CTAD，class 都可以睇建構子推導；[[r3]]推導出嚟嘅係真正嘅類型，雙引號係 const char 指標；"
          "[[r4]]唔清楚嘅時候，自己寫明。",
          BulletCard("今集重點", [("函數模板：睇參數", "r1"), ("CTAD：睇建構子", "r2"), ("\"Amy\" → const char*", "r3"), ("唔清楚：自己寫", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 CTAD 整一個裝 std::string 嘅 Box，同一個 pair，裝一個字元同一個整數，印出嚟。[[next]]下一集：C++20 嘅 concepts。"
          "多謝收睇，下次見！",
          EndCard("用 CTAD：Box s{std::string{\"hi\"}}; std::pair p{'A', 7}; 印出 s.get()、p.first、p.second。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 39 (syllabus 3.10): 拆開多個檔案

mathutil.h (declarations), mathutil.cpp (definitions), main.cpp (uses them). Compiling only
main.cpp is a real "undefined reference" link error; compiling both works; a header included
twice without #pragma once is a real redefinition error. Run `python3 video3.10.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 39
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-10"
H = (CODE / "mathutil.h").read_text()
CPP = (CODE / "mathutil.cpp").read_text()
MAIN = (CODE / "main.cpp").read_text()
CH = {n: (CODE / "challenge" / n).read_text() for n in ("greet.h", "greet.cpp", "main.cpp")}
INC = "#include \"mathutil.h\"\n"
MAIN2 = MAIN.replace(INC, INC + INC)                  # included twice, as happens through other headers
H_NOPRAGMA = H.replace("#pragma once\n\n", "")
ONE = "g++ -std=c++20 -Wall -Wextra main.cpp -o app"
BOTH = "g++ -std=c++20 -Wall -Wextra main.cpp mathutil.cpp -o app"

(c1, c2, r2, clr, c3, c4, r4, rch) = cpp.session({"mathutil.h": H, "mathutil.cpp": CPP, "main.cpp": MAIN}, [
    ONE, BOTH, "./app",
    Write("main.cpp", MAIN2), Write("mathutil.h", H_NOPRAGMA), "clear", BOTH,
    Write("mathutil.h", H), BOTH, "./app",
    Write("main.cpp", MAIN),
    Write("greet.h", CH["greet.h"]), Write("greet.cpp", CH["greet.cpp"]), Write("challenge.cpp", CH["main.cpp"]),
    "g++ -std=c++20 -Wall -Wextra challenge.cpp greet.cpp -o ch && ./ch",
], refresh=opts.fresh_runs, cols=58)
assert "undefined reference to `square(int)'" in cpp.visible(c1.output) and c1.code != 0
assert r2.output.split() == ["49", "27"] and c2.code == 0
assert "redefinition of 'constexpr const double pi'" in cpp.visible(c3.output), c3.output
assert c4.code == 0 and r4.output.split() == ["49", "27"] and "Hello from greet.cpp!" in rch.output

SAY = {"mathutil.h": "math util 點 h", "mathutil.cpp": "math util 點 C P P", "main.cpp": "main 點 C P P", "mathutil": "math util",
       ".h": " 點 h", "#pragma once": "pragma once", "pragma once": "pragma once", "square": "square", "cube": "cube"}

s = Stage({"mathutil.h": H, "mathutil.cpp": CPP, "main.cpp": MAIN}, title="拆開多個檔案", split=0.45, code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！程式越嚟越大，全部擠喺一個檔案，好難管理。今集學點樣將函數拆去另一個檔案。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, ".h · .cpp · #pragma once")),
    Scene("goal",
          "今集會講：[[b1]]標頭檔 .h：放宣告；[[b2]].cpp 檔：放定義；[[b3]]點樣一次過編譯幾個檔案；[[b4]]#pragma once 有乜用。",
          BulletCard("今集學識", [("標頭檔 .h：宣告", "b1"), (".cpp：定義", "b2"), ("編譯幾個檔案", "b3"), ("#pragma once", "b4")])),
    Scene("files",
          "我哋會有三個檔案：[[h]]mathutil.h 係標頭檔，好似一份目錄，話俾人知有咩函數；[[cpp]]mathutil.cpp 放真正嘅做法；"
          "[[main]]main.cpp 就 include 個標頭檔，用嗰啲函數。",
          TileCard("三個檔案", [
              Tile("📑", "mathutil.h", "宣告：有咩函數\n（目錄）", "h", PURPLE),
              Tile("⚙️", "mathutil.cpp", "定義：點樣做", "cpp", BLUE),
              Tile("🚀", "main.cpp", "include 標頭檔\n用啲函數", "main", GREEN),
          ], height=360)),
    Scene("header",
          "[[open]]標頭檔入面，有一個常數 pi，同埋兩個函數嘅宣告，冇大括號。[[pragma]]第一行嘅 #pragma once，等陣再講。",
          s.scene(Open("mathutil.h", mode="instant", at="open"), Mark((5, 6), at="open"), Mark(1, at="pragma"))),
    Scene("source",
          "[[open]]mathutil.cpp 放定義。[[inc]]佢自己都 include 個標頭檔，留意用雙引號：自己寫嘅檔案用雙引號，標準庫就用角括號。"
          "[[main]]main.cpp 只要 include mathutil.h，就可以用 square 同 cube。",
          s.scene(Mark(None), Open("mathutil.cpp", mode="instant", at="open"), Mark(1, at="inc"),
                  Open("main.cpp", mode="instant", at="main"), Mark(2, at="main"))),
    Scene("one",
          "[[cc]]試吓淨係編譯 main.cpp：[[err]]連結錯誤，搵唔到 square 同 cube。記得 3.3：宣告有咗，但係定義喺 mathutil.cpp，"
          "我哋冇交俾 g++。",
          s.scene(Mark(None), Run(c1, at="cc"), Note("淨係 main.cpp：\n搵唔到定義", at="err", where="editor"))),
    Scene("both",
          "[[cc]]兩個 .cpp 都要一齊交俾 g++；標頭檔就唔使，因為佢已經俾 include 咗。[[run]]運行，[[o]]四十九同二十七。",
          s.scene(Note(None), Run(c2, at="cc"), Run(r2, at="run"))),
    Scene("how",
          "g++ 背後做咗兩步：[[c1]]每個 .cpp 先各自編譯，[[c2]]然後連結器將佢哋砌埋一齊，變成一個程式。"
          "[[why]]所以改咗 mathutil.cpp，只係需要重新編譯嗰一個檔案，大程式就快好多。第十章會再講。",
          FlowCard("編譯，再連結", [
              Row("main", ".cpp", GREEN, [Node("main.cpp", "", "c1"), Node("編譯", "→ main.o", "c1"), Node("連結", "砌埋一齊", "c2", col=2),
                                         Node("app", "程式", "c2", col=3)]),
              Row("mathutil", ".cpp", BLUE, [Node("mathutil.cpp", "", "c1"), Node("編譯", "→ mathutil.o", "c1")]),
          ], top=280, row_h=230)),
    Scene("twice",
          "最後講 #pragma once。[[dup]]大程式入面，同一個標頭檔好容易被 include 兩次，例如兩個標頭檔都 include 咗佢。"
          "[[del]]如果標頭檔冇 #pragma once，[[cc]]編譯：[[err]]出錯，pi 重複定義。",
          s.scene(Run(clr, at="dup"), Type("main.cpp", INC, after=INC, at="dup"),
                  Replace("mathutil.h", "#pragma once\n\n", "", at="del"), Expect("mathutil.h", H_NOPRAGMA),
                  Expect("main.cpp", MAIN2), Run(c3, at="cc", recall=True))),
    Scene("pragma",
          "[[fix]]加返 #pragma once：佢保證每個標頭檔，喺同一個 .cpp 入面只會被包含一次。[[cc]]再編譯運行，[[o]]冇問題。"
          "[[rule]]所以每個標頭檔，第一行都寫 #pragma once。",
          s.scene(Type("mathutil.h", "#pragma once\n\n", before="constexpr", at="fix"), Expect("mathutil.h", H),
                  Run(c4, at="cc", recall=True), Run(r4),
                  Replace("main.cpp", INC + INC, INC, at="rule"), Expect("main.cpp", MAIN))),
    Scene("recap",
          "總結：[[r1]]標頭檔放宣告，.cpp 放定義；[[r2]]自己嘅標頭檔用雙引號 include；[[r3]]所有 .cpp 都要交俾 g++；"
          "[[r4]]每個標頭檔第一行寫 #pragma once。",
          BulletCard("今集重點", [(".h 宣告，.cpp 定義", "r1"), ("#include \"mathutil.h\"：雙引號", "r2"),
                                ("所有 .cpp 都交俾 g++", "r3"), ("標頭檔第一行：#pragma once", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個 greet.h 同 greet.cpp，入面有個 sayHello 函數，再喺 main.cpp 呼叫佢。"
          "[[next]]下一集，我哋講 namespace。多謝收睇，下次見！",
          EndCard("整 greet.h 同 greet.cpp，入面有 sayHello()；喺 main.cpp 呼叫佢，三個檔案一齊編譯。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 118 (syllabus 10.1): 編譯三部曲

main.cpp + greet.h + greet.cpp built step by step. `g++ -E main.cpp | wc -l` really shows
36,895 lines after the preprocessor (iostream pasted in); `tail -4` shows our main at the end.
`g++ -c` makes main.o and greet.o; linking main.o alone is a real "undefined reference to
`greet(...)'" from ld; linking both runs: Hello, Amy! Run `python3 video118.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 118
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-01"
FILES = {f: (CODE / f).read_text() for f in ["main.cpp", "greet.h", "greet.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()

(wc, tail, clr, cm, cg, ls, clr2, l1, l2, run, ch1, ch2) = cpp.session(FILES, [
    "g++ -E main.cpp | wc -l", "g++ -E main.cpp | tail -4", "clear", "g++ -c main.cpp", "g++ -c greet.cpp", "ls", "clear",
    "g++ main.o -o hello", "g++ main.o greet.o -o hello", "./hello",
    Write("challenge.cpp", CHALLENGE), "g++ -c challenge.cpp", "g++ challenge.o greet.o -o ch",
], refresh=opts.fresh_runs, cols=48)
nlines = int(wc.output.strip())
assert nlines > 20000 and 'std::cout << greet("Amy")' in tail.output, (wc.output, tail.output)
assert ls.output.split() == ["greet.cpp", "greet.h", "greet.o", "main.cpp", "main.o"], ls.output
assert "undefined reference to `greet(" in l1.output and l1.code != 0 and l2.code == 0 and run.output == "Hello, Amy!\n"
assert ch1.code == 0 and "undefined reference to `farewell(" in ch2.output
D = "零一二三四五六七八九"
say_lines = f"{D[nlines // 10000]}萬{D[nlines // 1000 % 10]}千幾"

SAY = {"g++ -E": "g 加加 E", "-E": "E", "-c": "c", "main.o": "main 點 o", "greet.o": "greet 點 o", ".o": "點 o", "greet.h": "greet 點 h",
       "greet.cpp": "greet 點 c p p", "main.cpp": "main 點 c p p", "#include": "include", "#pragma once": "pragma once",
       "undefined reference": "undefined reference", "ld": "l d", "linker": "linker", "wc -l": "w c l", "tail": "tail", "farewell": "farewell",
       "preprocessor": "preprocessor"}

s = Stage(FILES, title="編譯三部曲", code_px=26)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十部分講工具同真正嘅工程。我哋成日一句 g++ 就由 cpp 變出程式，其實入面分三步：預處理、編譯、連結。今集逐步拆開嚟睇。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "預處理 · 編譯 · 連結")),
    Scene("goal",
          "今集會講：[[b1]]預處理，D 嘅 E；[[b2]]編譯，D 嘅 c，出 o 檔；[[b3]]連結；[[b4]]點分 compile error 同 link error。",
          BulletCard("今集學識", [("預處理：g++ -E", "b1"), ("編譯：g++ -c → .o", "b2"), ("連結：.o → 程式", "b3"), ("compile error vs link error", "b4")])),
    Scene("files",
          "三個檔：[[h]]greet.h 只係宣告 greet；[[cpp]]greet.cpp 寫佢嘅內容；[[main]]main.cpp include greet.h，叫 greet。好似 3.10 咁。",
          s.scene(Open("greet.h", at="h"), Mark(4, at="h"), Open("greet.cpp", at="cpp"), Mark((3, 5), at="cpp"), Open("main.cpp", at="main"),
                  Mark((2, 5), at="main"))),
    Scene("pipeline",
          "[[pre]]第一步預處理：處理所有井號開頭嘅指令，include 就係將成個檔案貼入嚟；[[comp]]第二步編譯：將每個 cpp 變成機器碼，叫 object file；[[link]]第三步連結："
          "將所有 o 檔砌埋，變成一個程式。",
          BoxesCard("由 .cpp 到程式", [
              BoxRow([Box("main.cpp", "#include 貼入", "① 預處理", at="pre", color=PURPLE, w=460, key="a")]),
              BoxRow([Box("main.o", "機器碼", "② 編譯", at="comp", color=BLUE, w=340, key="b"), Box("greet.o", "機器碼", "② 編譯", at="comp", color=BLUE, w=340, key="c")], gap=80),
              BoxRow([Box("hello", "可以執行", "③ 連結", at="link", color=GREEN, w=460, key="d")]),
          ], top=CONTENT_TOP - 20, row_h=220, box_h=100, size=44)),
    Scene("pre",
          "[[e]]g++ D E 只做預處理。用 w c l 數吓有幾多行：[[n]]" + say_lines + "行！全部係 iostream 貼入嚟嘅。[[tail]]睇最尾四行，先至係我哋自己寫嘅 main。",
          s.scene(Mark(None), Run(wc, at="e"), Run(tail, at="tail"))),
    Scene("compile",
          "[[c]]g++ D c，只編譯唔連結：main.cpp 變 main.o，[[g]]greet.cpp 變 greet.o。[[ls]]ls 睇吓，多咗兩個 o 檔。[[know]]main.o 只係知道有 greet 呢個函數，唔知佢喺邊。",
          s.scene(Run(clr, at="c"), Run(cm), Run(cg, at="g"), Run(ls, at="ls"), Note("main.o：識 greet 個名\n但係冇佢嘅 code", at="know"))),
    Scene("link",
          "[[one]]如果只連結 main.o：[[err]]錯誤，undefined reference to greet：連結器搵唔到 greet 嘅定義。[[two]]加埋 greet.o 再連結，[[run]]運行：Hello, Amy!程式終於砌好。",
          s.scene(Note(None), Run(clr2, at="one"), Run(l1), Run(l2, at="two"), Run(run, at="run"))),
    Scene("errors",
          "[[ce]]compile error 係 g++ 自己講，通常有檔名同行號，例如打錯字、類型唔夾；[[le]]link error 由 ld 講，通常係 undefined reference：有宣告，冇定義，或者漏咗某個 o 檔。",
          TableCard("點分錯誤？", ["", "邊個講", "常見原因"], [
              (["compile error", "g++（有行號）", "語法、類型錯"], "ce"),
              (["link error", "ld：undefined reference", "冇定義、漏咗 .o"], "le", AMBER),
          ], widths=[1.1, 1.4, 1.2], code_cols=(0,), size=38)),
    Scene("recap",
          "總結：[[r1]]預處理將 include 貼入嚟；[[r2]]編譯將每個 cpp 變成 o 檔；[[r3]]連結將所有 o 檔砌成程式；[[r4]]undefined reference 係連結錯，搵吓個定義喺邊。",
          BulletCard("今集重點", [("-E：預處理", "r1"), ("-c：.cpp → .o", "r2"), ("連結：.o → 程式", "r3"), ("undefined reference：連結錯", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 cpp，宣告 farewell 但係唔寫定義，再叫佢。估吓 D c 嗰步會唔會出錯，連結嗰步又會點。[[next]]下一集：preprocessor 同 macro。多謝收睇，下次見！",
          EndCard("宣告 std::string farewell(const std::string&); 但唔定義，main 叫佢：g++ -c 過唔過？連結會出咩錯？",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

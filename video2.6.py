#!/usr/bin/env python3
"""Video 24 (syllabus 2.6): while 迴圈

A countdown with while, traced step by step; without n-- it really loops forever and is
stopped with Ctrl+C (the real output scrolls by); summing numbers until 0 is entered.
Run `python3 video2.6.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 24
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-06"
LOOP = (CODE / "loop.cpp").read_text()
SUM = (CODE / "sum.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
DEC = "        n--;\n"
FOREVER = LOOP.replace(DEC, "")
CL = "g++ -std=c++20 -Wall -Wextra loop.cpp -o loop"
CS = "g++ -std=c++20 -Wall -Wextra sum.cpp -o sum"

(c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"loop.cpp": LOOP, "sum.cpp": SUM}, [
    CL, "./loop",
    Write("loop.cpp", FOREVER), CL, Input("./loop", [("^C", 1.5)]),
    "clear", CS, Input("./sum", ["5", "10", "20", "0"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["5", "4", "3", "2", "1", "Go!"]
assert r2.code == 130 and r2.output.rstrip().endswith("^C") and set(r2.output.split()[:-1]) == {"5"}
assert r3.output.endswith("Total: 35\n") and r3.output.count("Number (0 to stop): ") == 4
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.strip() == "5050"

SAY = {"while": "while", "n--": "n minus minus", "Ctrl": "control", "Ctrl+C": "control C"}

s = Stage({"loop.cpp": LOOP, "sum.cpp": SUM}, title="while 迴圈")

scenes = [
    Scene("intro",
          "歡迎返嚟！想程式重複做同一樣嘢，就要用迴圈。今集學第一種迴圈：while。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "while · 死循環 · Ctrl+C")),
    Scene("goal",
          "今集會講：[[b1]]while 迴圈點樣運作；[[b2]]死循環，同埋點樣用 Ctrl+C 停止；[[b3]]用 while 一路讀數字，讀到零為止。",
          BulletCard("今集學識", [("while 迴圈 loop", "b1"), ("死循環同 Ctrl+C", "b2"), ("讀到 0 為止", "b3")])),
    Scene("countdown",
          "[[open]]呢個程式會倒數。[[cond]]while 後面係條件：n 大過零。[[body]]條件成立，就行大括號入面嘅嘢：印出 n，再減一。"
          "[[back]]行完之後，返去再檢查條件，一直重複，直到條件唔成立為止。",
          s.scene(Open("loop.cpp", at="open"), Mark(5, at="cond"), Mark((6, 7), at="body"), Mark(5, at="back"))),
    Scene("run1",
          "[[cc]]編譯運行。[[out]]五、四、三、二、一，最後 Go!。n 變咗零之後，條件唔成立，就離開迴圈，行下面嗰句。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1))),
    Scene("trace",
          "逐步睇：[[r5]]n 係五，五大過零，印五，n 變四；[[r4]]四、三、二、一，都係咁；[[r0]]到 n 係零，條件唔成立，迴圈就完。"
          "[[note]]所以大括號入面一共行咗五次。",
          TableCard("每一次檢查", ["n", "n > 0？", "做咩"], [
              (["5", "true", "印 5，n 變 4"], "r5"),
              (["4", "true", "印 4，n 變 3"], ("r4", 0.0)),
              (["3 · 2 · 1", "true", "印出嚟，再減一"], ("r4", 0.6)),
              (["0", "false", "離開迴圈，印 Go!"], "r0", RED),
          ], widths=[0.8, 0.8, 1.8], code_cols=(0, 1), size=42, note=("迴圈入面行咗 5 次", "note"))),
    Scene("forever",
          "如果唔記得 n-- 呢句會點？[[del]]刪走佢。[[cc]]編譯運行：[[flood]]n 永遠係五，條件永遠成立，程式不停咁印五，停唔到！"
          "呢個叫死循環。[[ctrl]]撳 Ctrl 同 C，就可以強制停止個程式。",
          s.scene(Replace("loop.cpp", DEC, "", at="del"), Expect("loop.cpp", FOREVER), Run(c2, at="cc", recall=True),
                  Run(r2, keys=("ctrl",)), Note("死循環：撳 Ctrl + C 停止", at="ctrl", where="editor"))),
    Scene("forever_why",
          "所以寫 while 嘅時候，記住問自己：[[change]]迴圈入面，有冇嘢會令條件最終變成 false？冇嘅話，就會變成死循環。"
          "[[fix]]加返 n-- 就得。",
          s.scene(Note("迴圈入面要有嘢\n令條件最終變 false", at="change", where="editor"),
                  Note(None, at="fix"), Type("loop.cpp", DEC, after="std::cout << n << '\\n';\n", at="fix"), Expect("loop.cpp", LOOP))),
    Scene("sum",
          "while 最常見嘅用法，係唔知要重複幾多次嘅時候。[[open]]呢個程式不停讀數字，加埋佢哋，直到輸入零為止。"
          "[[first]]第一個數喺迴圈前面讀；[[loop]]唔係零，就加入總數，再讀下一個。",
          s.scene(Run(clr), Open("sum.cpp", at="open"), Mark((6, 7), at="first"), Mark((8, 12), at="loop"))),
    Scene("run2",
          "[[cc]]編譯運行。[[t1]]第一個數輸入五，[[t2]]再輸入十，[[t3]]再輸入二十，[[t4]]最後輸入零，迴圈就停。"
          "[[out]]總數係三十五，即係五加十加二十。",
          s.scene(Mark(None), Run(c3, at="cc"), Run(r3, keys=("t1", "t2", "t3", "t4")))),
    Scene("rules",
          "記住 while 嘅三個重點：[[r1]]條件喺開頭檢查，一開始唔成立，就一次都唔會行；[[r2]]迴圈入面一定要有嘢改變條件；"
          "[[r3]]唔知要行幾多次嘅時候，就用 while。",
          BulletCard("while 三個重點", [("條件喺開頭檢查：可能一次都唔行", "r1"), ("入面要改變條件，唔係就死循環", "r2"),
                                      ("唔知次數：用 while", "r3")])),
    Scene("recap",
          "總結：[[r1]]while 條件成立就重複；[[r2]]死循環用 Ctrl+C 停止；[[r3]]讀到某個值為止，係 while 嘅典型用法。",
          BulletCard("今集重點", [("while：條件成立就重複", "r1"), ("死循環：Ctrl + C", "r2"), ("讀到 0 為止", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]用 while，由一加到一百，印出總數。"
          "[[next]]下一集，我哋學另一種迴圈：for。多謝收睇，下次見！",
          EndCard("用 while 由 1 加到 100，印出總數。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

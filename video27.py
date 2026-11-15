#!/usr/bin/env python3
"""Video 27 (syllabus 2.9): 巢狀迴圈

A square of stars from two loops, then a triangle by changing the inner condition to `row`,
traced row by row; the newline moved into the inner loop really prints a column of stars; the
9 x 9 times table aligned with std::setw. Run `python3 video27.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 27
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-09"
TRI = (CODE / "star.cpp").read_text()
NINE = (CODE / "nine.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SQUARE = TRI.replace("col <= row", "col <= n")
GOOD_NL = "            std::cout << '*';\n        }\n        std::cout << '\\n';\n"
BAD_NL = "            std::cout << '*';\n            std::cout << '\\n';\n        }\n"
NLBAD = TRI.replace(GOOD_NL, BAD_NL)
CS = "g++ -std=c++20 -Wall -Wextra star.cpp -o star"
CN = "g++ -std=c++20 -Wall -Wextra nine.cpp -o nine"

(c1, r1, c2, r2, c3, r3, clr, c4, r4, cch, rch) = cpp.session({"star.cpp": SQUARE, "nine.cpp": NINE}, [
    CS, Input("./star", ["5"]),
    Write("star.cpp", TRI), CS, Input("./star", ["5"]),
    Write("star.cpp", NLBAD), CS, Input("./star", ["5"]),
    "clear", CN, "./nine",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["4"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("*****\n" * 5)
assert r2.output.endswith("".join("*" * k + "\n" for k in range(1, 6)))
assert r3.output.endswith("*\n" * 15)
table = r4.output.rstrip("\n").split("\n")
assert len(table) == 9 and table[8].split()[-1] == "81" and table[0] == "".join(f"{k:3}" for k in range(1, 10))
assert all(r.code == 0 for r in (c1, c2, c3, c4, cch)) and rch.output.endswith("****\n***\n**\n*\n")

SAY = {"setw(3)": "set W 三", "setw": "set W", "setprecision": "set precision", "iomanip": "I O manip", "row": "row", "col": "col"}

s = Stage({"star.cpp": SQUARE, "nine.cpp": NINE}, title="巢狀迴圈")

scenes = [
    Scene("intro",
          "歡迎返嚟！迴圈入面，可以再有迴圈，叫巢狀迴圈。今集用佢砌星星三角形，同埋印九因歌。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "迴圈入面嘅迴圈")),
    Scene("goal",
          "今集會講：[[b1]]巢狀迴圈點樣運作；[[b2]]外層同內層各自負責乜；[[b3]]用 setw 將輸出排整齊。",
          BulletCard("今集學識", [("巢狀迴圈 nested loop", "b1"), ("外層管行，內層管每行入面", "b2"), ("setw：排整齊", "b3")])),
    Scene("square",
          "[[open]]先砌一個正方形。[[outer]]外層迴圈管行：row 由一到 n；[[inner]]內層迴圈管每一行入面嘅星：col 由一到 n；"
          "[[nl]]內層行完，即係一行印完，就換行。",
          s.scene(Open("star.cpp", at="open"), Mark(7, at="outer"), Mark((8, 10), at="inner"), Mark(11, at="nl"))),
    Scene("run1",
          "[[cc]]編譯運行，[[t]]輸入五。[[o]]五行，每行五粒星，一個正方形。[[count]]外層每行一次，內層就行晒五次，總共印咗二十五粒星。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("t",)),
                  Note("外層 5 次 × 內層 5 次\n＝ 25 粒星", at="count", where="editor"))),
    Scene("triangle",
          "想要三角形：第一行一粒，第二行兩粒，如此類推。[[edit]]只要將內層嘅條件，由 n 改做 row，每一行就印 row 粒星。"
          "[[cc]]再運行，[[t]]輸入五，[[o]]三角形出咗嚟。",
          s.scene(Note(None), Replace("star.cpp", "col <= n", "col <= row", at="edit"), Expect("star.cpp", TRI),
                  Mark(8, at="edit"), Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("t",)))),
    Scene("trace",
          "逐行睇：[[r1]]row 係一，內層由一行到一，印一粒；[[r2]]row 係二，印兩粒；[[r5]]一直到 row 係五，印五粒。"
          "[[key]]關鍵係：內層嘅次數，跟住外層嘅 row 變。",
          TableCard("每一行", ["row", "內層：col 由 1 到", "印出"], [
              (["1", "1", "*"], "r1"), (["2", "2", "**"], "r2"), (["3", "3", "***"], ("r2", 0.6)),
              (["4", "4", "****"], ("r2", 1.2)), (["5", "5", "*****"], "r5"),
          ], widths=[0.6, 1.4, 1], code_cols=(0, 1, 2), size=40, note=("內層嘅次數跟住 row 變", "key"))),
    Scene("mistake",
          "如果換行放錯位置，[[mv]]放咗入內層迴圈入面，[[cc]]運行，[[t]]輸入五，[[o]]每粒星都換一行，變咗一條直線。"
          "[[fix]]換行要放喺內層外面、外層入面：一行印完，先換行。",
          s.scene(Mark(None), Replace("star.cpp", GOOD_NL, BAD_NL, at="mv"), Expect("star.cpp", NLBAD),
                  Run(c3, at="cc", recall=True), Run(r3, recall=True, keys=("t",)),
                  Replace("star.cpp", BAD_NL, GOOD_NL, at="fix"), Expect("star.cpp", TRI))),
    Scene("nine",
          "再嚟一個經典例子：九因歌。[[open]]i 係外層，j 係內層，每一格印 i 乘 j。[[setw]]setw(3) 令每個數字佔三格位，排得整齊；"
          "佢同 setprecision 一樣，喺 iomanip 入面。",
          s.scene(Run(clr), Open("nine.cpp", at="open"), Mark((5, 6), at="open"), Mark(7, at="setw"))),
    Scene("run2",
          "[[cc]]編譯運行，[[o]]九乘九嘅乘數表，一格一格排得好整齊。[[count]]留意：外層九次，內層又九次，總共行咗八十一次。"
          "巢狀迴圈嘅次數係相乘嘅，數字一大就會好慢，第十二章會再講。",
          s.scene(Mark(None), Run(c4, at="cc"), Run(r4), Note("9 × 9 = 81 次", at="count", where="editor"))),
    Scene("recap",
          "總結：[[r1]]迴圈入面可以再有迴圈；[[r2]]外層每行一次，內層就行晒一輪；[[r3]]內層嘅範圍可以跟住外層變，砌出三角形；"
          "[[r4]]setw 令輸出對齊。",
          BulletCard("今集重點", [("巢狀迴圈：迴圈入面嘅迴圈", "r1"), ("外層一次，內層一整輪", "r2"),
                                ("內層範圍跟外層變：三角形", "r3"), ("std::setw(n) 對齊", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]印一個倒轉嘅三角形：第一行五粒星，最後一行一粒。"
          "[[next]]下一集，我哋學點樣產生隨機數。多謝收睇，下次見！",
          EndCard("印一個倒轉嘅三角形：第一行 n 粒星，最後一行 1 粒。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 19 (syllabus 2.1): if / else

Pass or fail with if, then else; the six comparison operators (results from a real run); the
`if (mark = 100)` bug that really says "Full marks!" for 75, with g++'s -Wparentheses warning.
Run `python3 video19.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 19
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-01"
FINAL = (CODE / "pass.cpp").read_text()
COMPARE = (CODE / "compare.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
FULL = "    if (mark == 100) {\n        std::cout << \"Full marks!\\n\";\n    }\n"
ELSE = " else {\n        std::cout << \"Fail\\n\";\n    }"
IF = "    if (mark >= 50) {\n        std::cout << \"Pass\\n\";\n    }\n"
V2 = FINAL.replace(FULL, "")
V1 = V2.replace(ELSE, "")
V0 = V1.replace(IF, "")
BUG = FINAL.replace("mark == 100", "mark = 100")
CC = "g++ -std=c++20 -Wall -Wextra pass.cpp -o pass"

(c1, r1a, r1b, c2, r2, clr, c3, r3, c4, r4a, r4b, cc_, rc, cch, rch) = cpp.session({"pass.cpp": V1, "compare.cpp": COMPARE}, [
    CC, Input("./pass", ["75"]), Input("./pass", ["30"]),
    Write("pass.cpp", V2), CC, Input("./pass", ["30"]),
    Write("pass.cpp", BUG), "clear", CC, Input("./pass", ["75"]),
    Write("pass.cpp", FINAL), CC, Input("./pass", ["75"]), Input("./pass", ["100"]),
    "g++ -std=c++20 compare.cpp -o compare", "./compare",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["7"]),
], refresh=opts.fresh_runs, cols=48)
assert r1a.output.endswith("Pass\n") and r1b.output == "Mark: 30\n" and r2.output.endswith("Fail\n")
assert "suggest parentheses around assignment used as truth value" in cpp.visible(c3.output), c3.output
assert r3.output.endswith("Full marks!\nPass\n") and r4a.output.endswith("75\nPass\n") and r4b.output.endswith("Full marks!\nPass\n")
cmp = rc.output.split()
assert cmp == ["0", "1", "0", "1", "1", "1"], cmp
assert all(r.code == 0 for r in (c1, c2, c3, c4, cch)) and rch.output.endswith("Odd\n")

TF = {"0": "false (0)", "1": "true (1)"}
SAY = {"==": "兩個等號", "!=": "感嘆號等號", ">=": "大過或等於", "<=": "細過或等於", "mark = 100": "mark 等如一百",
       "Full marks": "Full marks", "else": "else", "if": "if"}

s = Stage({"pass.cpp": V0}, title="if / else")

scenes = [
    Scene("intro",
          "歡迎嚟到第二章：流程控制！到目前為止，程式都係由上至下，一句一句咁行。今集學 if，等程式識得做決定。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "if · else · == != < > <= >=")),
    Scene("goal",
          "今集會講：[[b1]]if 同 else；[[b2]]六個比較運算子；[[b3]]一個好多人中過嘅陷阱：一個等號同兩個等號。",
          BulletCard("今集學識", [("if 同 else", "b1"), ("六個比較運算子", "b2"), ("陷阱：= 同 ==", "b3")])),
    Scene("if1",
          "[[open]]呢個程式讀入一個分數。[[if]]if 後面嘅括號入面係條件：分數大過或等於五十。"
          "[[body]]條件成立，就會行大括號入面嘅嘢：印出 Pass。",
          s.scene(Open("pass.cpp", mode="instant", at="open"), Type("pass.cpp", IF.splitlines(True)[0], before="}", last=True, at="if"),
                  Type("pass.cpp", "".join(IF.splitlines(True)[1:]), before="}", last=True, at="body"), Expect("pass.cpp", V1))),
    Scene("run1",
          "[[cc]]編譯運行，[[t1]]輸入七十五，[[o1]]印出 Pass。[[t2]]再試三十：[[o2]]乜都冇印，因為條件唔成立，大括號入面成段跳過。",
          s.scene(Run(c1, at="cc"), Run(r1a, keys=("t1",)), Run(r1b, at="t2", recall=True, keys=(("t2", 1.0),)))),
    Scene("else",
          "唔合格都想印句嘢，[[type]]就加 else：條件唔成立嘅時候，就會行 else 嗰段。[[cc]]編譯運行，[[t]]輸入三十，[[o]]今次印出 Fail。",
          s.scene(Type("pass.cpp", ELSE, after="        std::cout << \"Pass\\n\";\n    }", at="type"), Expect("pass.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("t",)))),
    Scene("fork",
          "所以 if 同 else 就好似一個分岔路口：[[yes]]條件成立，行 if 嗰段；[[no]]唔成立，就行 else 嗰段。"
          "[[one]]兩段之中，一定會行一段，亦都只會行一段。",
          TileCard("if / else：分岔路口", [
              Tile("✅", "條件成立 true", "行 if 嘅大括號\nmark >= 50 → Pass", "yes", GREEN),
              Tile("❌", "條件唔成立 false", "行 else 嘅大括號\n否則 → Fail", "no", RED),
          ], cols=2, height=360, footer=("一定行一段，亦只會行一段", "one"))),
    Scene("ops",
          "條件入面可以用六個比較運算子：[[eq]]兩個等號，比較係咪相等；[[ne]]感嘆號等號，即係唔等於；"
          "[[lt]]細過同大過；[[le]]仲有細過或等於，同大過或等於。結果唔係 true，就係 false。",
          TableCard("比較運算子", ["運算子", "意思", "例子", "結果"], [
              (["==", "等於", "75 == 50", TF[cmp[0]]], "eq"),
              (["!=", "唔等於", "75 != 50", TF[cmp[1]]], "ne"),
              (["<", "細過", "75 < 50", TF[cmp[2]]], "lt"),
              ([">", "大過", "75 > 50", TF[cmp[3]]], ("lt", 0.5)),
              (["<=", "細過或等於", "75 <= 75", TF[cmp[4]]], "le"),
              ([">=", "大過或等於", "75 >= 50", TF[cmp[5]]], ("le", 0.6)),
          ], widths=[0.7, 1.2, 1, 1], code_cols=(0, 2, 3), size=40)),
    Scene("bug",
          "而家加一個功能：滿分就印 Full marks。[[type]]if，mark 等如一百……[[cc]]編譯，[[warn]]g++ 有個警告，不過我哋照運行："
          "[[t]]輸入七十五，[[o]]竟然話滿分！",
          s.scene(Run(clr), Type("pass.cpp", FULL.replace("==", "="), after="std::cin >> mark;\n", at="type"), Expect("pass.cpp", BUG),
                  Run(c3, at="cc", recall=True), Run(r3, recall=True, keys=("t",)),
                  Note("75 分都係滿分？", at="o", where="editor"))),
    Scene("bug_why",
          "因為一個等號唔係比較，而係賦值：[[assign]]mark = 100，將一百放入 mark，[[true]]而一百唔係零，就當係 true。"
          "所以條件永遠成立，連 mark 都俾我哋改咗做一百。[[warn]]g++ 嘅警告，其實就係問你：你係咪想用賦值做條件？",
          s.scene(Note(None), Mark(7, at="assign"), Note("mark = 100：放入 100\n非零 → 當 true", at="assign", where="editor"))),
    Scene("fix",
          "[[fix]]比較一定要用兩個等號。[[cc]]再編譯，[[t1]]輸入七十五，[[o1]]淨係 Pass；[[t2]]輸入一百，[[o2]]先係滿分。今次啱晒。",
          s.scene(Note(None), Replace("pass.cpp", "mark = 100", "mark == 100", at="fix"), Mark(None), Expect("pass.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4a, recall=True, keys=("t1",)), Run(r4b, at="t2", recall=True, keys=(("t2", 1.0),)))),
    Scene("recap",
          "總結：[[r1]]if 條件成立，先行大括號入面嘅嘢；[[r2]]else 處理唔成立嘅情況；[[r3]]六個比較運算子；"
          "[[r4]]比較用兩個等號，一個等號係賦值，記住開 -Wall 等 g++ 提你。",
          BulletCard("今集重點", [("if：條件成立先行", "r1"), ("else：唔成立就行呢段", "r2"),
                                ("== != < > <= >=", "r3"), ("比較用 ==；= 係賦值", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一個整數，用百分號判斷佢係單數定雙數，印出 Odd 或者 Even。"
          "[[next]]下一集，我哋學點樣用且、或、非，組合幾個條件。多謝收睇，下次見！",
          EndCard("讀入一個整數，用 % 判斷佢係單數定雙數，印出 Odd 或者 Even。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

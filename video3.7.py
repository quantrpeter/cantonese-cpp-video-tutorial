#!/usr/bin/env python3
"""Video 36 (syllabus 3.7): 預設參數同多載

3.1's printLine with default arguments (three ways to call it); a default that is not at the
right end is a real error; area() overloaded for squares and rectangles; adding a default to the
second area makes area(5) a real "ambiguous" error. Run `python3 video3.7.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 36
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-07"
LINE = (CODE / "line.cpp").read_text()
AREA = (CODE / "area.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LBAD = LINE.replace("char ch = '-'", "char ch")
ABAD = AREA.replace("int width, int height)", "int width, int height = 1)")
CL = "g++ -std=c++20 -Wall -Wextra line.cpp -o line"
CA = "g++ -std=c++20 -Wall -Wextra area.cpp -o area"

(c1, r1, c2, clr, c3, r3, c4, cch, rch) = cpp.session({"line.cpp": LINE, "area.cpp": AREA}, [
    CL, "./line", Write("line.cpp", LBAD), CL, Write("line.cpp", LINE),
    "clear", CA, "./area", Write("area.cpp", ABAD), CA, Write("area.cpp", AREA),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "-" * 20 + "\n" + "-" * 10 + "\n" + "*" * 10 + "\n"
assert "default argument missing for parameter 2" in cpp.visible(c2.output), c2.output
assert r3.output.split() == ["25", "24"]
assert "call of overloaded 'area(int)' is ambiguous" in cpp.visible(c4.output), c4.output
assert c1.code == c3.code == cch.code == 0 and rch.output.split() == ["8", "8"]

SAY = {"printLine": "print line", "area(5)": "area 五", "area(4, 6)": "area 四、六", "overload": "overload"}

s = Stage({"line.cpp": LINE, "area.cpp": AREA}, title="預設參數同多載")

scenes = [
    Scene("intro",
          "歡迎返嚟！今集學兩樣令函數更加方便嘅嘢：預設參數，同埋函數多載。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "default argument · overload")),
    Scene("goal",
          "今集會講：[[b1]]預設參數：唔傳就用預設值；[[b2]]函數多載：同一個名，唔同參數；[[b3]]兩樣撞埋會出咩問題。",
          BulletCard("今集學識", [("預設參數 default argument", "b1"), ("函數多載 overload", "b2"), ("兩樣撞埋：歧義", "b3")])),
    Scene("defaults",
          "[[open]]記得 3.1 嘅 printLine？今次佢有兩個參數：長度同字元。[[def]]參數後面加等號同一個值，就係預設值："
          "呼叫嗰陣唔傳，就用呢個值。[[calls]]main 入面有三種叫法：乜都唔傳；淨係傳長度；兩個都傳。",
          s.scene(Open("line.cpp", at="open"), Mark(3, at="def"), Mark((11, 13), at="calls"))),
    Scene("run1",
          "[[cc]]編譯運行。[[o]]第一行二十個橫線，用晒兩個預設值；第二行十個橫線；第三行十個星號。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1))),
    Scene("rule",
          "預設參數有一條規則。[[rm]]如果刪走右邊字元嘅預設值，淨係留低左邊長度嗰個，[[cc]]編譯，[[err]]就會出錯：第二個參數冇預設值。"
          "[[why]]因為預設參數一定要由最右邊開始，中間唔可以跳過。[[undo]]改返。",
          s.scene(Replace("line.cpp", "char ch = '-'", "char ch", at="rm"), Expect("line.cpp", LBAD),
                  Run(c2, at="cc", recall=True), Note("預設值要由最右邊開始", at="why", where="editor"),
                  Replace("line.cpp", "char ch)", "char ch = '-')", at="undo"), Expect("line.cpp", LINE))),
    Scene("overload",
          "另一樣係多載。[[open]]兩個函數可以用同一個名，只要參數唔同：[[one]]area 一個參數，計正方形；[[two]]兩個參數，計長方形。"
          "[[cc]]編譯運行，[[o]]二十五同二十四：編譯器睇你傳咗幾多個、咩型別嘅參數，自動揀啱嗰個。",
          s.scene(Note(None), Run(clr, at="open"), Open("area.cpp", at="open"), Mark((3, 5), at="one"), Mark((7, 9), at="two"),
                  Mark(None, at="cc"), Run(c3, at="cc"), Run(r3))),
    Scene("pick",
          "[[a]]area(5) 得一個 int，就揀正方形嗰個；[[b]]area(4, 6) 有兩個 int，就揀長方形嗰個。",
          TableCard("編譯器揀邊個？", ["呼叫", "揀中", "結果"], [
              (["area(5)", "int area(int side)", r3.output.split()[0]], "a"),
              (["area(4, 6)", "int area(int width, int height)", r3.output.split()[1]], "b"),
          ], widths=[0.8, 2, 0.5], code_cols=(0, 1, 2), size=40)),
    Scene("ambiguous",
          "如果兩樣撞埋：[[def]]喺長方形嗰個 area，加個預設值：height 等於一。[[cc]]編譯，[[err]]出錯：area(5) 有歧義。"
          "[[why]]因為而家兩個 area 都可以只收一個參數，編譯器唔知揀邊個。[[undo]]刪走個預設值就得。",
          s.scene(Replace("area.cpp", "int width, int height)", "int width, int height = 1)", at="def"), Expect("area.cpp", ABAD),
                  Run(c4, at="cc", recall=True), Note("兩個都啱：唔知揀邊個\n＝ ambiguous 歧義", at="why", where="editor"),
                  Replace("area.cpp", "int height = 1)", "int height)", at="undo"), Expect("area.cpp", AREA))),
    Scene("rules",
          "記住幾條規則：[[r1]]預設值由最右邊開始；[[r2]]多載：同一個名，參數嘅數量或者型別唔同；"
          "[[r3]]淨係回傳型別唔同，唔算多載；[[r4]]小心預設參數同多載撞埋，產生歧義。",
          BulletCard("規則", [("預設值：由右邊開始", "r1"), ("多載：同名，參數唔同", "r2"),
                            ("淨係回傳型別唔同：唔算", "r3"), ("小心歧義 ambiguous", "r4")])),
    Scene("recap",
          "總結：[[r1]]預設參數令呼叫可以少傳幾個值；[[r2]]多載令同一個名做相似嘅嘢；[[r3]]編譯器根據參數揀啱嗰個函數，揀唔到就係歧義。",
          BulletCard("今集重點", [("預設參數：少傳幾個", "r1"), ("多載：同名做相似嘅嘢", "r2"), ("揀唔到：ambiguous", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]寫兩個同名嘅函數 biggest：一個揀兩個數入面大嗰個，一個揀三個數入面最大嗰個。"
          "[[next]]下一集，我哋講作用域同生命週期。多謝收睇，下次見！",
          EndCard("寫兩個同名函數 biggest：一個比較兩個 int，一個比較三個 int。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

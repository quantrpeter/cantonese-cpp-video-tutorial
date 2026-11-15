#!/usr/bin/env python3
"""Video 32 (syllabus 3.3): 宣告同定義

main first and the functions below it is a real "'square' was not declared in this scope";
prototypes fix it; declaration vs definition; a misspelt definition (sqare) is a real linker
error, "undefined reference to `square(int)'". Run `python3 video32.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 32
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-03"
FINAL = (CODE / "order.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
DECL = "int square(int x);\nint cube(int x);\n\n"
BAD = FINAL.replace(DECL, "")
TYPO = FINAL.replace("int square(int x) {", "int sqare(int x) {")
CC = "g++ -std=c++20 -Wall -Wextra order.cpp -o order"

(c1, c2, r2, c3, cch, rch) = cpp.session({"order.cpp": BAD}, [
    CC, Write("order.cpp", FINAL), CC, "./order", Write("order.cpp", TYPO), CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "'square' was not declared in this scope" in cpp.visible(c1.output) and c1.code != 0
assert r2.output.split() == ["49", "27"] and c2.code == 0
assert "undefined reference to `square(int)'" in cpp.visible(c3.output) and "ld returned 1" in cpp.visible(c3.output)
assert cch.code == 0 and rch.output.split() == ["9", "3", "18"]

SAY = {"square(7)": "square 七", "cube(3)": "cube 三", "sqare": "S Q A R E", "ld": "L D",
       "undefined reference": "undefined reference", "int square(int x);": "int square int x"}

s = Stage({"order.cpp": BAD}, title="宣告同定義", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！之前我哋一直將函數寫喺 main 上面。如果想 main 放喺最頂，一打開檔案就睇到程式做乜，得唔得？今集講宣告同定義。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "宣告 declaration · 定義 definition")),
    Scene("goal",
          "今集會講：[[b1]]點解函數嘅次序有關係；[[b2]]函數原型，即係宣告；[[b3]]宣告同定義嘅分別；[[b4]]連結錯誤 undefined reference。",
          BulletCard("今集學識", [("次序點解有關係", "b1"), ("函數原型 prototype", "b2"), ("宣告 vs 定義", "b3"),
                                ("undefined reference", "b4")])),
    Scene("bad",
          "[[open]]今次 main 放喺最頂，square 同 cube 放喺下面；cube 仲會用到 square。[[cc]]編譯，[[err]]出錯：square 同 cube 都未宣告。",
          s.scene(Open("order.cpp", at="open"), Mark((3, 6), at=("open", 1.0)), Mark((8, 14), at=("open", 3.0)), Mark(None, at="cc"),
                  Run(c1, at="cc"))),
    Scene("why",
          "因為編譯器由上至下讀。[[main]]讀到 main 入面嘅 square(7) 嗰陣，[[unk]]佢仲未見過 square，唔知佢收咩參數、回傳咩，"
          "就唔肯繼續。[[later]]就算下面有定義，都已經遲咗。",
          FlowCard("編譯器由上至下讀", [Row("讀", "第 1 行起", RED, [
              Node("int main()", "第 3 行", "main"), Node("square(7)", "第 4 行：乜嘢嚟？", "unk"),
              Node("int square…", "第 8 行：遲咗", "later"),
          ], note="用之前，一定要俾編譯器見過", note_at="later")])),
    Scene("decl",
          "解決方法：[[type]]喺 main 上面加兩句宣告。[[proto]]宣告只寫回傳型別、名同參數，冇大括號，以分號結尾，叫做函數原型。"
          "意思係話俾編譯器聽：有呢個函數，詳細點做，後面先寫。[[cc]]編譯運行，[[o]]四十九同二十七。",
          s.scene(Type("order.cpp", DECL, after="#include <iostream>\n\n", at="type", rate=20), Expect("order.cpp", FINAL),
                  Mark((3, 4), at="proto"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("table",
          "比較一下：[[d1]]宣告講個函數係乜樣：名、參數、回傳型別，冇大括號，分號結尾；[[d2]]定義就係真正嘅內容，有大括號。"
          "[[rule]]宣告可以寫幾多次都得，但係定義只可以有一個。",
          TableCard("宣告 vs 定義", ["", "寫法", "作用"], [
              (["宣告", "int square(int x);", "話俾編譯器知有呢個函數"], "d1"),
              (["定義", "int square(int x) { … }", "真正嘅內容（只可以有一個）"], "d2"),
          ], widths=[0.6, 1.5, 1.6], code_cols=(1,), size=40, note=("宣告可以有幾次；定義只可以有一次", "rule"))),
    Scene("link",
          "另一個常見錯誤：[[typo]]定義嗰度，square 打錯咗做 sqare。[[cc]]編譯，[[err]]今次嘅錯誤好唔同：undefined reference，"
          "[[ld]]而且唔係編譯器講，而係連結器 ld 講。意思係：宣告咗 square，但係成個程式都搵唔到佢嘅定義。",
          s.scene(Mark(None), Replace("order.cpp", "int square(int x) {", "int sqare(int x) {", at="typo"),
                  Expect("order.cpp", TYPO), Run(c3, at="cc", recall=True),
                  Note("ld：連結器\n宣告咗，但搵唔到定義", at="ld", where="editor"))),
    Scene("link2",
          "[[two]]C++ 程式係分兩步整：先編譯，再連結。編譯只需要宣告；連結嘅時候，先至要搵到真正嘅定義。第十章會再詳細講。"
          "[[fix]]改返個名就得。",
          s.scene(Note("編譯：見到宣告就得\n連結：要搵到定義", at="two", where="editor"), Note(None, at="fix"),
                  Replace("order.cpp", "int sqare(int x) {", "int square(int x) {", at="fix"), Expect("order.cpp", FINAL))),
    Scene("recap",
          "總結：[[r1]]函數用之前，編譯器一定要見過佢；[[r2]]宣告，即係函數原型，以分號結尾；[[r3]]定義有大括號，只可以有一個；"
          "[[r4]]搵唔到定義，連結器就會報 undefined reference。",
          BulletCard("今集重點", [("用之前要見過：宣告或者定義", "r1"), ("原型：int square(int x);", "r2"),
                                ("定義：有 { }，只可以一個", "r3"), ("undefined reference：搵唔到定義", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫 add、subtract 同 multiply 三個函數，main 放喺最頂，用宣告令個程式編譯到。"
          "[[next]]下一集，我哋睇吓參數其實係一個副本。多謝收睇，下次見！",
          EndCard("寫 add、subtract、multiply 三個函數，main 放喺最頂，用宣告令個程式編譯到。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

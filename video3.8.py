#!/usr/bin/env python3
"""Video 37 (syllabus 3.8): 作用域同生命週期

The loop variable i used after its loop is a real "'i' was not declared in this scope"; a visit
counter with a local count really prints "Visit #1" three times; a global fixes it but anyone can
change it; a static local is the clean fix. Run `python3 video3.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 37
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-08"
SCOPE = (CODE / "scope.cpp").read_text()
COUNT = (CODE / "count.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SBAD = SCOPE.replace("std::cout << total << '\\n';", "std::cout << total << ' ' << i << '\\n';")
STATIC = "    static int count = 0;\n"
GLOBAL = "int count = 0;\n\n"
LOCAL = COUNT.replace(STATIC, "    int count = 0;\n")
GLOB = COUNT.replace(STATIC, "").replace("void visit", GLOBAL + "void visit")
CS = "g++ -std=c++20 -Wall -Wextra scope.cpp -o scope"
CC = "g++ -std=c++20 -Wall -Wextra count.cpp -o count"

(s1, s2, rs, clr, c1, r1, c2, r2, c3, r3, cch, rch) = cpp.session({"scope.cpp": SBAD, "count.cpp": LOCAL}, [
    CS, Write("scope.cpp", SCOPE), CS, "./scope",
    "clear", CC, "./count", Write("count.cpp", GLOB), CC, "./count", Write("count.cpp", COUNT), CC, "./count",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "'i' was not declared in this scope" in cpp.visible(s1.output) and rs.output.strip() == "6"
assert r1.output == "Visit #1\n" * 3 and r2.output == r3.output == "Visit #1\nVisit #2\nVisit #3\n"
assert s2.code == c1.code == c2.code == c3.code == cch.code == 0 and rch.output.split() == ["1", "2", "3"]

SAY = {"static": "static", "count": "count", "visit": "visit", "Visit #1": "Visit 一號"}

s = Stage({"scope.cpp": SBAD, "count.cpp": LOCAL}, title="作用域同生命週期")

scenes = [
    Scene("intro",
          "歡迎返嚟！一個變數喺邊度用得？幾時出世、幾時消失？今集講作用域同生命週期。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "scope · lifetime · static")),
    Scene("goal",
          "今集會講：[[b1]]作用域：變數喺邊度用得；[[b2]]生命週期：變數幾時出世、幾時消失；[[b3]]全域變數點解唔好用；[[b4]]static 局部變數。",
          BulletCard("今集學識", [("作用域 scope", "b1"), ("生命週期 lifetime", "b2"), ("全域變數嘅問題", "b3"),
                                ("static 局部變數", "b4")])),
    Scene("scope",
          "[[open]]呢個迴圈將一、二、三加埋，最後想印埋 i 出嚟。[[cc]]編譯，[[err]]出錯：i 未宣告？"
          "[[why]]因為 i 喺 for 入面宣告，佢嘅作用域只係個迴圈；迴圈一完，i 就唔存在。",
          s.scene(Open("scope.cpp", at="open"), Mark(8, at=("open", 1.2)), Mark(None, at="cc"), Run(s1, at="cc"),
                  Mark((5, 7), at="why"), Note("i 嘅作用域：只係 for 入面", at="why", where="editor"))),
    Scene("blocks",
          "記住呢條規則：[[outer]]喺大括號入面宣告嘅變數，只喺嗰對大括號入面用得。total 喺 main 嘅大括號入面，成個 main 都用得；"
          "[[inner]]i 喺 for 入面，就只係迴圈用得。",
          CodeCard("每對大括號：一個作用域", SBAD, "scope.cpp", marks=[
              ((4, 9), "total：成個 main", "outer", BLUE), ((5, 7), "i：淨係 for", "inner", AMBER)], size=34)),
    Scene("fix",
          "[[fix]]所以喺迴圈外面，唔可以再用 i。刪走佢，[[cc]]再編譯運行，[[o]]總數係六。",
          s.scene(Note(None), Mark(None), Replace("scope.cpp", " << ' ' << i", "", at="fix"), Expect("scope.cpp", SCOPE),
                  Run(s2, at="cc", recall=True), Run(rs))),
    Scene("local",
          "跟住講生命週期。[[open]]visit 每次被呼叫，就印出係第幾次探訪。[[local]]count 係函數入面嘅局部變數。"
          "[[cc]]編譯運行，[[o]]三次都話係第一次！count 好似完全記唔住之前嘅數。",
          s.scene(Run(clr, at="open"), Open("count.cpp", at="open"), Mark(4, at="local"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1), Note("三次都係 #1？", at="o", where="editor"))),
    Scene("lifetime",
          "因為局部變數嘅生命好短：[[born]]每次呼叫 visit，count 就重新出世，由零開始；[[inc]]加一，印出一；"
          "[[die]]函數一完，count 就消失。下一次呼叫，又由零開始。",
          TableCard("每次呼叫 visit()", ["呼叫", "count 出世", "count++", "印出", "函數完"], [
              (["第 1 次", "0", "1", "#1", "count 消失"], "born"),
              (["第 2 次", "0", "1", "#1", "count 消失"], "inc"),
              (["第 3 次", "0", "1", "#1", "count 消失"], "die"),
          ], widths=[0.8, 0.9, 0.8, 0.6, 1.1], code_cols=(1, 2, 3), size=38)),
    Scene("global",
          "[[move]]將 count 搬出函數外面，變成全域變數。[[cc]]運行，[[o]]一、二、三，啱咗。[[but]]不過全域變數喺邊度都改得，"
          "程式一大，就好難知道係邊個改咗佢，出錯好難搵，所以盡量唔好用。",
          s.scene(Note(None), Replace("count.cpp", "    int count = 0;\n", "", at="move"), Type("count.cpp", GLOBAL, before="void visit"),
                  Expect("count.cpp", GLOB), Run(c2, at="cc", recall=True), Run(r2),
                  Note("全域變數：邊度都改得\n出錯好難搵", at="but", where="editor"))),
    Scene("static",
          "更好嘅做法：[[back]]搬返入函數，[[st]]前面加 static。static 局部變數只會初始化一次，函數完咗都唔會消失，"
          "但係只有呢個函數用得。[[cc]]運行，[[o]]一、二、三，而且冇其他人改得到。",
          s.scene(Note(None), Replace("count.cpp", GLOBAL, "", at="back"), Type("count.cpp", STATIC, after="void visit() {\n"),
                  Expect("count.cpp", COUNT), Mark(4, at="st"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("table",
          "比較三種變數：[[l]]局部變數，只喺自己嘅大括號入面用得，離開就消失；[[g]]全域變數，邊度都用得，程式完先消失；"
          "[[st]]static 局部變數，只喺函數入面用得，但係一直保留到程式完。",
          TableCard("三種變數", ["種類", "邊度用得", "幾時消失"], [
              (["局部", "自己嘅 { } 入面", "離開 { } 就消失"], "l"),
              (["全域", "成個程式（危險）", "程式完先消失"], "g", RED),
              (["static 局部", "自己嘅函數入面", "程式完先消失"], "st", GREEN),
          ], widths=[0.9, 1.4, 1.3], size=40)),
    Scene("recap",
          "總結：[[r1]]變數嘅作用域，係宣告佢嗰對大括號；[[r2]]局部變數每次都重新出世，離開就消失；[[r3]]全域變數邊度都改得，盡量避免；"
          "[[r4]]要記住上一次嘅值，就用 static 局部變數。",
          BulletCard("今集重點", [("作用域：宣告佢嗰對 { }", "r1"), ("局部變數：每次重新出世", "r2"),
                                ("避免全域變數", "r3"), ("記住上次嘅值：static", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數 nextTicket，每次呼叫，就回傳下一個籌號：一、二、三。"
          "[[next]]下一集，我哋學遞迴：函數呼叫自己。多謝收睇，下次見！",
          EndCard("寫一個函數 nextTicket()，每次呼叫回傳下一個籌號：1、2、3……",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

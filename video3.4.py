#!/usr/bin/env python3
"""Video 33 (syllabus 3.4): 傳值

addOne(score) prints 11 inside but score is really still 10 outside: the parameter is a copy
(shown as two boxes); returning the new value and assigning it fixes it.
Run `python3 video3.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 33
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-04"
FINAL = (CODE / "add.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
INSIDE = "    std::cout << \"Inside: \" << n << '\\n';\n"
V1 = (FINAL.replace("int addOne", "void addOne").replace("    return n;\n", INSIDE)
      .replace("    score = addOne(score);", "    addOne(score);"))
CC = "g++ -std=c++20 -Wall -Wextra add.cpp -o add"

(c1, r1, c2, r2, cch, rch) = cpp.session({"add.cpp": V1}, [
    CC, "./add", Write("add.cpp", FINAL), CC, "./add",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Inside: 11\nOutside: 10\n" and r2.output == "Outside: 11\n"
assert c1.code == c2.code == cch.code == 0 and rch.output.strip() == "42"

SAY = {"addOne": "add one", "addOne(score)": "add one score", "score = addOne(score)": "score 等如 add one score",
       "pass by value": "pass by value", "Inside": "Inside", "Outside": "Outside"}

s = Stage({"add.cpp": V1}, title="傳值")

scenes = [
    Scene("intro",
          "歡迎返嚟！寫一個將分數加一嘅函數，好簡單啩？今集你會見到，結果同你諗嘅唔一樣。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "pass by value · 副本")),
    Scene("goal",
          "今集會講：[[b1]]傳值：參數其實係一個副本；[[b2]]點解函數改唔到外面嘅變數；[[b3]]用 return 交返新嘅值。",
          BulletCard("今集學識", [("傳值 pass by value", "b1"), ("函數改唔到外面嘅變數", "b2"), ("用 return 交返新值", "b3")])),
    Scene("run1",
          "[[open]]addOne 將 n 加一，再印出嚟。[[main]]main 有個 score，係十，交俾 addOne，之後再印一次 score。"
          "[[cc]]編譯運行，[[o1]]入面印十一，[[o2]]但係出返嚟，score 仲係十！",
          s.scene(Open("add.cpp", at="open"), Mark((3, 6), at=("open", 0.8)), Mark((9, 11), at="main"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1), Note("入面 11，出面仲係 10？", at="o2", where="editor"))),
    Scene("boxes",
          "原因係：[[call]]呼叫 addOne(score) 嘅時候，C++ 將 score 嘅值複製一份，[[copy]]放入參數 n。"
          "[[inc]]函數改嘅係 n 呢個副本；[[same]]main 嘅 score 由頭到尾冇郁過。",
          BoxesCard("參數係副本", [
              BoxRow([Box("score", "10", "int", at="call", w=300)], label="main"),
              BoxRow([Box("n", [("10", "copy"), ("11", "inc")], "副本", at="copy", color=AMBER, w=300)], label="addOne"),
          ], arrows=[("score", "n", "copy")], top=CONTENT_TOP + 40, row_h=280, box_h=130, size=60,
              notes=[("n = n + 1：改嘅係副本；score 冇郁過", "same")])),
    Scene("why",
          "呢個叫傳值，pass by value。[[good]]好處係安全：函數唔會偷偷改咗你嘅變數；[[bad]]壞處係，真係想改嘅時候，就改唔到。",
          TileCard("傳值 pass by value", [
              Tile("🛡️", "好處：安全", "函數只係攞到副本\n唔會亂改你嘅變數", "good", GREEN),
              Tile("⚠️", "壞處：改唔到", "想改外面嘅變數\n就要另外諗辦法", "bad", AMBER),
          ], cols=2, height=360)),
    Scene("fix",
          "一個簡單嘅辦法：[[ret]]將函數改成回傳新嘅值：回傳型別改做 int，最後 return n。"
          "[[assign]]喺 main 入面，用 score 等於 addOne(score)，將結果放返入 score。",
          s.scene(Note(None), Replace("add.cpp", "void addOne", "int addOne", at="ret"), Replace("add.cpp", INSIDE, "    return n;\n"),
                  Replace("add.cpp", "    addOne(score);", "    score = addOne(score);", at="assign"), Expect("add.cpp", FINAL))),
    Scene("run2",
          "[[cc]]編譯運行，[[o]]今次 score 係十一。[[note]]另一個方法係 reference，下兩集會講，到時就可以寫一個真正交換兩個變數嘅 swap。",
          s.scene(Run(c2, at="cc", recall=True), Run(r2), Note("用 return 交返新值\n再放返入 score", at="o", where="editor"))),
    Scene("recap",
          "總結：[[r1]]傳值嘅參數係一個副本；[[r2]]函數改副本，唔會影響外面嘅變數；[[r3]]想交返結果，就用 return，再放返入變數。",
          BulletCard("今集重點", [("參數係副本 copy", "r1"), ("改副本，外面唔受影響", "r2"), ("用 return 交返新值", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數 doubled，回傳一個數嘅兩倍，喺 main 用佢將一個變數變成兩倍。"
          "[[next]]下一集，我哋學 reference：一個變數嘅第二個名。多謝收睇，下次見！",
          EndCard("寫一個函數 doubled(x) 回傳 x 嘅兩倍，喺 main 用佢將一個變數變成兩倍。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 30 (syllabus 3.1): 點解要用函數

A banner with the same separator line written three times; changing it by hand misses one, for
real; printLine() makes it one place to change; a call without () is a real -Waddress warning
and the line really goes missing. Run `python3 video3.1.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 30
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-01"
FINAL = (CODE / "line.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
STAR, EQ, DASH = "*" * 20, "=" * 20, "-" * 20
FUNC = f"void printLine() {{\n    std::cout << \"{STAR}\\n\";\n}}\n\n"
CALL = "    printLine();\n"
V1 = FINAL.replace(STAR, EQ)
V0 = V1.replace(FUNC.replace(STAR, EQ), "").replace(CALL, f"    std::cout << \"{DASH}\\n\";\n")
DASH_L, EQ_L = f"    std::cout << \"{DASH}\\n\";\n", f"    std::cout << \"{EQ}\\n\";\n"
V0B = V0.replace(DASH_L, EQ_L, 2)
NOPAREN = FINAL.replace(CALL + "    std::cout << \"  Lesson", "    printLine;\n    std::cout << \"  Lesson")
CC = "g++ -std=c++20 -Wall -Wextra line.cpp -o line"

(c0, r0, cb, rb, c1, r1, c2, r2, c3, r3, cch, rch) = cpp.session({"line.cpp": V0}, [
    CC, "./line", Write("line.cpp", V0B), CC, "./line",
    Write("line.cpp", V1), CC, "./line",
    Write("line.cpp", FINAL), CC, "./line",
    Write("line.cpp", NOPAREN), CC, "./line",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert rb.output.split("\n")[0] == EQ and rb.output.split("\n")[4] == DASH, rb.output
assert r1.output.count(EQ) == 3 and r2.output.count(STAR) == 3
assert "statement is a reference, not call, to function 'printLine'" in cpp.visible(c3.output), c3.output
assert r3.output.count(STAR) == 2 and rch.output.count("Hello") == 2
assert all(r.code == 0 for r in (c0, cb, c1, c2, c3, cch))

SAY = {"printLine()": "print line", "printLine": "print line", "void": "void"}

s = Stage({"line.cpp": V0}, title="點解要用函數")

scenes = [
    Scene("intro",
          "歡迎嚟到第三章：函數！程式越寫越長，好多嘢會重複。函數可以將一堆指令包成一個有名嘅動作，要用嘅時候叫佢一聲就得。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "定義 · 呼叫 · void")),
    Scene("goal",
          "今集會講：[[b1]]點解要用函數；[[b2]]點樣定義同呼叫一個函數；[[b3]]void 係乜意思。",
          BulletCard("今集學識", [("點解要用函數 function", "b1"), ("定義同呼叫", "b2"), ("void：唔回傳嘢", "b3")])),
    Scene("repeat",
          "[[open]]呢個程式印一個標題框，分隔線一模一樣，寫咗三次。[[cc]]編譯運行，[[o]]印出一個標題框，暫時冇問題。",
          s.scene(Open("line.cpp", at="open"), Mark(4, at=("open", 1.2)), Mark(6, at=("open", 1.6)), Mark(8, at=("open", 2.0)),
                  Mark(None, at="cc"), Run(c0, at="cc"), Run(r0))),
    Scene("miss",
          "而家想將分隔線改做等號。[[e1]]改第一條，[[e2]]改第二條……[[cc]]運行，[[o]]咦，最後一條唔記得改！"
          "同一樣嘢寫幾次，改嘅時候就好容易漏。",
          s.scene(Replace("line.cpp", DASH_L, EQ_L, at="e1"), Replace("line.cpp", DASH_L, EQ_L, at="e2"), Expect("line.cpp", V0B),
                  Run(cb, at="cc", recall=True), Run(rb), Note("最後一條漏咗改！", at="o", where="editor"))),
    Scene("define",
          "用函數就唔會。[[def]]喺 main 上面，定義一個函數：void printLine，[[body]]大括號入面，就係佢要做嘅嘢：印一條分隔線。"
          "[[call]]然後喺 main 入面，三個地方都改成 printLine 加括號，即係呼叫佢。",
          s.scene(Note(None), Type("line.cpp", FUNC.replace(STAR, EQ), after="#include <iostream>\n\n", at="def", rate=20),
                  Replace("line.cpp", EQ_L, CALL, at="call", last=True), Replace("line.cpp", EQ_L, CALL, last=True),
                  Replace("line.cpp", DASH_L, CALL),
                  Expect("line.cpp", V1))),
    Scene("anatomy",
          "[[void]]void 意思係呢個函數做完嘢，唔會交返任何值出嚟；[[name]]printLine 係函數嘅名；[[paren]]括號入面放參數，今次冇，下集再講；"
          "[[body]]大括號入面係函數嘅內容。",
          AnatomyCard("定義一個函數", [
              Part("void", "唔回傳值", PURPLE, "void"),
              Part(" printLine", "函數名", BLUE, "name"),
              Part("()", "參數（下集講）", AMBER, "paren"),
              Part(" { … }", "做嘅嘢", GREEN, "body"),
          ], size=84)),
    Scene("run1",
          "[[cc]]編譯運行，[[o]]三條等號線，全部一致。[[change]]而家再改做星號，[[edit]]只要改函數入面一個地方，"
          "[[run]]三條線就一齊變。",
          s.scene(Run(c1, at="cc", recall=True), Run(r1), Replace("line.cpp", EQ, STAR, at="edit"), Expect("line.cpp", FINAL),
                  Run(c2, at="run", recall=True), Run(r2))),
    Scene("flow",
          "呼叫函數嘅時候，[[go]]程式會跳去函數嗰度，[[do]]由頭行到尾，[[back]]行完再跳返嚟，繼續 main 嘅下一句。",
          FlowCard("呼叫函數：跳去，再返嚟", [Row("main", "由上至下", BLUE, [
              Node("printLine();", "跳去函數", "go"), Node("printLine", "印一條線", "do"),
              Node("返嚟 main", "行下一句", "back"),
          ], note="每次呼叫，都會由頭行一次函數", note_at="back")])),
    Scene("noparen",
          "常見錯誤：[[del]]唔記得括號。[[cc]]編譯，[[warn]]g++ 警告：呢句只係提到個函數，冇呼叫佢。[[run]]運行，[[o]]真係少咗一條線。"
          "[[fix]]呼叫函數，一定要有括號。",
          s.scene(Replace("line.cpp", CALL + "    std::cout << \"  Lesson", "    printLine;\n    std::cout << \"  Lesson", at="del"),
                  Expect("line.cpp", NOPAREN), Run(c3, at="cc", recall=True), Run(r3, at="run"),
                  Note("冇括號：冇呼叫到！", at="o", where="editor"),
                  Type("line.cpp", "()", before=";\n    std::cout << \"  Lesson", at="fix"), Expect("line.cpp", FINAL),
                  Note(None, at="fix"))),
    Scene("why",
          "函數有幾個好處：[[w1]]唔使重複寫同一段嘢；[[w2]]要改，只改一個地方；[[w3]]有個好名，main 讀落似一份清單；"
          "[[w4]]仲可以逐個函數分開測試。",
          BulletCard("點解要用函數？", [("唔使重複", "w1"), ("要改，只改一個地方", "w2"), ("有名：main 易讀", "w3"),
                                     ("可以分開測試", "w4")])),
    Scene("recap",
          "總結：[[r1]]函數將一堆指令包成一個有名嘅動作；[[r2]]喺 main 上面定義，喺 main 入面用名加括號呼叫；"
          "[[r3]]void 即係唔回傳任何值；[[r4]]呼叫一定要有括號。",
          BulletCard("今集重點", [("函數：有名嘅一堆指令", "r1"), ("定義喺上面，用 名() 呼叫", "r2"),
                                ("void：唔回傳值", "r3"), ("記得括號 ()", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數 sayHello，印出一句自我介紹，再喺 main 入面呼叫兩次。"
          "[[next]]下一集，我哋學點樣將資料傳入函數，同埋由函數攞返結果。多謝收睇，下次見！",
          EndCard("寫一個函數 sayHello()，印出一句自我介紹，再喺 main 入面呼叫兩次。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

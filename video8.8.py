#!/usr/bin/env python3
"""Video 95 (syllabus 8.8): stack 同 queue

A bracket matcher on std::stack<char>: the real session prints ok for "(a[1] + b) * {c}", bad
for "(a[1)]" (the top is [ when ) arrives) and bad for "((x)"
(one ( left over). A ticket queue on std::queue really serves Amy, Ben, Cat in arrival order.
Run `python3 video8.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 95
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-08"
BR = (CODE / "brackets.cpp").read_text()
TK = (CODE / "tickets.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
IN = ["(a[1] + b) * {c}", "(a[1)]", "((x)", "^D"]

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"brackets.cpp": BR, "tickets.cpp": TK}, [
    "g++ -std=c++20 -Wall -Wextra brackets.cpp -o br", Input("./br", IN), "clear",
    "g++ -std=c++20 -Wall -Wextra tickets.cpp -o tk", "./tk",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "(a[1] + b) * {c}\nok\n(a[1)]\nbad\n((x)\nbad\n", r1.output
assert r2.output == "serving Amy\nserving Ben\nserving Cat\n" and c1.code == c2.code == cch.code == 0 and rch.output == "olleh\n"

SAY = {"std::stack": "S T D stack", "std::queue": "S T D queue", "push": "push", "pop": "pop", "top": "top", "front": "front",
       "empty": "empty", "LIFO": "L I F O", "FIFO": "F I F O", "opens": "opens", "closes": "closes", "npos": "n pos",
       "Amy": "Amy", "Ben": "Ben", "Cat": "Cat", "serving": "serving", "ok": "OK", "bad": "bad", "olleh": "o l l e h"}

s = Stage({"brackets.cpp": BR, "tickets.cpp": TK}, title="stack 同 queue", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！有啲情況，最後放入去嘅，要最先攞出嚟，好似一疊碟；有啲情況，先到先得，好似排隊。今集學 std::stack 同 std::queue。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "後入先出 · 先入先出")),
    Scene("goal",
          "今集會講：[[b1]]stack：後入先出；[[b2]]用 stack 檢查括號；[[b3]]queue：先入先出；[[b4]]兩個嘅操作。",
          BulletCard("今集學識", [("stack：LIFO", "b1"), ("括號配對", "b2"), ("queue：FIFO", "b3"), ("push、pop、top、front", "b4")])),
    Scene("stack",
          "[[push]]stack 只可以喺頂部操作：push 放上去，[[top]]top 睇最頂嗰個，[[pop]]pop 攞走最頂嗰個。最後放嘅，最先出嚟。",
          BoxesCard("std::stack：後入先出", [
              BoxRow([Box("", "{", "top", at="push", color=GREEN, w=160, key="t")]),
              BoxRow([Box("", "[", "", at="push", color=BLUE, w=160)]),
              BoxRow([Box("", "(", "最早放", at="push", color=BLUE, w=160)]),
          ], notes=[("top() 睇 · pop() 攞走", "top"), ("最後放嘅最先出", "pop")], top=CONTENT_TOP - 20, row_h=125, box_h=90, size=46)),
    Scene("code",
          "括號檢查：[[open]]見到開括號，就 push 入 stack。[[close]]見到關括號，最頂嗰個一定要係配對嘅開括號，唔係就錯；啱就 pop 走。[[end]]最後 stack 要清空，"
          "冇剩低未關嘅括號。",
          s.scene(Open("brackets.cpp", at="open"), Mark((12, 13), at="open"), Mark((14, 18), at="close"), Mark(21, at="end"))),
    Scene("run1",
          "[[cc]]編譯運行，輸入三行。[[o1]]第一行，括號全部配對，OK。[[o2]]第二行，中括號未關，就嚟咗個小括號，bad。[[o3]]第三行，多咗一個開括號冇關，bad。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o1", type_rate=24))),
    Scene("trace",
          "逐步睇第二行：[[a]]小括號 push；[[b]]中括號 push；[[c]]跟住嚟咗關小括號，但係最頂係中括號，唔配對，即刻 bad。",
          TableCard("(a[1)] 逐步", ["字元", "動作", "stack"], [
              (["(", "push", "("], "a"),
              (["[", "push", "( ["], "b"),
              ([")", "top 係 [，唔配對", "bad"], "c", RED),
          ], widths=[0.7, 1.6, 1], code_cols=(0, 2), size=40)),
    Scene("queue",
          "[[open]]queue 就係排隊：[[push]]push 喺尾加入，[[front]]front 睇排頭嗰個，pop 攞走排頭。[[cc]]編譯運行，[[o]]Amy、Ben、Cat，按到嘅次序服務：最早到嘅，最先處理。",
          s.scene(Run(clr, at="open"), Open("tickets.cpp", at="open"), Mark((7, 9), at="push"), Mark((11, 12), at="front"), Mark(None, at="cc"),
                  Run(c2, at="cc"), Run(r2))),
    Scene("ops",
          "[[s]]stack 用 top 睇最頂；[[q]]queue 用 front 睇排頭，back 睇排尾。[[pop]]留意：兩個嘅 pop 都唔會回傳嘢，要先睇，再 pop。[[e]]空嘅時候唔好睇，"
          "先用 empty 檢查。",
          TableCard("stack vs queue", ["", "stack", "queue"], [
              (["加入", "push", "push（尾）"], "s"),
              (["睇", "top()", "front()、back()"], "q"),
              (["攞走", "pop()：唔回傳", "pop()：唔回傳"], "pop", AMBER),
              (["空？", "empty()", "empty()"], "e"),
          ], widths=[0.7, 1.2, 1.4], code_cols=(1, 2), size=38)),
    Scene("recap",
          "總結：[[r1]]stack 後入先出，只喺頂部操作；[[r2]]括號配對、復原上一步，都好啱用 stack；[[r3]]queue 先入先出，好似排隊；[[r4]]pop 唔回傳嘢，空嘅時候唔好睇。",
          BulletCard("今集重點", [("stack：LIFO，top", "r1"), ("括號配對、undo", "r2"), ("queue：FIFO，front", "r3"), ("pop 唔回傳；先查 empty", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 stack char，將 hello 倒轉印出嚟。[[next]]下一集：priority_queue。多謝收睇，下次見！",
          EndCard("用 std::stack<char>：逐個 push \"hello\" 嘅字元，再逐個 top、pop，印出 olleh。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

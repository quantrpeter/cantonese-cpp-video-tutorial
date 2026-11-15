#!/usr/bin/env python3
"""Video 114 (syllabus 9.6): 讀寫檔案

std::ofstream writes two lines to notes.txt (`cat notes.txt` and `ls` really show it).
Reading back with a misspelled name ("note.txt") and no check really prints nothing at all;
checking `if (!in)` prints "cannot open"; with the right name std::getline numbers the lines
(1: buy milk / 2: call Amy). Run `python3 video114.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 114
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-06"
FINAL = (CODE / "notes.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CHECK = "    if (!in) {\n        std::cout << \"cannot open\\n\";\n        return 1;\n    }\n"
READ = "    std::ifstream in" + FINAL.split("    std::ifstream in")[1].rsplit("}\n", 1)[0]
V3 = FINAL.replace('std::ifstream in("notes.txt");', 'std::ifstream in("note.txt");')
V2 = V3.replace(CHECK, "")
V1 = FINAL.replace(READ, "").replace("#include <string>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra notes.cpp -o notes"

(c1, r1, cat, ls, clr, c2, r2, c3, r3, clr2, c4, r4, cch, rch) = cpp.session({"notes.cpp": V1}, [
    CC, "./notes", "cat notes.txt", "ls", "clear", Write("notes.cpp", V2), CC, "./notes", Write("notes.cpp", V3), CC, "./notes",
    "clear", Write("notes.cpp", FINAL), CC, "./notes",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "" and cat.output == "buy milk\ncall Amy\n" and "notes.txt" in ls.output, (r1.output, cat.output, ls.output)
assert r2.output == "" and r2.code == 0 and r3.output == "cannot open\n" and r3.code == 1, (r2.output, r3.output)
assert r4.output == "1: buy milk\n2: call Amy\n" and c1.code == c2.code == c3.code == c4.code == cch.code == 0 and rch.output == "3\n"

SAY = {"std::ofstream": "S T D o f stream", "ofstream": "o f stream", "std::ifstream": "S T D i f stream", "ifstream": "i f stream",
       "<fstream>": "f stream", "std::getline": "S T D get line", "getline": "get line", "notes.txt": "notes 點 t x t", "note.txt": "note 點 t x t",
       "cat": "cat", "ls": "l s", "if (!in)": "if 唔係 in", "close()": "close", "std::ios::app": "ios app", "buy milk": "buy milk",
       "call Amy": "call Amy", "todo.txt": "to do 點 t x t"}

s = Stage({"notes.cpp": V1}, title="讀寫檔案", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！程式一結束，變數就冇晒。想記住啲嘢，就要寫入檔案。今集學 fstream：寫檔、讀檔，同埋最容易漏嘅一步：檢查檔案有冇開到。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "ofstream · ifstream · getline")),
    Scene("goal",
          "今集會講：[[b1]]ofstream 寫檔；[[b2]]ifstream 讀檔；[[b3]]檢查有冇開到；[[b4]]getline 逐行讀。",
          BulletCard("今集學識", [("std::ofstream", "b1"), ("std::ifstream", "b2"), ("if (!in)", "b3"), ("std::getline", "b4")])),
    Scene("write",
          "[[open]]ofstream out，開一個叫 notes.txt 嘅檔案嚟寫。[[put]]用法同 cout 一樣，兩個細過號就寫入去；[[close]]寫完 close。[[cc]]編譯運行：[[o]]冇印嘢。"
          "[[cat]]用 cat 睇吓個檔：兩行字真係寫咗入去，ls 都見到 notes.txt。程式完咗，個檔仲喺度。",
          s.scene(Open("notes.cpp", at="open"), Mark(5, at="open"), Mark((6, 7), at="put"), Mark(8, at="close"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1), Run(cat, at="cat"), Run(ls))),
    Scene("read",
          "[[type]]跟住讀返出嚟：ifstream in，[[loop]]getline 每次讀一整行，讀到冇就停。但係我打錯咗檔名：note，少咗個 s。[[cc]]運行：[[o]]乜都冇印！冇錯誤，乜都冇。",
          s.scene(Run(clr, at="type"), Replace("notes.cpp", "#include <iostream>\n", "#include <iostream>\n#include <string>\n", at="type", rate=40),
                  Type("notes.cpp", READ.replace(CHECK, "").replace("notes.txt", "note.txt"), before="}", last=True, rate=60), Expect("notes.cpp", V2),
                  Mark(10, at="type"), Mark((13, 16), at="loop"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("check",
          "[[why]]開檔失敗，ifstream 唔會 throw，只係變成失敗狀態，之後讀乜都讀唔到。[[type]]所以一定要檢查：if 唔係 in，就印 cannot open，return 一。"
          "[[cc]]運行：[[o]]cannot open，起碼知道出咗事。",
          s.scene(Note("開唔到：唔會 throw\n靜靜雞乜都讀唔到", at="why", where="editor"), Note(None, at="type"),
                  Type("notes.cpp", CHECK, after='std::ifstream in("note.txt");\n', at="type", rate=40), Expect("notes.cpp", V3),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("fix",
          "[[type]]改返正確嘅檔名 notes。[[cc]]運行：[[o]]一，buy milk；二，call Amy。",
          s.scene(Run(clr2, at="type"), Replace("notes.cpp", '"note.txt"', '"notes.txt"', at="type", rate=20), Expect("notes.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("modes",
          "幾個重點：[[trunc]]ofstream 預設會清空舊內容；[[app]]想加喺後面，就用 std::ios::app；[[raii]]就算唔 close，物件消失嗰陣都會自動關檔，又係 RAII。",
          TableCard("開檔模式", ["寫法", "效果"], [
              (["std::ofstream out(\"f\");", "清空再寫"], "trunc"),
              (["std::ofstream out(\"f\", std::ios::app);", "加喺尾"], "app", GREEN),
              (["{ std::ofstream out(\"f\"); … }", "離開大括號自動關"], "raii"),
          ], widths=[2, 1], code_cols=(0,), size=34)),
    Scene("recap",
          "總結：[[r1]]ofstream 寫，ifstream 讀，用法同 cout、cin 一樣；[[r2]]開檔一定要檢查；[[r3]]getline 逐行讀；[[r4]]ios::app 加喺尾，物件消失自動關檔。",
          BulletCard("今集重點", [("ofstream / ifstream", "r1"), ("if (!in)：一定要查", "r2"), ("while (std::getline(in, line))", "r3"), ("ios::app、RAII 關檔", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]先寫兩行入 todo.txt，再用 ios::app 加一行，最後讀返出嚟數有幾多行。[[next]]下一集：stringstream 同解析文字。多謝收睇，下次見！",
          EndCard("寫兩行入 todo.txt，用 std::ios::app 再加一行，讀返出嚟數行數：答案 3。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

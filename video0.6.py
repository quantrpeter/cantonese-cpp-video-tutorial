#!/usr/bin/env python3
"""Video 6 (syllabus 0.6): 註解同寫碼風格

A messy program and its tidy twin give the same output (both compiled for real); // and /* */
comments typed on camera; commenting out a line to disable it; VS Code auto format; naming.
Run `python3 video0.6.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 6
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "00-06"
MESSY = (CODE / "messy.cpp").read_text()
FINAL = (CODE / "tidy.cpp").read_text()                     # with every comment added on camera
HEADER = "/* 我嘅第一個整齊程式\n   作者：陳大文 */\n"
TAIL = "  // 最後一句"
TIDY = FINAL.replace(HEADER, "").replace(TAIL, "")          # how tidy.cpp starts
OFF = FINAL.replace('    std::cout << "I am', '    // std::cout << "I am')   # line 2 commented out
CCM = "g++ -std=c++20 -Wall -Wextra messy.cpp -o messy"
CCT = "g++ -std=c++20 -Wall -Wextra tidy.cpp -o tidy"

(cm, rm, ct, rt, clr, ct2, rt2, ct3, rt3) = cpp.session({"messy.cpp": MESSY, "tidy.cpp": TIDY}, [
    CCM, "./messy", CCT, "./tidy",
    Write("tidy.cpp", FINAL), "clear", CCT, "./tidy",
    Write("tidy.cpp", OFF), CCT, "./tidy",
], refresh=opts.fresh_runs, cols=48)
assert rm.output == rt.output == rt2.output, "messy, tidy and commented versions must print the same"
assert "I am learning" not in rt3.output and all(r.code == 0 for r in (cm, ct, ct2, ct3))

s = Stage({"messy.cpp": MESSY, "tidy.cpp": TIDY}, title="註解同寫碼風格")

scenes = [
    Scene("intro",
          "歡迎返嚟！程式唔單止係寫俾電腦睇，仲係寫俾人睇，包括幾個月之後嘅你自己。今集講註解同寫碼風格。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "寫俾人睇嘅程式")),
    Scene("goal",
          "今集會講：[[b1]]兩種註解；[[b2]]點樣用註解暫時停用一行程式；[[b3]]寫碼嘅三個好習慣；[[b4]]仲有點樣改個好名。",
          BulletCard("今集學識", [("兩種註解：// 同 /* */", "b1"), ("用註解暫時停用一行", "b2"),
                                ("一行一句、縮排、留空間", "b3"), ("改個好名", "b4")])),
    Scene("messy",
          "睇吓呢個程式。[[cc]]佢可以編譯，[[run]]亦都行得，[[hard]]但係全部擠埋一齊，第二行長到睇唔晒，邊句開始、邊句完都唔清楚。",
          s.scene(Open("messy.cpp", mode="instant"), Run(cm, at="cc"), Run(rm, at="run"),
                  Note("行得，但係好難睇", at="hard"))),
    Scene("tidy",
          "同一個程式，[[tidy]]執靚之後係咁樣，清楚好多。[[cc]]編譯運行，結果一模一樣。[[same]]編譯器唔理你寫得靚唔靚，但係人會。",
          s.scene(Note(None), Open("tidy.cpp", at="tidy", rate=9), Run(ct, at="cc"), Run(rt),
                  Note("結果一樣\n編譯器唔理靚唔靚，人會", at="same"))),
    Scene("rules",
          "執靚程式有三個好習慣：[[r1]]一行一句，每句指令自己一行；[[r2]]縮排，大括號入面嘅嘢縮入四格，一眼就睇到邊啲屬於 main；"
          "[[r3]]留空間，<< 前後加空格，唔同部分之間空一行。",
          BulletCard("寫碼三個好習慣", [("一行一句：每句指令自己一行", "r1"), ("縮排：大括號入面，縮入 4 格", "r2"),
                                      ("留空間：<< 前後加空格，唔同部分空一行", "r3")])),
    Scene("format",
          "唔想自己慢慢執？VS Code 有自動排版：[[win]]Windows 撳 Shift、Alt、F，[[mac]]Mac 撳 Shift、Option、F，"
          "[[linux]]Linux 就撳 Ctrl、Shift、I。[[auto]]佢會幫你執好縮排同空格。",
          TileCard("VS Code 自動排版", [
              Tile("🪟", "Windows", "Shift + Alt + F", "win", BLUE),
              Tile("🍎", "Mac", "Shift + Option + F", "mac", PURPLE),
              Tile("🐧", "Linux", "Ctrl + Shift + I", "linux", TEAL),
          ], height=330, footer=("撳一下，自動執好縮排同空格", "auto"))),
    Scene("comment1",
          "留意第三行。[[mark]]兩條斜線開頭嘅，叫做註解。由 // 開始，一直到嗰行尾，編譯器都會完全無視，所以可以寫中文，用嚟解釋程式做緊乜。",
          s.scene(Note(None), Run(clr), Mark(3, at="mark"), Note("// 開始到行尾：註解\n編譯器完全無視", at="mark"))),
    Scene("comment2",
          "[[type]]註解亦可以放喺一句指令後面。[[block]]如果想寫幾行，就用 /* 開始、*/ 結束，中間寫幾多行都得，"
          "通常放喺檔案最頂，講吓個程式係做乜、邊個寫。[[run]]編譯運行，結果完全冇變。",
          s.scene(Mark(None), Note(None), Type("tidy.cpp", TAIL, after='"See you!\\n";', at="type"),
                  Type("tidy.cpp", HEADER, before="#include", at="block"), Expect("tidy.cpp", FINAL),
                  Note("/* … */：幾多行都得", at="block"), Run(ct2, at="run", recall=True), Run(rt2, recall=True))),
    Scene("disable",
          "註解仲有個好用嘅地方：[[cmt]]喺一行前面加 //，就可以暫時停用佢。[[run]]編譯運行，嗰句就冇再印出嚟。"
          "[[key]]喺 VS Code，撳 Ctrl 同斜線，就可以一下開關註解。[[undo]]想用返，刪走 // 就得。",
          s.scene(Note(None), Type("tidy.cpp", "// ", before='std::cout << "I am', at="cmt"), Expect("tidy.cpp", OFF),
                  Run(ct3, at="run", recall=True), Run(rt3, recall=True), Note("Windows／Linux：Ctrl + /\nMac：Cmd + /", at="key"),
                  Replace("tidy.cpp", '// std::cout << "I am', 'std::cout << "I am', at="undo"), Expect("tidy.cpp", FINAL))),
    Scene("naming",
          "最後講改名。之後學變數嘅時候，[[bad]]a、b、c 呢啲名，過幾日你自己都唔記得係乜；[[good]]改做 pricePerBook、books、total，"
          "一睇就明。檔案名都一樣，hello.cpp 好過 abc.cpp。",
          CodeCompareCard("改個好名", [
              Pane("唔清楚", "int a = 15;\nint b = 3;\nint c = a * b;", False, "bad"),
              Pane("一睇就明", "int pricePerBook = 15;\nint books = 3;\nint total = pricePerBook * books;", True, "good"),
          ])),
    Scene("recap",
          "總結：[[r1]]兩條斜線係單行註解，斜線星係多行註解；[[r2]]註解可以暫時停用一行程式；[[r3]]一行一句、縮排四格、留空間；"
          "[[r4]]仲有改有意思嘅名。",
          BulletCard("今集重點", [("// 單行註解，/* */ 多行註解", "r1"), ("註解可以暫時停用一行程式", "r2"),
                                ("一行一句、縮排 4 格、留空間", "r3"), ("改有意思嘅名", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]搵返你嘅 Hello World，喺每一行上面加一句註解解釋佢做乜，再用 VS Code 自動排版試吓。"
          "[[next]]起步篇完成喇！下一集開始第一章：變數。多謝收睇，下次見！",
          EndCard("搵返你嘅 Hello World，喺每一行上面加一句註解解釋佢，再用 VS Code 自動排版試吓。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)

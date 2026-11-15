#!/usr/bin/env python3
"""Video 28 (syllabus 2.10): 隨機數

Five dice rolls with std::mt19937 and uniform_int_distribution: seed 42 really gives the same
rolls on two runs; a generator made inside the loop rolls the same number five times; seeding
from std::random_device makes two runs differ; why not rand(). Run `python3 video2.10.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 28
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-10"
FINAL = (CODE / "dice.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
RD = "    std::random_device rd;\n"
V1 = FINAL.replace(RD, "").replace("gen(rd())", "gen(42)")
GEN = "    std::mt19937 gen(42);\n"
LOOP_HEAD = "for (int i = 0; i < 5; i++) {\n"
INLOOP = V1.replace(GEN, "").replace(LOOP_HEAD, LOOP_HEAD + "    " + GEN)
CC = "g++ -std=c++20 -Wall -Wextra dice.cpp -o dice"

(c1, r1a, r1b, c2, r2, clr, c3, r3a, r3b, cch, rch) = cpp.session({"dice.cpp": V1}, [
    CC, "./dice", "./dice",
    Write("dice.cpp", INLOOP), CC, "./dice",
    Write("dice.cpp", FINAL), "clear", CC, "./dice", "./dice",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
rolls = r1a.output.split()
assert r1a.output == r1b.output and len(rolls) == 5 and all(x in "123456" for x in rolls)
same = r2.output.split()
assert len(set(same)) == 1 and same[0] == rolls[0], same
assert r3a.output != r3b.output, "two random_device runs happened to match; rerun with --fresh-runs"
assert all(r.code == 0 for r in (c1, c2, c3, cch)) and "=" in rch.output

SAY = {"mt19937": "M T 一九九三七", "std::mt19937": "S T D M T 一九九三七", "uniform_int_distribution": "uniform int distribution",
       "random_device": "random device", "dice(gen)": "dice gen", "rand()": "rand", "rand": "rand", "random": "random"}

s = Stage({"dice.cpp": V1}, title="隨機數：擲骰仔", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！遊戲、抽獎、模擬，都需要隨機數。今集用 C++ 嘅 random 函式庫，嚟擲骰仔。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "<random> · mt19937 · 種子")),
    Scene("goal",
          "今集會講：[[b1]]亂數產生器 mt19937；[[b2]]分佈：決定數字嘅範圍；[[b3]]種子 seed；[[b4]]點解唔好再用 rand。",
          BulletCard("今集學識", [("亂數產生器 std::mt19937", "b1"), ("分佈：uniform_int_distribution", "b2"),
                                ("種子 seed", "b3"), ("點解唔用 rand()", "b4")])),
    Scene("open",
          "[[inc]]要 include random。[[gen]]mt19937 係一個亂數產生器，括號入面嘅四十二，叫做種子。"
          "[[dist]]uniform_int_distribution 決定範圍：一至六，每個數字機會均等。[[roll]]dice(gen) 就係擲一次。",
          s.scene(Open("dice.cpp", at="inc"), Mark(2, at="inc"), Mark(5, at="gen"), Mark(6, at="dist"), Mark(8, at="roll"))),
    Scene("run1",
          "[[cc]]編譯運行，[[o1]]擲咗五次。[[again]]再運行多一次，[[o2]]咦，五個數字完全一樣？",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1a), Run(r1b, at="again", recall=True),
                  Note("兩次完全一樣？", at="o2", where="editor"))),
    Scene("seed",
          "因為電腦冇真正嘅隨機。[[formula]]mt19937 用一條數學公式，計出一串睇落好似隨機嘅數；[[same]]種子一樣，成串數就一模一樣。"
          "[[good]]呢個其實有用：測試嘅時候，可以每次重現同一個結果。",
          TileCard("種子 seed", [
              Tile("🧮", "一條公式", "由種子開始\n計出一串好似隨機嘅數", "formula", BLUE),
              Tile("🌱", "種子一樣", "成串數一模一樣\n測試嘅時候好有用", "same", GREEN),
          ], cols=2, height=360)),
    Scene("inloop",
          "順帶一提一個常見錯誤：[[mv]]將產生器搬咗入迴圈入面。[[cc]]運行，[[o]]五次都係同一個數！"
          "因為每次都用同一個種子，由頭開始。[[fix]]產生器只應該整一次，放喺迴圈外面。",
          s.scene(Note(None), Replace("dice.cpp", GEN, "", at="mv"), Type("dice.cpp", "    " + GEN, after=LOOP_HEAD),
                  Expect("dice.cpp", INLOOP), Run(c2, at="cc", recall=True), Run(r2),
                  Replace("dice.cpp", "    " + GEN, "", at="fix"), Type("dice.cpp", GEN, before="    std::uniform_int"),
                  Expect("dice.cpp", V1))),
    Scene("rd",
          "想每次運行都唔同，[[rd]]就用 random_device，攞一個真正隨機嘅種子，[[seed]]再交俾 mt19937。"
          "[[cc]]編譯運行，[[o1]]第一次……[[o2]]第二次，今次唔同咗。",
          s.scene(Run(clr, at="rd"), Type("dice.cpp", RD, before="    std::mt19937", at="rd"),
                  Replace("dice.cpp", "gen(42)", "gen(rd())", at="seed"), Expect("dice.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3a), Run(r3b, at="o2", recall=True))),
    Scene("rand",
          "你可能喺網上見過 rand。[[old]]佢係 C 語言留落嚟嘅舊函數：質素差，用百分號取範圍，仲會令某啲數字機會多啲。"
          "[[new]]寫新程式，就用 mt19937 加 uniform_int_distribution。",
          CodeCompareCard("rand() 定 <random>？", [
              Pane("舊：rand()", "std::srand(std::time(0));\nint d = std::rand() % 6 + 1;", False, "old"),
              Pane("新：<random>", "std::mt19937 gen(rd());\nstd::uniform_int_distribution<int>\n    dice(1, 6);\nint d = dice(gen);",
                   True, "new"),
          ], size=28)),
    Scene("recap",
          "總結：[[r1]]mt19937 係亂數產生器，只整一次；[[r2]]uniform_int_distribution 決定範圍；[[r3]]種子一樣，結果就一樣；"
          "[[r4]]用 random_device 做種子，每次都唔同；唔好再用 rand。",
          BulletCard("今集重點", [("std::mt19937：只整一次", "r1"), ("uniform_int_distribution(1, 6)", "r2"),
                                ("種子一樣 → 結果一樣", "r3"), ("random_device 做種子；唔用 rand()", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]擲兩粒骰仔，印出兩粒嘅點數同總和；如果兩粒一樣，再印 Double!"
          "[[next]]下一集係第二章嘅小項目：估數字遊戲。多謝收睇，下次見！",
          EndCard("擲兩粒骰仔，印出兩粒嘅點數同總和；如果兩粒一樣，再印 Double!",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

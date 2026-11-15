#!/usr/bin/env python3
"""Video 38 (syllabus 3.9): 遞迴

factorial(n) = n * factorial(n - 1) with a base case; the call stack traced for factorial(5);
without the base case g++ warns of infinite recursion and the run really ends in a segmentation
fault (stack overflow); fib(45) with two recursive calls really takes seconds (the time is quoted
from the run). Run `python3 video38.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 38
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-09"
FACT = (CODE / "fact.cpp").read_text()
FIB = (CODE / "fib.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BASE = "    if (n <= 1) {\n        return 1;\n    }\n"
NOBASE = FACT.replace(BASE, "")
CF = "g++ -std=c++20 -Wall -Wextra fact.cpp -o fact"
CB = "g++ -std=c++20 -Wall -Wextra fib.cpp -o fib"

(c1, r1, c2, r2, clr, c3, r3a, r3b, cch, rch) = cpp.session({"fact.cpp": FACT, "fib.cpp": FIB}, [
    CF, "./fact", Write("fact.cpp", NOBASE), CF, "./fact", Write("fact.cpp", FACT),
    "clear", CB, Input("./fib", ["30"]), Input("./fib", ["45"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["120", "2432902008176640000"]
assert "infinite recursion detected" in cpp.visible(c2.output) and r2.code != 0
crash = r2.output.strip().split("\n")[-1]
assert crash == "Segmentation fault", r2.output
assert r3a.output.endswith("fib(30) = 832040\n") and r3b.output.endswith("fib(45) = 1134903170\n")
slow = r3b.io[-1][2] - next(t for k, _, t in r3b.io if k == "i")      # from typing 45 to the answer
assert slow > 2, slow
assert c1.code == c3.code == cch.code == 0 and rch.output.strip() == "5050"

a, b = 0, 1
for _ in range(46):
    a, b = b, a + b
CALLS = 2 * a - 1                      # calls made by fib(45): 2 * fib(46) - 1

SAY = {"factorial": "factorial", "factorial(5)": "factorial 五", "factorial(n - 1)": "factorial n 減一",
       "fib": "fib", "fib(45)": "fib 四十五", "base case": "base case", "call stack": "call stack",
       "stack overflow": "stack overflow", "Segmentation fault": "Segmentation fault"}

s = Stage({"fact.cpp": FACT, "fib.cpp": FIB}, title="遞迴", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！一個函數入面，可以再呼叫佢自己，呢個方法叫做遞迴。今集我哋用遞迴，計階乘，同埋計費氏數列。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "recursion · base case · call stack"), seed=12),
    Scene("goal",
          "今集會講：[[b1]]遞迴：函數呼叫自己；[[b2]]base case：幾時停；[[b3]]call stack：一層一層咁等；[[b4]]冇 base case 會點。",
          BulletCard("今集學識", [("遞迴 recursion", "b1"), ("base case：停嘅條件", "b2"), ("call stack", "b3"),
                                ("stack overflow", "b4")])),
    Scene("idea",
          "諗吓五嘅階乘：[[a]]五嘅階乘，等於五乘四嘅階乘；[[b]]四嘅階乘，又等於四乘三嘅階乘……[[c]]一直落去，[[d]]去到一嘅階乘，就係一，唔使再拆。"
          "[[same]]大問題，變成同一樣、但係細少少嘅問題：呢個就係遞迴。",
          BulletCard("5! 點樣拆？", [("5! = 5 × 4!", "a"), ("4! = 4 × 3!", "b"), ("3! = 3 × 2!，2! = 2 × 1!", "c"),
                                   ("1! = 1：唔使再拆（base case）", "d")], size=50)),
    Scene("code",
          "[[open]]寫成程式：[[base]]如果 n 細過或等於一，就直接回傳一，呢個係 base case，即係停嘅條件；"
          "[[rec]]否則，就回傳 n 乘 factorial(n - 1)：函數呼叫自己。[[cc]]編譯運行，[[o]]一百二十，同埋二十嘅階乘。",
          s.scene(Open("fact.cpp", at="open"), Mark((4, 6), at="base"), Mark(7, at="rec"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("stack",
          "電腦點樣計？[[down]]factorial(5) 要等 factorial(4)，factorial(4) 又要等 factorial(3)，一層疊一層，叫做 call stack。"
          "[[base]]去到 factorial(1)，碰到 base case，回傳一；[[up]]然後一層一層咁返上去：二、六、二十四，最後一百二十。",
          TableCard("call stack：一層疊一層", ["呼叫", "要計", "回傳"], [
              (["factorial(5)", "5 × factorial(4)", "120"], ("down", 0.0)),
              (["factorial(4)", "4 × factorial(3)", "24"], ("down", 0.6)),
              (["factorial(3)", "3 × factorial(2)", "6"], ("down", 1.2)),
              (["factorial(2)", "2 × factorial(1)", "2"], ("down", 1.8)),
              (["factorial(1)", "base case", "1"], "base", GREEN),
          ], widths=[1.1, 1.4, 0.6], code_cols=(0, 1, 2), size=40, note=("回傳由下而上：1 → 2 → 6 → 24 → 120", "up"))),
    Scene("nobase",
          "如果冇 base case 會點？[[del]]刪走佢。[[cc]]編譯，[[warn]]g++ 已經警告：偵測到無限遞迴。[[run]]照運行，[[o]]程式死咗：Segmentation fault。",
          s.scene(Replace("fact.cpp", BASE, "", at="del"), Expect("fact.cpp", NOBASE), Run(c2, at="cc", recall=True),
                  Run(r2, at="run"), Note(f"{crash}\n＝ stack overflow", at="o", where="editor"))),
    Scene("overflow",
          "因為每呼叫一次函數，就要喺 stack 記憶體留一格位，記住佢嘅變數同埋返去邊。[[forever]]冇 base case，就會一直呼叫落去，"
          "[[full]]直到 stack 滿瀉，程式就當機，叫做 stack overflow。[[fix]]所以遞迴一定要有 base case。",
          s.scene(Note(None), Note("每次呼叫：用一格 stack\n無限呼叫 → 爆 stack", at="forever", where="editor"),
                  Note(None, at="fix"), Type("fact.cpp", BASE, after="long long factorial(int n) {\n", at="fix"),
                  Expect("fact.cpp", FACT))),
    Scene("fib",
          "再嚟費氏數列：每個數係前兩個數之和。[[open]]fib(n) 等於 fib(n - 1) 加 fib(n - 2)，一次呼叫兩個自己。"
          "[[cc]]編譯運行，[[t1]]輸入三十，[[o1]]即刻有答案：八十三萬零四十。三十個數，一眨眼就計完。",
          s.scene(Run(clr, at="open"), Open("fib.cpp", at="open"), Mark(7, at="open"), Mark(None, at="cc"),
                  Run(c3, at="cc"), Run(r3a, keys=("t1",)))),
    Scene("fib45",
          "[[t2]]再試四十五。你會見到，個程式停咗喺度，好似死咗機咁。其實佢仲喺度計緊，因為要呼叫好多好多次函數。"
          f"[[done]]終於有答案，等咗成{zh_seconds(slow)}！",
          s.scene(Run(r3b, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("why_slow",
          "點解咁慢？[[tree]]因為 fib(45) 要計 fib(44) 同 fib(43)，佢哋又各自再拆兩個，同一個數被重複計咗好多好多次，"
          f"加埋要呼叫{zh_int(CALLS // 10**8)}億幾次。[[later]]第十二章學動態規劃嘅時候，會教點樣記住計過嘅答案，快好多好多倍。",
          TileCard("點解 fib(45) 咁慢？", [
              Tile("🌳", "每次拆兩個", "fib(45) → fib(44) + fib(43)\n每個又再拆兩個……", "tree", AMBER),
              Tile("🔁", "重複計", "fib(43) 喺唔同地方\n被計咗好多次", "tree", RED),
          ], cols=2, height=360, footer=("12.14 動態規劃：記住計過嘅答案", "later"))),
    Scene("recap",
          "總結：[[r1]]遞迴就係函數呼叫自己，將問題變細；[[r2]]一定要有 base case，唔係就會 stack overflow；"
          "[[r3]]每一層呼叫都排喺 call stack 等；[[r4]]遞迴寫得短，但係可能好慢。",
          BulletCard("今集重點", [("遞迴：呼叫自己，問題變細", "r1"), ("一定要有 base case", "r2"),
                                ("call stack：一層一層等", "r3"), ("寫得短，未必快", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用遞迴寫 sumTo(n)，計由一加到 n。[[next]]下一集，我哋將程式拆開做幾個檔案。多謝收睇，下次見！",
          EndCard("用遞迴寫 sumTo(n)，計 1 + 2 + … + n。base case 係乜？",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

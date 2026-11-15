#!/usr/bin/env python3
"""Video 29 (syllabus 2.11): 小項目：估數字

Part 2's project: the computer picks 1-100 with <random>, a while loop reads guesses and says
Too big / Too small. The game is really played: the input player halves the range after each
reply (cpp.Input bisect), and the narration quotes its actual guesses. A forgotten tries++
really reports 0 tries. Run `python3 video29.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 29
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-11"
FINAL = (CODE / "guess.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SKEL = "#include <iostream>\n#include <random>\n\nint main() {\n}\n"
RAND = ("    std::random_device rd;\n    std::mt19937 gen(rd());\n"
        "    std::uniform_int_distribution<int> pick(1, 100);\n    const int answer = pick(gen);\n")
VARS = "\n    int guess{0};\n    int tries{0};\n"
LOOP = ("    while (guess != answer) {\n        std::cout << \"Guess (1-100): \";\n        std::cin >> guess;\n"
        "        if (guess > answer) {\n            std::cout << \"Too big\\n\";\n"
        "        } else if (guess < answer) {\n            std::cout << \"Too small\\n\";\n        }\n    }\n")
END = "    std::cout << \"Correct! \" << tries << \" tries\\n\";\n"
BUG = SKEL.replace("}\n", RAND + VARS + LOOP + END + "}\n")
TRIES = "        tries++;\n"
assert BUG.replace("std::cin >> guess;\n", "std::cin >> guess;\n" + TRIES) == FINAL
CC = "g++ -std=c++20 -Wall -Wextra guess.cpp -o guess"
PLAYER = {"bisect": [1, 100], "big": "Too big", "small": "Too small"}

(c1, r1, c2, r2, cch, rch) = cpp.session({"guess.cpp": BUG}, [
    CC, Input("./guess", [PLAYER]),
    Write("guess.cpp", FINAL), CC, Input("./guess", [PLAYER]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", [PLAYER]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("Correct! 0 tries\n"), r1.output
guesses = [int(g) for g in re.findall(r"Guess \(1-100\): (\d+)", r2.output)]
replies = re.findall(r"Too big|Too small|Correct!", r2.output)
assert len(guesses) >= 3, "the answer was found in under 3 guesses; rerun with --fresh-runs for a longer game"
assert replies[-1] == "Correct!" and r2.output.endswith(f"Correct! {len(guesses)} tries\n") and len(guesses) <= 7
assert c1.code == c2.code == cch.code == 0 and ("Correct!" in rch.output or "Game over" in rch.output)
ZH = {"Too big": "太大", "Too small": "太細", "Correct!": "啱咗"}
ranges, lo, hi = [], 1, 100
for g, rep in zip(guesses, replies):
    ranges.append(f"{lo} – {hi}")
    if rep == "Too big":
        hi = g - 1
    elif rep == "Too small":
        lo = g + 1

ROWS = [([str(i + 1), rg, str(g), rep], ("t1", 0.5 * i)) + ((GREEN,) if rep == "Correct!" else ())
        for i, (rg, g, rep) in enumerate(zip(ranges, guesses, replies))]

SAY = {"tries++": "tries plus plus", "Too big": "Too big", "Too small": "Too small", "random": "random",
       "mt19937": "M T 一九九三七", "uniform_int_distribution": "uniform int distribution"}

s = Stage({"guess.cpp": SKEL}, title="小項目：估數字", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！第二章嘅小項目：估數字遊戲。電腦諗一個一至一百嘅數，你嚟估，佢話你知太大定太細，直到估中為止。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "random · while · if")),
    Scene("plan",
          "步驟係咁：[[pick]]電腦揀一個隨機數；[[read]]讀入估計；[[cmp]]比較，話你知太大定太細；[[repeat]]未估中就重複；"
          "[[done]]估中就印出用咗幾多次。",
          FlowCard("估數字：步驟", [Row("遊戲", "流程", BLUE, [
              Node("電腦揀數", "1 – 100", "pick"), Node("讀入估計", "cin", "read"),
              Node("比較", "太大？太細？", "cmp"), Node("估中", "印出次數", "done"),
          ], note="未估中：返去讀入估計（while）", note_at="repeat")])),
    Scene("rand",
          "[[rd]]用返上一集嘅 random：random_device 做種子，[[gen]]mt19937 做產生器，[[pick]]範圍係一至一百。"
          "[[ans]]答案用 const，因為揀咗之後就唔會再變。",
          s.scene(Open("guess.cpp", mode="instant"), Type("guess.cpp", RAND.splitlines(True)[0], before="}", last=True, at="rd", rate=24),
                  Type("guess.cpp", RAND.splitlines(True)[1], before="}", last=True, at="gen", rate=24),
                  Type("guess.cpp", RAND.splitlines(True)[2], before="}", last=True, at="pick", rate=30),
                  Type("guess.cpp", RAND.splitlines(True)[3], before="}", last=True, at="ans", rate=24))),
    Scene("loop",
          "[[vars]]guess 記住估嘅數，一開始係零；tries 計估咗幾多次。[[loop]]只要未估中，就一直重複：[[read]]印提示，讀入估計；"
          "[[cmp]]比答案大，就話 Too big；比答案細，就話 Too small；一樣嘅話，迴圈條件唔成立，就會離開。",
          s.scene(Type("guess.cpp", VARS, before="}", last=True, at="vars", rate=24),
                  Type("guess.cpp", "".join(LOOP.splitlines(True)[:1]), before="}", last=True, at="loop", rate=26),
                  Type("guess.cpp", "".join(LOOP.splitlines(True)[1:3]), before="}", last=True, at="read", rate=30),
                  Type("guess.cpp", "".join(LOOP.splitlines(True)[3:]), before="}", last=True, at="cmp", rate=34))),
    Scene("end",
          "[[done]]離開迴圈，即係估中咗，就印出用咗幾多次。",
          s.scene(Type("guess.cpp", END, before="}", last=True, at="done", rate=26), Expect("guess.cpp", BUG))),
    Scene("run1",
          "[[cc]]編譯，開始玩！[[play]]我哋每次都估範圍嘅中間，睇佢話太大定太細，再收窄範圍，一直估落去。"
          "[[win]]終於估中！不過，佢話用咗零次？",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("play",)), Note("用咗 0 次？", at="win", where="editor"))),
    Scene("fix",
          "原來我哋唔記得計數：[[fix]]每讀一次估計，tries 就要加一。",
          s.scene(Note(None), Type("guess.cpp", TRIES, after="std::cin >> guess;\n", at="fix"), Expect("guess.cpp", FINAL),
                  Mark(15, at="fix"))),
    Scene("run2",
          f"[[cc]]再編譯，再玩一次。[[g1]]第一次估{zh_int(guesses[0])}：{ZH[replies[0]]}；"
          f"[[g2]]跟住估{zh_int(guesses[1])}：{ZH[replies[1]]}。每次都估範圍中間，範圍就減一半。"
          f"[[win]]第{zh_int(len(guesses))}次就估中，今次次數啱晒。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("g1", "g2")))),
    Scene("table",
          "睇返成個過程：[[t1]]範圍一開始係一至一百，每估一次，就剩返一半。[[max]]一百個數，用呢個方法最多七次，就一定估中。"
          "呢個方法叫二分法，第八同第十二章會再見到。",
          TableCard("每一次估", ["次數", "範圍", "估", "結果"], ROWS, widths=[0.6, 1.1, 0.6, 1], code_cols=(0, 1, 2, 3), size=38, note=("1 – 100：二分法最多 7 次", "max"))),
    Scene("recap",
          "第二章完成！我哋學咗：[[r1]]用 if、else if 同 switch 做決定；[[r2]]用且、或、非組合條件；"
          "[[r3]]用 while、for 同 do-while 重複；[[r4]]break 同 continue，仲有隨機數。",
          BulletCard("第二章重點", [("if、else if、switch：做決定", "r1"), ("&&、||、!：組合條件", "r2"),
                                  ("while、for、do-while：重複", "r3"), ("break、continue、<random>", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個上限：最多估七次；七次都未估中，就印出答案同 Game over。"
          "[[next]]下一章，我哋學函數，將程式拆成一件一件。多謝收睇，下次見！",
          EndCard("加一個上限：最多估 7 次；7 次都未估中，就印出答案同 Game over。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

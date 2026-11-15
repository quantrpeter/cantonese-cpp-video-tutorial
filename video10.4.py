#!/usr/bin/env python3
"""Video 121 (syllabus 10.4): Debugger

average() of {70, 80, 90} really prints 56.6667 instead of 80. A real gdb session (built with -g):
break average, run, next, next, print i shows $1 = 1 (the loop starts at 1), print v shows the
vector {70, 80, 90}, backtrace shows main called average, continue prints 56.6667. Starting the
loop at 0 really prints 80. gdb.init only switches off line editing, paging and two warnings.
Run `python3 video10.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 121
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-04"
FINAL = (CODE / "avg.cpp").read_text()
GDBINIT = (CODE / "gdb.init").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = FINAL.replace("std::size_t i = 0;", "std::size_t i = 1;")
CC = "g++ -g avg.cpp -o avg"
CMDS = ["break average", "run", "next", "next", "print i", "print v", "backtrace", "continue", "quit"]
KEYS = ("b", "r", "n1", "n2", "pi", "pv", "bt", "c", "q")

(c1, r1, clr, g, clr2, c2, r2, cch, rch) = cpp.session({"avg.cpp": BAD, "gdb.init": GDBINIT}, [
    CC, "./avg", "clear", Input("gdb -q -ix gdb.init ./avg", CMDS), "clear", Write("avg.cpp", FINAL), CC, "./avg",
    Write("challenge.cpp", CHALLENGE), "g++ -g challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
gv = cpp.visible(g.output)
assert r1.output == "56.6667\n" and r2.output == "80\n", (r1.output, r2.output)
for want in ("Breakpoint 1 at", "Breakpoint 1, average", "$1 = 1", "$2 = std::vector of length 3", "70, 80, 90", "#1  0x", "in main () at avg.cpp:14",
             "56.6667", "exited normally"):
    assert want in gv, (want, gv)
assert c1.code == c2.code == cch.code == 0 and rch.output == "120\n"

SAY = {"gdb": "g d b", "-g": "D g", "break": "break", "run": "run", "next": "next", "step": "step", "print": "print", "print i": "print i",
       "print v": "print v", "backtrace": "back trace", "continue": "continue", "quit": "quit", "breakpoint": "breakpoint",
       "average": "average", "factorial": "factorial", "gdb.init": "g d b 點 init"}

s = Stage({"avg.cpp": BAD}, title="Debugger", code_px=21, split=0.45)

scenes = [
    Scene("intro",
          "歡迎返嚟！程式冇當機，但係答案錯，點搵個 bug？一路加 cout 好慢。今集學用 debugger：gdb，令程式停喺你想停嘅地方，逐行行，隨時睇變數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "break · next · print · backtrace")),
    Scene("goal",
          "今集會講：[[b1]]用 D g 編譯；[[b2]]設 breakpoint 同運行；[[b3]]逐行行同印變數；[[b4]]backtrace 睇邊個叫你。",
          BulletCard("今集學識", [("g++ -g", "b1"), ("break、run", "b2"), ("next、print", "b3"), ("backtrace", "b4")])),
    Scene("bug",
          "[[open]]average 計平均分。[[cc]]用 D g 編譯，即係加入除錯資料，令 gdb 知道每一行喺邊。運行：[[o]]七十、八十、九十，平均應該係八十，但係印咗五十六點六！",
          s.scene(Open("avg.cpp", at="open"), Mark((4, 10), at="open"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note("應該係 80？", at="o", where="editor"))),
    Scene("cmds",
          "gdb 常用指令：[[b]]break 設停車位；[[r]]run 開始運行；[[n]]next 行一行；[[p]]print 印變數；[[bt]]backtrace 睇呼叫鏈；[[c]]continue 繼續行到尾。",
          TableCard("gdb 常用指令", ["指令", "做乜"], [
              (["break average", "去到 average 就停"], "b"),
              (["run", "開始運行"], "r"),
              (["next", "行一行（唔入函數）"], "n"),
              (["print i", "印變數"], "p"),
              (["backtrace", "邊個叫邊個"], "bt"),
              (["continue", "繼續行"], "c"),
          ], widths=[1.2, 1.6], code_cols=(0,), size=36)),
    Scene("gdb",
          "[[start]]開 gdb。[[b]]break average；[[r]]run：程式停喺 average 第一行。[[n1]]next，[[n2]]再 next，入咗迴圈。[[pi]]print i：係一！"
          "[[pv]]print v 睇 vector：七十、八十、九十。第一格七十喺位置零，i 由一開始，七十就漏咗。[[bt]]backtrace：係 main 第十四行叫 average。[[c]]continue 行完，[[q]]quit 離開。一個 cout 都冇加，就搵到個 bug。",
          s.scene(Note(None), Run(clr, at="start"), Run(g, keys=KEYS, type_rate=14), Mark(6, at="pi"))),
    Scene("fix",
          "[[type]]將 i 改返由零開始。[[cc]]重新編譯運行：[[o]]八十，啱晒。",
          s.scene(Mark(None), Run(clr2, at="type"), Replace("avg.cpp", "std::size_t i = 1;", "std::size_t i = 0;", at="type", rate=10),
                  Expect("avg.cpp", FINAL), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("tips",
          "幾個貼士：[[g]]debug 一定要用 D g，最好唔好開 O 二，唔係變數可能俾優化咗；[[s]]step 會行入函數入面；[[w]]crash 嘅時候，直接喺 gdb 運行，佢會停喺當機嗰行，再 backtrace。",
          BulletCard("貼士", [("-g，唔好 -O2", "g"), ("step：行入函數", "s"), ("當機：gdb run，再 backtrace", "w")])),
    Scene("recap",
          "總結：[[r1]]用 D g 編譯；[[r2]]break 設停車位，run 開始；[[r3]]next 逐行，print 睇變數；[[r4]]backtrace 睇呼叫鏈，continue 行完。",
          BulletCard("今集重點", [("g++ -g", "r1"), ("break、run", "r2"), ("next、print", "r3"), ("backtrace、continue", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 gdb 停喺 factorial，每行 next 一次，再 print result，睇吓佢點樣變到一百二十。[[next]]下一集：單元測試。多謝收睇，下次見！",
          EndCard("break factorial、run，之後不斷 next 同 print result，睇 result 由 1 變到 120。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

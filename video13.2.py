#!/usr/bin/env python3
"""Video 150 (syllabus 13.2): 貪食蛇（二）：鍵盤同碰撞

Steering the snake: RawMode (an RAII struct) switches the terminal out of line mode and echo with
termios and restores it in its destructor; readKey() uses select() with a zero timeout so the
game never waits for a key. w/a/s/d turn (never straight back), q quits; hitting the wall or the
snake's own body ends the loop with "game over!". In the real run the player presses w and then a,
and the snake crashes into the left wall. Run `python3 video13.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 150
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "13-02"
FINAL = (CODE / "snake.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    return next(i + 1 for i in range(start - 1, len(LINES)) if text in LINES[i])


(c1, r1, cch, rch) = cpp.session({"snake.cpp": FINAL}, [
    "g++ -std=c++20 -O2 -Wall -Wextra snake.cpp -o sn", Input("./sn", [("w", 1.1), ("a", 1.9)]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", Input("./ch", [("p", 0.5), ("p", 1.5), ("q", 2.0)]),
], refresh=opts.fresh_runs, cols=58)
last = r1.output.split("\x1b[2J\x1b[H")[-1]
assert r1.output.rstrip().endswith("game over!") and "#Ooo" in last, last
assert c1.code == cch.code == 0 and "game over!" in rch.output

SAY = {"termios": "term i o s", "RawMode": "Raw Mode", "ICANON": "I CANON", "ECHO": "ECHO", "select": "select", "readKey": "read key",
       "RAII": "R A I I", "tcsetattr": "t c set attr", "w": "w", "a": "a", "s": "s", "d": "d", "q": "q", "dir": "dir", "isWall": "is wall",
       "std::ranges::find": "ranges find", "game over": "game over"}

s = Stage({"snake.cpp": FINAL}, title="貪食蛇（二）：鍵盤同碰撞", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集條蛇自己行，今集要用鍵盤控制佢，撞牆或者撞到自己就 game over。難位係：遊戲唔可以停低等你撳掣。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "termios · select · 碰撞")),
    Scene("goal",
          "今集會講：[[b1]]關閉 terminal 嘅行緩衝；[[b2]]唔等待咁讀鍵盤；[[b3]]用 w a s d 轉方向；[[b4]]撞牆同撞自己。",
          BulletCard("今集學識", [("RawMode：termios", "b1"), ("readKey：select 唔等", "b2"), ("w a s d 轉向", "b3"), ("碰撞 → game over", "b4")])),
    Scene("raw",
          "[[why]]平時 terminal 要你撳 Enter 先將成行交俾程式，仲會將你打嘅字顯示出嚟。[[on]]RawMode 用 termios 關咗呢兩樣；[[off]]解構子將設定還原：RAII，就算點樣離開都會還原，唔會整壞個 terminal。",
          s.scene(Open("snake.cpp", mode="instant"), Mark((ln("struct RawMode"), ln("RawMode() {") + 5), at="on"),
                  Mark((ln("~RawMode()"), ln("~RawMode()") + 2), at="off"))),
    Scene("key",
          "[[select]]readKey 用 select，而且等待時間係零：有鍵就讀一個，冇就即刻回傳零。咁遊戲迴圈每一 tick 問一次，唔會卡住。",
          s.scene(Mark((ln("char readKey()"), ln("return c;") + 1), at="select"))),
    Scene("turn",
          "[[keys]]w 上、s 下、a 左、d 右；[[back]]但係唔可以直接掉頭：向緊左右先可以轉上下。[[quit]]q 就離開。",
          s.scene(Mark((ln("char k = readKey();"), ln("dir = {1, 0};")), at="keys"), Mark(ln("if (k == 'w' && dir.y == 0)"), at="back"),
                  Mark((ln("} else if (k == 'q')"), ln("break;", ln("} else if (k == 'q')"))), at="quit"))),
    Scene("crash",
          "[[next]]計好新嘅頭之後，[[self]]用 ranges find 睇吓新頭係咪撞到自己嘅身；[[wall]]撞牆或者撞自己，就跳出迴圈，印 game over。",
          s.scene(Mark(ln("bool self = std::ranges::find"), at="self"), Mark((ln("if (isWall(head) || self)"), ln("if (isWall(head) || self)") + 2), at="wall"))),
    Scene("run",
          "[[cc]]編譯運行。蛇一開始向右行，我哋一齊睇住佢：[[w]]撳 w，佢轉咗向上，行到最頂嗰行；[[a]]再撳 a，轉左，一路沿住頂行過去，冇再撳掣……[[o]]就撞落左邊嘅牆，game over！程式離開，terminal 亦都還原返正常。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("w", "a"), type_rate=6))),
    Scene("recap",
          "總結：[[r1]]termios 關閉行緩衝同回顯，RAII 負責還原；[[r2]]select 加零等待，讀鍵盤唔會卡住；[[r3]]唔可以直接掉頭；[[r4]]新頭撞牆或者撞身就完。",
          BulletCard("今集重點", [("RawMode：termios + RAII", "r1"), ("select 零等待", "r2"), ("唔准掉頭", "r3"), ("撞牆 / 撞身 → 完", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個暫停掣：撳 p 停低，再撳 p 繼續。[[next]]下一集：食物、分數、加速，同埋最高分。多謝收睇，下次見！",
          EndCard("加 p：撳一次就停（不斷 readKey 直到再撳 p），再撳一次繼續。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

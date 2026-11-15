#!/usr/bin/env python3
"""Video 149 (syllabus 13.1): 貪食蛇（一）：遊戲迴圈

The game loop for a terminal Snake: a 20 × 10 board, the snake as a std::deque<Point> (head at the
front), and each tick: move (push_front a new head, pop_back the tail), draw, sleep 200 ms. draw()
builds the whole frame in a string that starts with the ANSI codes ESC[2J ESC[H (clear the screen,
cursor home), so every frame replaces the last. The real run animates the snake moving right for
13 ticks. Run `python3 video13.1.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 149
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "13-01"
FINAL = (CODE / "snake.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text):
    return next(i + 1 for i, l in enumerate(LINES) if text in l)


(c1, r1, cch, rch) = cpp.session({"snake.cpp": FINAL}, [
    "g++ -std=c++20 -O2 -Wall -Wextra snake.cpp -o sn", Input("./sn", []),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", Input("./ch", []),
], refresh=opts.fresh_runs, cols=58)
last = r1.output.split("\x1b[2J\x1b[H")[-1]
assert r1.output.count("\x1b[2J") == 13 and "#               ooO#" in last and r1.seconds > 2.4, last
assert c1.code == cch.code == 0 and rch.output.count("\x1b[2J") == 5

SAY = {"deque": "deque", "std::deque<Point>": "deque Point", "Point": "Point", "Snake": "Snake", "push_front": "push front",
       "pop_back": "pop back", "draw": "draw", "isWall": "is wall", "ANSI": "A N S I", "\\x1b[2J": "清畫面", "tick": "tick", "200ms": "二百毫秒",
       "sleep_for": "sleep for", "O": "大楷 O", "o": "細楷 o", "game loop": "game loop"}

s = Stage({"snake.cpp": FINAL}, title="貪食蛇（一）：遊戲迴圈", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！最後一部分係綜合項目。頭三集喺 terminal 寫一個貪食蛇遊戲。第一集先整遊戲迴圈：一條自己識行嘅蛇。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "遊戲迴圈 · ANSI · deque")),
    Scene("plan",
          "三集嘅計劃：[[b1]]今集：遊戲迴圈同畫畫面；[[b2]]下集：鍵盤控制同碰撞；[[b3]]第三集：食物、分數、加速，同埋儲存最高分。",
          BulletCard("貪食蛇三集", [("13.1 遊戲迴圈、畫畫面", "b1"), ("13.2 鍵盤、碰撞", "b2"), ("13.3 分數、加速、最高分", "b3")])),
    Scene("loop",
          "所有遊戲嘅核心都係一個迴圈：[[input]]讀輸入，[[update]]更新狀態，[[draw]]畫畫面，[[wait]]等一陣，再嚟過。今集未有輸入，蛇自己行。",
          TableCard("遊戲迴圈", ["步驟", "貪食蛇"], [
              (["① 輸入", "（下一集）"], "input"),
              (["② 更新", "蛇向前一格"], "update"),
              (["③ 畫", "清畫面，畫格仔"], "draw"),
              (["④ 等", "sleep 200 毫秒"], "wait"),
          ], widths=[0.8, 1.8], code_cols=(), size=40)),
    Scene("data",
          "[[board]]地圖二十乘十。[[point]]Point 係一個格仔，有 x 同 y，用 default 嘅等於號比較。[[snake]]蛇係一條 deque：前面係頭，後面係尾，兩頭加減都快，8.10 講過。[[wall]]isWall 判斷係咪圍牆。",
          s.scene(Open("snake.cpp", mode="instant"), Mark((ln("const int W"), ln("const int H")), at="board"), Mark((ln("struct Point"), ln("};")), at="point"),
                  Mark(ln("using Snake"), at="snake"), Mark((ln("bool isWall"), ln("bool isWall") + 2), at="wall"))),
    Scene("draw",
          "[[clear]]draw 先寫兩個 ANSI 控制碼：清畫面，同埋將游標移返左上角。[[cells]]然後逐格決定畫乜：圍牆係井號，蛇頭係大楷 O，身係細楷 o。[[once]]成個畫面砌好喺一個 string，最後一次過印，就唔會閃。",
          s.scene(Mark(ln('std::string out = "\\x1b[2J\\x1b[H";'), at="clear"), Mark((ln("char c = isWall"), ln("c = i == 0 ?")), at="cells"),
                  Mark(ln("std::cout << out << std::flush;"), at="once"))),
    Scene("move",
          "[[dir]]dir 係方向，一開始向右。[[head]]每一 tick：新嘅頭等於舊頭加方向，[[push]]push_front 加去前面，pop_back 拎走尾，蛇就向前行咗一格，長度唔變。[[sleep]]畫完等二百毫秒。",
          s.scene(Mark(ln("Point dir{1, 0};"), at="dir"), Mark((ln("Point head = snake.front();"), ln("head.y += dir.y;")), at="head"),
                  Mark((ln("snake.push_front(head);"), ln("snake.pop_back();")), at="push"), Mark(ln("sleep_for(200ms)"), at="sleep"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]蛇喺地圖入面一格格咁向右行，十三步之後停。下一集就可以用鍵盤控制佢。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("recap",
          "總結：[[r1]]遊戲迴圈：輸入、更新、畫、等；[[r2]]ANSI 碼清畫面，每個畫面蓋過上一個；[[r3]]deque 做蛇：前面加頭，後面去尾；[[r4]]成個畫面砌好先一次過印。",
          BulletCard("今集重點", [("輸入 → 更新 → 畫 → 等", "r1"), ("\\x1b[2J\\x1b[H 清畫面", "r2"), ("deque：push_front / pop_back", "r3"), ("一次過印", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將蛇放喺上面中間，改做向下行五步。[[next]]下一集：鍵盤控制同碰撞。多謝收睇，下次見！",
          EndCard("蛇由 (10, 3) 開始，dir 改做 {0, 1}，向下行 5 步。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

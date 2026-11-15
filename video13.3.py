#!/usr/bin/env python3
"""Video 151 (syllabus 13.3): 貪食蛇（三）：分數同收尾

The finished Snake: food appears at a fixed list of places (so the demo can be repeated); eating
grows the snake (no pop_back that tick), adds a point and shortens the delay (faster, down to
80 ms). At the end the best score is read from best.txt and written back when beaten. Real run 1:
the snake eats twice, crashes into the top wall: "game over! score 2 best 2". Real run 2 (no keys):
eats once, hits the right wall: "game over! score 1 best 2"; `cat best.txt` shows 2.
Run `python3 video13.3.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 151
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "13-03"
FINAL = (CODE / "snake.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    return next(i + 1 for i in range(start - 1, len(LINES)) if text in LINES[i])


(c1, r1, clr, r2, cat, cch, rch) = cpp.session({"snake.cpp": FINAL}, [
    "g++ -std=c++20 -O2 -Wall -Wextra snake.cpp -o sn", Input("./sn", [("w", 1.26)]), "clear", Input("./sn", []), "cat best.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", Input("./ch", []),
], refresh=opts.fresh_runs, cols=58)
assert r1.output.rstrip().endswith("game over! score 2 best 2"), r1.output[-200:]
assert r2.output.rstrip().endswith("game over! score 1 best 2") and cat.output.strip() == "2"
assert c1.code == cch.code == 0 and "game over! score 1 best 2" in rch.output

SAY = {"foods": "foods", "food": "food", "score": "score", "delay": "delay", "best.txt": "best 點 t x t", "best": "best", "std::max": "S T D max",
       "pop_back": "pop back", "push_front": "push front", "ifstream": "i f stream", "ofstream": "o f stream", "game over": "game over",
       "80": "八十", "cat": "cat", "raylib": "raylib"}

s = Stage({"snake.cpp": FINAL}, title="貪食蛇（三）：分數同收尾", code_px=19)

scenes = [
    Scene("intro",
          "歡迎返嚟！貪食蛇最後一集：加食物、分數、越食越快，同埋將最高分儲落檔案，下次再玩都記得。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "食物 · 分數 · 加速 · 最高分")),
    Scene("goal",
          "今集會講：[[b1]]食物同變長；[[b2]]分數同加速；[[b3]]儲存最高分；[[b4]]成個遊戲用咗乜。",
          BulletCard("今集學識", [("食到：唔 pop_back，變長", "b1"), ("score++、delay 縮短", "b2"), ("best.txt", "b3"), ("全課程嘅技巧", "b4")])),
    Scene("food",
          "[[list]]食物出現嘅位置用一個固定嘅清單，咁示範可以重複；真遊戲可以用隨機數。[[draw]]draw 將食物畫成星號，最底再印分數。",
          s.scene(Open("snake.cpp", mode="instant"), Mark(ln("const Point foods[]"), at="list"),
                  Mark((ln("if (food == Point{x, y})"), ln("c = '*';")), at="draw"))),
    Scene("eat",
          "[[push]]每步照樣喺前面加新頭。[[ate]]如果新頭就係食物：分數加一，換下一粒食物，[[fast]]delay 減十五毫秒，最快八十毫秒；[[grow]]而且今次唔 pop_back，條蛇就長咗一格。冇食到先 pop_back。",
          s.scene(Mark(ln("snake.push_front(head);"), at="push"), Mark((ln("if (head == food)"), ln("food = foods[next];")), at="ate"),
                  Mark(ln("delay = std::max(80, delay - 15);"), at="fast"), Mark((ln("} else {", ln("delay = std::max")), ln("snake.pop_back();")), at="grow"))),
    Scene("best",
          "[[read]]遊戲完咗，用 ifstream 讀 best.txt；第一次冇呢個檔，best 就保持零。[[write]]今次分數高過紀錄，就用 ofstream 寫返落去。[[show]]最後印分數同最高分。",
          s.scene(Mark((ln("int best = 0;"), ln('std::ifstream("best.txt") >> best;')), at="read"), Mark((ln("if (score > best)"), ln('std::ofstream("best.txt")')), at="write"),
                  Mark((ln('std::cout << "game over! score "'), ln('std::cout << " best "')), at="show"))),
    Scene("run1",
          "[[cc]]編譯運行。[[go]]蛇向右行，食第一粒；[[w]]撳 w 轉上，食埋第二粒，越嚟越快，最後撞到頂嘅牆：兩分，最高分兩分。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="go", keys=("w",), type_rate=6))),
    Scene("run2",
          "[[again]]再玩一次，今次乜都唔撳：食到一粒，就撞向右邊嘅牆。[[o]]一分，但係最高分仲係兩分，[[cat]]best.txt 入面都係二。",
          s.scene(Run(clr, at="again"), Run(r2, at="again"), Run(cat, at="cat"))),
    Scene("parts",
          "呢個遊戲用咗成個課程嘅嘢：[[a]]struct 同運算子；[[b]]deque 同 ranges；[[c]]RAII 還原 terminal；[[d]]檔案讀寫；[[e]]chrono 同 thread 控制速度。",
          TableCard("貪食蛇用咗乜", ["技巧", "喺邊度"], [
              (["struct + operator== = default", "Point"], "a"),
              (["deque、ranges::find", "蛇、撞自己"], "b"),
              (["RAII", "RawMode"], "c"),
              (["ifstream / ofstream", "best.txt"], "d"),
              (["chrono + sleep_for", "速度"], "e"),
          ], widths=[1.7, 1.3], code_cols=(), size=34)),
    Scene("recap",
          "總結：[[r1]]食到就唔去尾，條蛇變長；[[r2]]分數加一，delay 縮短；[[r3]]最高分存喺檔案；[[r4]]一個細遊戲，已經用到好多 C++ 工具。",
          BulletCard("今集重點", [("食到：唔 pop_back", "r1"), ("score++、加速", "r2"), ("best.txt", "r3"), ("綜合運用", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將蛇一開始嘅長度改做五格。想再進一步，可以試吓 13.6 介紹嘅 raylib，整一個有圖像嘅版本。[[next]]下一集：圖書館管理系統。多謝收睇，下次見！",
          EndCard("將起始嘅蛇改做 5 格：{5,5} {4,5} {3,5} {2,5} {1,5}。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 138 (syllabus 12.6): 貪心

Activity selection: pick as many non-overlapping activities as possible from 7. Greedy by
earliest start really picks only 0-6 and 6-10 (count 2); greedy by earliest end picks 1-4, 5-7,
8-11 (count 3), which is optimal: the exchange argument explains why. The challenge is greedy
change-making with HK coins: 63 needs 4 coins. Run `python3 video138.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 138
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-06"
FINAL = (CODE / "greedy.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BAD = FINAL.replace("return a.end < b.end;", "return a.start < b.start;")
CC = "g++ -std=c++20 -O2 greedy.cpp -o gr"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"greedy.cpp": BAD, "in.txt": IN}, [
    CC, "./gr < in.txt", "clear", Write("greedy.cpp", FINAL), CC, "./gr < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "0-6 6-10 \ncount 2\n" and r2.output == "1-4 5-7 8-11 \ncount 3\n", (r1.output, r2.output)
assert c1.code == c2.code == cch.code == 0 and rch.output == "4\n"

SAY = {"lastEnd": "last end", "a.end": "a 點 end", "a.start": "a 點 start", "greedy": "greedy", "sort": "sort", "count": "count",
       "in.txt": "in 點 t x t", "exchange argument": "exchange argument"}

s = Stage({"greedy.cpp": BAD}, title="貪心", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！貪心法就係每一步都揀而家睇落最好嘅，唔回頭。佢好快，但係揀錯咗準則，答案就會錯。今集用排活動做例子。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "每步揀最好 · 排序 · 證明")),
    Scene("problem",
          "題目：[[p]]有七個活動，每個有開始同結束時間；[[goal]]一間房同一時間只可以搞一個，最多可以排到幾多個？",
          TableCard("七個活動", ["活動", "開始", "結束"], [
              (["A", "1", "4"], "p"), (["B", "3", "5"], "p"), (["C", "0", "6"], "p"), (["D", "5", "7"], "p"),
              (["E", "5", "9"], "goal"), (["F", "6", "10"], "goal"), (["G", "8", "11"], "goal"),
          ], widths=[0.8, 0.8, 0.8], code_cols=(), size=34)),
    Scene("bad",
          "[[sort]]第一個諗法：按開始時間排，邊個最早開始就揀邊個。[[pick]]之後只揀開始時間唔早過上一個結束嘅。[[cc]]運行：[[o]]零到六，六到十，得兩個。睇落好合理，但係真係最多咩？",
          s.scene(Open("greedy.cpp", mode="instant"), Mark((16, 18), at="sort"), Mark((21, 27), at="pick"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("fix",
          "[[why]]問題係 C 零到六好早開始，但係好遲先完，霸住成間房。[[type]]改做按結束時間排：邊個最早完就揀邊個，留最多時間俾後面。[[cc]]運行：[[o]]一到四、五到七、八到十一，三個。",
          s.scene(Note("C：最早開始，但係霸到六點", at="why", where="editor"), Note(None, at="type"), Run(clr, at="type"),
                  Replace("greedy.cpp", "return a.start < b.start;", "return a.end < b.end;", at="type", rate=20), Expect("greedy.cpp", FINAL),
                  Mark(17, at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("proof",
          "點知最早完一定啱？[[ex]]用交換論證：假設最好嘅答案第一個唔係最早完嗰個，[[swap]]將佢換做最早完嗰個，後面一樣排得落，數量冇少；[[so]]所以揀最早完，永遠唔會吃虧。",
          BulletCard("交換論證", [("假設最佳答案第一個係 X", "ex"), ("換做最早完嘅 A：A 完得更早", "swap"), ("後面照排得落：唔會差", "so")])),
    Scene("rules",
          "用貪心之前：[[sort]]通常要先排序，揀啱準則；[[test]]用細嘅例子試，搵反例；[[prove]]最好諗清楚點解啱。唔肯定嘅話，可能要用動態規劃，12.14 會講。",
          BulletCard("用貪心嘅步驟", [("排序：揀啱準則", "sort"), ("用細例子搵反例", "test"), ("諗清楚點解啱（或改用 DP）", "prove")])),
    Scene("recap",
          "總結：[[r1]]貪心每步揀當刻最好；[[r2]]準則好重要：按開始時間錯，按結束時間啱；[[r3]]用交換論證證明；[[r4]]排序加一次掃描，O n log n。",
          BulletCard("今集重點", [("每步揀最好", "r1"), ("準則：最早結束", "r2"), ("交換論證", "r3"), ("O(n log n)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用港幣硬幣同紙幣：五十、二十、十、五、二、一，用貪心法找六十三蚊，最少要幾多張或者個？[[next]]下一集：回溯。多謝收睇，下次見！",
          EndCard("面值 {50, 20, 10, 5, 2, 1}，每次揀最大面值，找 63：答案 4（50、10、2、1）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

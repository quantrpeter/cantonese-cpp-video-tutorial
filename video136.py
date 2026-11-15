#!/usr/bin/env python3
"""Video 136 (syllabus 12.4): 雙指針同滑動視窗

Longest run of consecutive numbers with sum ≤ k (all values non-negative): right moves forward
every step, left moves forward only while the window is too big. For 2 1 5 2 3 2 6 1 with k = 10
the real run prints 4 (the window 2 1 5 2). Each pointer only moves forward, so it is O(n).
The challenge counts pairs in a sorted array with two pointers from both ends (3).
Run `python3 video136.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 136
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-04"
FINAL = (CODE / "window.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"window.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 window.cpp -o win", "./win < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "4\n" and c1.code == cch.code == 0 and rch.output == "3\n"

SAY = {"left": "left", "right": "right", "sum": "sum", "best": "best", "k": "k", "O(n)": "O n", "O(n²)": "O n 二次方",
       "in.txt": "in 點 t x t", "cat": "cat", "two pointers": "two pointers", "sliding window": "sliding window"}

s = Stage({"window.cpp": FINAL}, title="雙指針同滑動視窗", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！搵一段連續嘅數，總和唔超過 k，最長可以有幾長？試晒所有開頭同結尾係 O n 二次方。今集學雙指針：兩隻手指一齊向前行，O n 搞掂。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "left · right · 只向前行")),
    Scene("goal",
          "今集會講：[[b1]]滑動視窗嘅諗法；[[b2]]right 擴大，left 收細；[[b3]]點解係 O n；[[b4]]另一種雙指針：兩頭向中間。",
          BulletCard("今集學識", [("滑動視窗", "b1"), ("right 擴大、left 收細", "b2"), ("O(n)", "b3"), ("兩頭向中間", "b4")])),
    Scene("code",
          "[[sum]]sum 係而家視窗入面嘅總和。[[right]]right 每次向前一格，將新嘅數加入視窗；[[shrink]]如果超過 k，就不斷將 left 嗰格拎走，left 向前；[[best]]之後視窗一定合法，記低最長嘅長度。",
          s.scene(Open("window.cpp", at="sum"), Mark(14, at="sum"), Mark((17, 18), at="right"), Mark((19, 22), at="shrink"), Mark(23, at="best"))),
    Scene("trace",
          "用 k 等於十試吓：[[a]]加二、一、五、二，啱啱十，長度四；[[b]]再加三，十三，太多，拎走二同一，剩五、二、三；[[c]]之後一路咁滑落去，最長都係四。",
          TableCard("k = 10", ["right 加入", "視窗", "sum", "長度"], [
              (["2 1 5 2", "2 1 5 2", "10", "4"], "a", GREEN),
              (["3", "5 2 3", "10", "3"], "b"),
              (["2", "2 3 2", "7", "3"], "c"),
              (["6", "2 6", "8", "2"], "c"),
          ], widths=[1.1, 1.3, 0.7, 0.7], code_cols=(), size=38)),
    Scene("run",
          "[[cat]]輸入檔：第一行係 n 等於八，k 等於十；第二行係八個數。[[cc]]編譯，用細過號讀入呢個檔，運行：[[o]]四，同我哋人手追蹤嘅一樣。",
          s.scene(Mark(None), Run(cat, at="cat"), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("why",
          "點解快？[[fwd]]left 同 right 都只會向前，唔會退後；[[count]]所以兩隻手指加埋最多行 2n 步，就係 O n。[[cond]]但係要所有數都唔係負數，加嘢先一定變大，呢個方法先成立。",
          BulletCard("點解係 O(n)", [("left、right 只向前", "fwd"), ("總共最多 2n 步", "count"), ("前提：數唔係負數", "cond")])),
    Scene("pairs",
          "另一種雙指針：[[sorted]]排好序嘅陣列，一隻手指喺頭，一隻喺尾；[[move]]兩個加埋太細，頭向右；太大，尾向左；啱啱好就記低。一樣係 O n。",
          BulletCard("兩頭向中間", [("排好序：i 喺頭、j 喺尾", "sorted"), ("太細 i++；太大 j--；啱就記低", "move")])),
    Scene("recap",
          "總結：[[r1]]滑動視窗：right 加入，超過就移 left；[[r2]]兩隻手指只向前，O n；[[r3]]數要唔係負數；[[r4]]排好序可以用兩頭向中間。",
          BulletCard("今集重點", [("right 加入、left 收細", "r1"), ("只向前：O(n)", "r2"), ("前提：非負", "r3"), ("排好序：兩頭向中間", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]排好序嘅一至六，用兩頭向中間嘅雙指針，數有幾多對加埋等於七。[[next]]下一集：二分答案。多謝收睇，下次見！",
          EndCard("{1, 2, 3, 4, 5, 6}：i 喺頭、j 喺尾，數 a[i] + a[j] == 7 嘅對數（答案 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

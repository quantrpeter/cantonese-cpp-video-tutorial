#!/usr/bin/env python3
"""Video 145 (syllabus 12.13): 並查集

Union-find (DSU): every element points to a parent; the root names the group. find() uses path
compression, unite() hangs the smaller tree under the bigger. With 6 people and the operations in
in.txt the real run answers no (0 and 3 apart), yes (after linking 1 and 2), no (4 and 5), and
"groups 3". The challenge detects the edge that closes a cycle (2-0). Run `python3 video12.13.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 145
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-13"
FINAL = (CODE / "dsu.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"dsu.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 -Wall -Wextra dsu.cpp -o dsu", "./dsu < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "no\nyes\nno\ngroups 3\n" and c1.code == cch.code == 0 and rch.output == "cycle at 2-0\n"

SAY = {"DSU": "D S U", "union-find": "union find", "find": "find", "unite": "unite", "parent": "parent", "size": "size", "iota": "iota",
       "path compression": "path compression", "U": "U", "Q": "Q", "in.txt": "in 點 t x t", "cat": "cat", "groups": "groups",
       "α(n)": "alpha n"}

s = Stage({"dsu.cpp": FINAL}, title="並查集", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！班上有人不斷交朋友，你想隨時知道兩個人係咪同一個朋友圈。每次都 DFS 一次太慢。今集學並查集：合併同查詢都幾乎係一步。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "find · unite · 路徑壓縮")),
    Scene("goal",
          "今集會講：[[b1]]用 parent 表示一棵樹；[[b2]]find 搵老大；[[b3]]路徑壓縮；[[b4]]unite 合併。",
          BulletCard("今集學識", [("parent：每人指住上司", "b1"), ("find：搵老大", "b2"), ("路徑壓縮", "b3"), ("unite：細樹掛去大樹", "b4")])),
    Scene("idea",
          "[[tree]]每個人有一個 parent，一路跟上去，去到指住自己嗰個就係老大。[[same]]兩個人老大一樣，就係同一個圈。[[merge]]合併兩個圈，只要將一個老大指去另一個老大。",
          BoxesCard("一個朋友圈 = 一棵樹", [
              BoxRow([Box("老大", "2", "parent[2] = 2", at="tree", color=GREEN, w=220, key="r")]),
              BoxRow([Box("", "3", "parent → 2", at="tree", w=200), Box("", "0", "parent → 2", at="same", w=200), Box("", "1", "parent → 0", at="same", w=200)], gap=40),
          ], notes=[("老大一樣 = 同一個圈", "same"), ("合併：老大指去另一個老大", "merge")], top=CONTENT_TOP + 10, row_h=250, box_h=110, size=40)),
    Scene("code",
          "[[init]]一開始每人都係自己嘅老大，iota 填零到 n 減一。[[find]]find 一路搵上去；[[compress]]搵到之後，順手將 parent 直接指去老大，叫路徑壓縮，下次一步就到。"
          "[[unite]]unite 先搵兩個老大，一樣就唔使做；唔一樣，就將細嗰棵掛去大嗰棵。",
          s.scene(Open("dsu.cpp", mode="instant"), Mark((6, 8), at="init"), Mark((9, 14), at="find"), Mark(11, at="compress"), Mark((15, 27), at="unite"))),
    Scene("run",
          "[[cat]]輸入：六個人，六個操作：U 係合併，Q 係問。[[cc]]編譯運行：[[o]]零同三，未合併，no；一同二合併之後，零同三連埋，yes；四同五，no。最後剩三個圈。",
          s.scene(Mark(None), Run(cat, at="cat"), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("cost",
          "[[fast]]有路徑壓縮，再加細樹掛大樹，每次操作平均差唔多係常數時間，比 DFS 快好多。[[uses]]用途：朋友圈、連通性、Kruskal 最小生成樹、判斷加邊會唔會成環。",
          BulletCard("並查集", [("find / unite：幾乎 O(1)", "fast"), ("連通、成環、最小生成樹", "uses")])),
    Scene("recap",
          "總結：[[r1]]parent 組成樹，老大代表一個集合；[[r2]]find 搵老大，順手路徑壓縮；[[r3]]unite 將細樹掛大樹；[[r4]]適合不斷合併、不斷問嘅題目。",
          BulletCard("今集重點", [("parent 樹，老大代表集合", "r1"), ("find + 路徑壓縮", "r2"), ("unite：細掛大", "r3"), ("合併 + 查詢", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]逐條加入邊：零一、一二、二零、二三，用並查集搵出邊一條邊令到圖出現環。[[next]]下一集：動態規劃入門。多謝收睇，下次見！",
          EndCard("逐條加邊 {0,1} {1,2} {2,0} {2,3}：兩端老大已經一樣，就係成環（答案 2-0）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 141 (syllabus 12.9): 圖嘅表示

A graph of 5 nodes and 5 undirected edges read from in.txt ("n m" then one edge per line), stored
two ways: an adjacency list (vector<vector<int>>) and an adjacency matrix (vector<vector<bool>>).
The real run prints each node's neighbours (1: 2 3 … 4: 2 3 5, 5: 4) and mat[2][3] mat[3][4] = 0 1.
The challenge finds the node with most neighbours (4, degree 3). Run `python3 video141.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 141
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-09"
FINAL = (CODE / "graph.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"graph.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 graph.cpp -o g", "./g < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch < in.txt",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "1: 2 3\n2: 1 4\n3: 1 4\n4: 2 3 5\n5: 4\n0 1\n" and c1.code == cch.code == 0 and rch.output == "4 3\n"

SAY = {"adj": "adj", "mat": "mat", "adjacency list": "adjacency list", "adjacency matrix": "adjacency matrix", "vector<vector<int>>": "vector 嘅 vector int",
       "push_back": "push back", "O(n²)": "O n 二次方", "O(n + m)": "O n 加 m", "O(1)": "O 一", "in.txt": "in 點 t x t", "cat": "cat", "MTR": "M T R"}

s = Stage({"graph.cpp": FINAL}, title="圖嘅表示", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！地鐵站同路線、朋友關係、網頁連結，都係圖：一堆點，同埋點之間嘅邊。之後幾集嘅 DFS、BFS、最短路都要先將圖讀入程式。今集講點樣表示一個圖。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "鄰接表 · 鄰接矩陣 · 讀邊")),
    Scene("goal",
          "今集會講：[[b1]]點同邊；[[b2]]常見嘅輸入格式；[[b3]]鄰接表；[[b4]]鄰接矩陣，同埋點揀。",
          BulletCard("今集學識", [("點、邊", "b1"), ("輸入：n m，再 m 條邊", "b2"), ("鄰接表", "b3"), ("鄰接矩陣 vs 鄰接表", "b4")])),
    Scene("picture",
          "[[nodes]]呢個圖有五個點，[[edges]]五條邊：一二、一三、二四、三四、四五。冇方向，即係一同二互相連住。",
          BoxesCard("5 個點、5 條邊", [
              BoxRow([Box("", "1", "", at="nodes", color=BLUE, w=110, key="n1")]),
              BoxRow([Box("", "2", "", at="nodes", color=BLUE, w=110, key="n2"), Box("", "3", "", at="nodes", color=BLUE, w=110, key="n3")], gap=260),
              BoxRow([Box("", "4", "", at="nodes", color=BLUE, w=110, key="n4")]),
              BoxRow([Box("", "5", "", at="nodes", color=BLUE, w=110, key="n5")]),
          ], arrows=[("n1", "n2", "edges", PURPLE), ("n1", "n3", "edges", PURPLE), ("n2", "n4", "edges", PURPLE), ("n3", "n4", "edges", PURPLE),
                     ("n4", "n5", "edges", PURPLE)], top=CONTENT_TOP - 20, row_h=160, box_h=80, size=40)),
    Scene("input",
          "[[cat]]輸入格式：第一行 n 同 m，即係點數同邊數；之後每行一條邊，兩個點。比賽通常就係咁俾。",
          s.scene(Open("graph.cpp", mode="instant"), Run(cat, at="cat"))),
    Scene("code",
          "[[adj]]鄰接表：每個點一個 vector，記住佢嘅鄰居。[[mat]]鄰接矩陣：n 乘 n 嘅表，有邊就係 true。[[read]]每讀一條邊，兩邊都要加，因為冇方向。[[print]]最後印出每個點嘅鄰居。",
          s.scene(Mark(7, at="adj"), Mark(8, at="mat"), Mark((9, 15), at="read"), Mark((16, 22), at="print"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]一嘅鄰居係二同三；四有三個鄰居：二、三、五。最後問矩陣：二同三有冇邊？零，冇；三同四？一，有。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("choose",
          "點揀？[[list]]鄰接表慳位，只記真正有嘅邊，行晒所有鄰居好快，大部分題目都用佢；[[matrix]]矩陣問兩點有冇邊係 O 一，但係要 n 二次方嘅位，n 細先用得。",
          TableCard("鄰接表 vs 鄰接矩陣", ["", "鄰接表", "鄰接矩陣"], [
              (["空間", "O(n + m)", "O(n²)"], "list"),
              (["u、v 有冇邊", "要搵", "O(1)"], "matrix"),
              (["適合", "大部分題目", "n ≤ 幾千"], "list", GREEN),
          ], widths=[1, 1.2, 1.2], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]圖由點同邊組成；[[r2]]輸入通常係 n、m，再 m 條邊；[[r3]]鄰接表 vector 嘅 vector，最常用；[[r4]]冇方向嘅邊，兩邊都要加。",
          BulletCard("今集重點", [("點 + 邊", "r1"), ("n m + m 條邊", "r2"), ("鄰接表：vector<vector<int>>", "r3"), ("無向：兩邊都加", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用同一個輸入，搵出邊個點嘅鄰居最多，印出佢同埋鄰居數目。[[next]]下一集：DFS 深度優先搜尋。多謝收睇，下次見！",
          EndCard("讀同一個 in.txt，搵 adj[u].size() 最大嘅點，印出點同度數（答案 4 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

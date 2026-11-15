#!/usr/bin/env python3
"""Video 143 (syllabus 12.11): BFS

Shortest number of steps through a 5 × 7 maze from S (top left) to E (bottom right): BFS with a
queue visits cells in order of distance, so the first time a cell is reached is the shortest.
`from` remembers where each cell was reached from, to draw the path. The real run prints steps 10
and the maze with the path marked by *. The challenge also counts reachable cells (26).
Run `python3 video143.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 143
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-11"
FINAL = (CODE / "maze.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    return next(i + 1 for i in range(start - 1, len(LINES)) if text in LINES[i])


(cat, c1, r1, cch, rch) = cpp.session({"maze.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 maze.cpp -o maze", "./maze < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", "./ch < in.txt",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "steps 10\nS.#....\n*##.##.\n***#...\n.#***#.\n...#**E\n", r1.output
assert c1.code == cch.code == 0 and rch.output.startswith("steps 10 reach 26\n")

SAY = {"BFS": "B F S", "queue": "queue", "dist": "dist", "from": "from", "dr": "d r", "dc": "d c", "-1": "負一", "in.txt": "in 點 t x t",
       "cat": "cat", "S": "S", "E": "E", "*": "星號", "DFS": "D F S", "O(R × C)": "O R 乘 C"}

s = Stage({"maze.cpp": FINAL}, title="BFS", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集 DFS 一條路行到盡，但係行到嘅唔一定係最短路。由 S 行去 E，最少要幾步？今集學 BFS，廣度優先搜尋：好似水波咁，一圈圈咁擴散。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "queue · 一圈圈擴散 · 最短步數")),
    Scene("goal",
          "今集會講：[[b1]]BFS 點解搵到最短；[[b2]]用 queue 實作；[[b3]]dist 同 from；[[b4]]畫返條路出嚟。",
          BulletCard("今集學識", [("一圈圈擴散", "b1"), ("queue", "b2"), ("dist、from", "b3"), ("畫出最短路", "b4")])),
    Scene("map",
          "[[cat]]迷宮：S 喺左上角，E 喺右下角，井號係牆。",
          s.scene(Open("maze.cpp", mode="instant"), Run(cat, at="cat"))),
    Scene("wave",
          "[[d0]]起點距離零；[[d1]]一步行到嘅格，距離一；[[d2]]再由佢哋行一步，距離二……[[first]]因為係按距離由近到遠處理，第一次去到某一格，就一定係最短距離。",
          BulletCard("一圈圈擴散", [("距離 0：起點", "d0"), ("距離 1：起點隔籬", "d1"), ("距離 2：再隔籬……", "d2"), ("第一次到 = 最短", "first")])),
    Scene("code",
          "[[dist]]dist 記住每格嘅距離，負一即係未去過；from 記住由邊格嚟。[[start]]起點放入 queue，距離零。[[loop]]每次由 queue 前面攞一格，[[dirs]]試四個方向：[[skip]]出界、撞牆、去過，就跳過；"
          "[[push]]否則距離加一，記低 from，放入 queue 尾。",
          s.scene(Mark(ln("vector<vector<int>> dist"), at="dist"), Mark((ln("q.push({0, 0});"), ln("dist[0][0] = 0;")), at="start"),
                  Mark((ln("while (!q.empty())"), ln("q.pop();")), at="loop"), Mark(ln("for (int k = 0; k < 4; k++)"), at="dirs"),
                  Mark((ln("if (nr < 0"), ln("if (g[nr][nc] == '#'") + 2), at="skip"), Mark((ln("dist[nr][nc] = dist[r][c] + 1;"), ln("q.push({nr, nc});")), at="push"))),
    Scene("path",
          "[[back]]搵完之後，由 E 跟住 from 一路行返去 S，沿途塗星號，就係最短路。",
          s.scene(Mark((ln("P cur = from[er][ec];"), ln("cur = from[cur.first]")), at="back"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]最少十步；星號就係條路：先向下，再向右，繞過啲牆去到 E。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("vs",
          "[[bfs]]BFS 用 queue，先近後遠，冇權重嘅最短路就用佢；[[dfs]]DFS 用遞迴或者 stack，行到盡，啱數連通、行晒所有可能。[[cost]]兩個都係每格行一次，O R 乘 C。",
          TableCard("BFS vs DFS", ["", "BFS", "DFS"], [
              (["工具", "queue", "遞迴 / stack"], "bfs"),
              (["次序", "由近到遠", "行到盡再退"], "dfs"),
              (["適合", "最少步數", "數島、連通、所有可能"], "dfs"),
          ], widths=[0.8, 1.2, 1.6], code_cols=(), size=38, note=("兩個都係 O(R × C)", "cost"))),
    Scene("recap",
          "總結：[[r1]]BFS 由近到遠一圈圈擴散；[[r2]]用 queue，dist 負一代表未去過；[[r3]]第一次去到就係最短；[[r4]]記住 from，就可以畫返條路。",
          BulletCard("今集重點", [("一圈圈擴散", "r1"), ("queue + dist", "r2"), ("第一次到 = 最短", "r3"), ("from：還原路徑", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]數吓由 S 出發，一共可以去到幾多格。提示：dist 唔係負一嘅就係去到。[[next]]下一集：Dijkstra，有權重嘅最短路。多謝收睇，下次見！",
          EndCard("BFS 之後數 dist != -1 嘅格（呢個迷宮係 26）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

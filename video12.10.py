#!/usr/bin/env python3
"""Video 142 (syllabus 12.10): DFS

Counting islands with a recursive depth-first flood fill: every unvisited '#' starts a new
island, and dfs() paints all land connected to it (up, down, left, right) with the island's
number. The real run on the 4 × 6 map prints the painted map (11..2. / 1...2. / ..33.. / .....4)
and 4. The challenge also reports the biggest island (3 cells). Run `python3 video12.10.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 142
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-10"
FINAL = (CODE / "islands.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cat, c1, r1, cch, rch) = cpp.session({"islands.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 islands.cpp -o isl", "./isl < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch < in.txt",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "11..2.\n1...2.\n..33..\n.....4\n4\n" and c1.code == cch.code == 0 and rch.output.endswith("4 3\n")

SAY = {"DFS": "D F S", "dfs": "D F S", "flood fill": "flood fill", "connected components": "connected components", "islands": "islands",
       "in.txt": "in 點 t x t", "cat": "cat", "#": "井號", "visited": "visited", "O(R × C)": "O R 乘 C", "stack overflow": "stack overflow"}

s = Stage({"islands.cpp": FINAL}, title="DFS", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！一張地圖，井號係陸地，點係海，有幾多個島？相連嘅陸地算同一個島。今集學 DFS，深度優先搜尋：沿住一條路行到盡，再退返嚟。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "深度優先 · flood fill · 數島")),
    Scene("goal",
          "今集會講：[[b1]]DFS 嘅諗法；[[b2]]遞迴版 DFS；[[b3]]flood fill 數島；[[b4]]連通分量。",
          BulletCard("今集學識", [("行到盡，再退返", "b1"), ("遞迴 dfs()", "b2"), ("flood fill：數島", "b3"), ("連通分量", "b4")])),
    Scene("map",
          "[[cat]]地圖：四行六列。一眼睇落：左上角一個，右邊一條，中間一個，右下角一粒，應該係四個島。",
          s.scene(Open("islands.cpp", mode="instant"), Run(cat, at="cat"))),
    Scene("dfs",
          "[[stop]]dfs 先檢查：出咗界，或者唔係未去過嘅陸地，就返。[[paint]]否則將呢格塗上島嘅編號，等於記住「去過」；[[four]]再向上下左右四個方向遞迴。一個島會被一口氣塗晒。",
          s.scene(Mark((8, 10), at="stop"), Mark(11, at="paint"), Mark((12, 15), at="four"))),
    Scene("count",
          "[[loop]]main 由左上角開始逐格睇：[[new]]見到仲未塗嘅井號，就係一個新島，島數加一，再由呢格開始 dfs，塗晒成個島。",
          s.scene(Mark((25, 32), at="loop"), Mark((27, 30), at="new"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]每個島都塗咗自己嘅編號：一號三格，二號兩格，三號兩格，四號一格。一共四個島。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("notes",
          "幾個重點：[[visit]]一定要標記去過，唔係會喺兩格之間不停來回，無限遞迴；[[cost]]每格最多去一次，所以係 O R 乘 C；[[deep]]地圖好大嘅時候，遞迴太深可能 stack overflow，可以改用自己嘅 stack，或者下一集嘅 BFS。",
          BulletCard("記住", [("一定要標記「去過」", "visit"), ("每格一次：O(R × C)", "cost"), ("太深：stack overflow → 用 stack / BFS", "deep")])),
    Scene("recap",
          "總結：[[r1]]DFS 沿一條路行到盡，再退返；[[r2]]遞迴寫法最簡單：檢查、標記、行四個方向；[[r3]]每次喺未去過嘅地方開始 DFS，就數到一個連通分量；[[r4]]記得防止重複去。",
          BulletCard("今集重點", [("行到盡再退", "r1"), ("檢查 → 標記 → 四方向", "r2"), ("新起點 = 新連通分量", "r3"), ("標記去過", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]改 dfs 令佢回傳塗咗幾多格，搵出最大嘅島有幾大。[[next]]下一集：BFS，搵最短步數。多謝收睇，下次見！",
          EndCard("int dfs(...)：回傳 1 + 四個方向嘅結果；記住最大值（呢張地圖係 3）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

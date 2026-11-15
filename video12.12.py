#!/usr/bin/env python3
"""Video 144 (syllabus 12.12): Dijkstra

Weighted shortest path on an MTR-style map: 6 stations, 8 links with made-up minutes. Dijkstra
keeps a min-heap (priority_queue with greater) of {distance, station}, always settles the closest
unsettled station, relaxes its links and skips stale heap entries. The real run prints
"19 min: Central Admiralty TST MongKok KowloonTong ShaTin". The challenge prints every station's
distance. Run `python3 video12.12.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 144
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-12"
FINAL = (CODE / "route.cpp").read_text()
IN = (CODE / "in.txt").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text, start=1):
    return next(i + 1 for i in range(start - 1, len(LINES)) if text in LINES[i])


(cat, c1, r1, cch, rch) = cpp.session({"route.cpp": FINAL, "in.txt": IN}, [
    "cat in.txt", "g++ -std=c++20 -O2 route.cpp -o route", "./route < in.txt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -O2 challenge.cpp -o ch", "./ch < in.txt",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "19 min: Central Admiralty TST MongKok KowloonTong ShaTin\n", r1.output
assert c1.code == cch.code == 0 and "KowloonTong 13\nShaTin 19\n" in rch.output

SAY = {"Dijkstra": "Dijkstra", "priority_queue": "priority queue", "greater<P>": "greater P", "dist": "dist", "from": "from",
       "INT_MAX": "int max", "relax": "relax", "Central": "中環", "Admiralty": "金鐘", "TST": "尖沙咀", "MongKok": "旺角",
       "KowloonTong": "九龍塘", "ShaTin": "沙田", "MTR": "港鐵", "in.txt": "in 點 t x t", "cat": "cat", "O((n + m) log n)": "O n 加 m log n"}

s = Stage({"route.cpp": FINAL}, title="Dijkstra", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！搭港鐵由中環去沙田，每段車程時間唔同，點樣搵最快嘅路線？BFS 只係數步數，唔理每步幾耐。今集學 Dijkstra：有權重嘅最短路。例子入面嘅分鐘係作嘅。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "priority_queue · 最近先處理")),
    Scene("goal",
          "今集會講：[[b1]]有權重嘅圖；[[b2]]Dijkstra 嘅諗法；[[b3]]用 priority_queue 實作；[[b4]]還原路線。",
          BulletCard("今集學識", [("邊有時間（權重）", "b1"), ("每次處理最近嘅站", "b2"), ("最小 heap", "b3"), ("from：還原路線", "b4")])),
    Scene("map",
          "[[cat]]輸入：六個站，八條路線；每條路線係兩個站加分鐘數，例如中環去金鐘二分鐘。",
          s.scene(Open("route.cpp", mode="instant"), Run(cat, at="cat"))),
    Scene("idea",
          "[[near]]Dijkstra 每次揀一個未處理、而家已知距離最短嘅站；[[fixed]]因為所有時間都唔係負數，佢嘅距離已經唔可能再短，可以定落嚟；[[relax]]再用佢去更新隔籬嘅站：經佢去會唔會快啲？",
          BulletCard("Dijkstra 嘅諗法", [("揀最近、未處理嘅站", "near"), ("佢嘅距離已經定（權重 ≥ 0）", "fixed"), ("更新鄰居：經佢會唔會快啲", "relax")])),
    Scene("code",
          "[[heap]]priority_queue 加 greater，就係最細先出嘅 heap，入面放距離同站。[[pop]]每次攞最近嗰個；[[stale]]如果佢嘅距離已經過時，即係之前搵到更短，就跳過。[[relax]]對每條路線：經呢個站更快，就更新距離同 from，再放入 heap。",
          s.scene(Mark((ln("vector<int> dist"), ln("priority_queue")), at="heap"), Mark((ln("auto [d, u] = pq.top();"), ln("pq.pop();")), at="pop"),
                  Mark((ln("if (d > dist[u])"), ln("if (d > dist[u])") + 2), at="stale"),
                  Mark((ln("for (auto [v, w] : adj[u])"), ln("pq.push({dist[v], v});")), at="relax"))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]十九分鐘：中環、金鐘、尖沙咀、旺角、九龍塘、沙田。由 ShaTin 跟 from 一路行返中環，再倒轉印，就係路線。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("rules",
          "記住：[[neg]]Dijkstra 只可以用喺權重唔係負數嘅圖；[[cost]]用 heap 嘅話，時間係 n 加 m 乘 log n；[[bfs]]如果每條邊都係一，直接用 BFS 就夠。",
          TableCard("最短路用邊個", ["情況", "演算法"], [
              (["每步一樣（冇權重）", "BFS：O(n + m)"], "bfs"),
              (["權重 ≥ 0", "Dijkstra：O((n + m) log n)"], "cost", GREEN),
              (["有負數權重", "唔可以用 Dijkstra"], "neg", RED),
          ], widths=[1.4, 1.8], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]每次處理最近、未處理嘅點；[[r2]]用最細先出嘅 priority_queue；[[r3]]過時嘅 heap 項目要跳過；[[r4]]記住 from 就可以還原路線。",
          BulletCard("今集重點", [("最近先處理", "r1"), ("priority_queue + greater", "r2"), ("跳過過時項目", "r3"), ("from 還原路線", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將每個站由中環出發嘅最短時間都印出嚟。[[next]]下一集：並查集。多謝收睇，下次見！",
          EndCard("Dijkstra 之後印出每個站嘅 dist（中環 0 … 沙田 19）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

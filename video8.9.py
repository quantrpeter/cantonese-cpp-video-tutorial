#!/usr/bin/env python3
"""Video 96 (syllabus 8.9): priority_queue

std::priority_queue<int> really pops 9 7 3 1 (biggest first, a max-heap); with
std::greater<int> as the third argument it pops 1 3 7 9 (a min-heap). Emergency-room triage
with pairs {level, name} really serves 5 Dan, 5 Ben, 3 Cat, 2 Amy: equal levels fall back to
comparing the names. Run `python3 video8.9.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 96
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-09"
NUMS = (CODE / "nums.cpp").read_text()
ER = (CODE / "er.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
MINQ = "std::priority_queue<int, std::vector<int>,\n                        std::greater<int>> pq;"
V1 = NUMS.replace(MINQ, "std::priority_queue<int> pq;")
CC = "g++ -std=c++20 -Wall -Wextra nums.cpp -o nums"

(c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"nums.cpp": V1, "er.cpp": ER}, [
    CC, "./nums", Write("nums.cpp", NUMS), CC, "./nums", "clear", "g++ -std=c++20 -Wall -Wextra er.cpp -o er", "./er",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "9 7 3 1 \n" and r2.output == "1 3 7 9 \n", (r1.output, r2.output)
assert r3.output == "5 Dan (breathing)\n5 Ben (heart)\n3 Cat (arm)\n2 Amy (cut)\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "1 3 5 \n"

SAY = {"std::priority_queue": "S T D priority queue", "priority_queue": "priority queue", "std::greater<int>": "S T D greater int",
       "std::greater": "S T D greater", "max-heap": "max heap", "min-heap": "min heap", "heap": "heap", "top()": "top", "pop()": "pop",
       "push": "push", "O(log n)": "O log n", "Amy": "Amy", "Ben": "Ben", "Cat": "Cat", "Dan": "Dan", "level": "level",
       "std::pair": "S T D pair"}

s = Stage({"nums.cpp": V1, "er.cpp": ER}, title="priority_queue", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！急症室唔係先到先得，而係最危急嘅病人先睇。呢種「永遠攞最重要嗰個」嘅需要，就用 std::priority_queue。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "最大先出 · std::greater · 分流")),
    Scene("goal",
          "今集會講：[[b1]]priority_queue 預設最大先出；[[b2]]用 std::greater 變成最細先出；[[b3]]heap 嘅概念；[[b4]]用 pair 做急症分流。",
          BulletCard("今集學識", [("預設：最大先出", "b1"), ("std::greater：最細先出", "b2"), ("heap", "b3"), ("pair：急症分流", "b4")])),
    Scene("max",
          "[[push]]將三、九、一、七逐個 push 入去。[[pop]]跟住不斷睇 top，再 pop。[[cc]]編譯運行，[[o]]九、七、三、一：每次 top 都係最大嗰個。",
          s.scene(Open("nums.cpp", at="push"), Mark((8, 10), at="push"), Mark((11, 14), at="pop"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("min",
          "想最細先出，[[type]]就要寫齊三個模板參數：元素係 int，底層用 vector int，比較用 std::greater int。[[cc]]運行，[[o]]一、三、七、九。",
          s.scene(Replace("nums.cpp", "std::priority_queue<int> pq;", MINQ, at="type", rate=30), Expect("nums.cpp", NUMS), Mark((7, 8), at="type"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("heap",
          "入面用嘅結構叫 heap：[[top]]最頂永遠係最大；[[tree]]每個格都大過佢下面嘅格，但係左右冇次序。[[cost]]所以 push 同 pop 都只係 O log n，攞 top 一步就得。",
          BoxesCard("max-heap", [
              BoxRow([Box("", "9", "top", at="top", color=GREEN, w=140, key="a")]),
              BoxRow([Box("", "7", "", at="tree", color=BLUE, w=140, key="b"), Box("", "1", "", at="tree", color=BLUE, w=140, key="c")], gap=160),
              BoxRow([Box("", "3", "", at="tree", color=BLUE, w=140, key="d")], gap=0),
          ], notes=[("push / pop：O(log n) · top：O(1)", "cost")], top=CONTENT_TOP - 20, row_h=215, box_h=90, size=44)),
    Scene("er",
          "[[open]]急症室：每個病人係一個 pair：危急程度，同埋名。[[cmp]]pair 會先比第一個，所以程度最高嘅先出。[[cc]]編譯運行：[[o]]五嘅兩個先，跟住三，最後二。最危急嘅永遠排第一。",
          s.scene(Run(clr, at="open"), Open("er.cpp", at="open"), Mark(7, at="open"), Mark((8, 11), at="cmp"), Mark(None, at="cc"),
                  Run(c3, at="cc"), Run(r3))),
    Scene("tie",
          "留意兩個都係五：[[same]]第一個一樣，pair 就比第二個，即係名。[[name]]Dan 嘅字母排喺 Ben 後面，算係大啲，所以 Dan 先。[[real]]真係要先到先得，就要加多一個到達次序。",
          TableCard("兩個都係 5 點比？", ["pair", "比較"], [
              (["{5, \"Dan …\"} vs {5, \"Ben …\"}", "first 一樣 → 比 second"], "same"),
              (["\"Dan\" > \"Ben\"", "Dan 先出"], "name", AMBER),
          ], widths=[1.6, 1.4], code_cols=(0,), size=38, note=("想先到先得：加一個到達編號", "real"))),
    Scene("recap",
          "總結：[[r1]]priority_queue 每次 top 都係最大；[[r2]]加 std::greater 就變最細先出；[[r3]]入面係 heap，push 同 pop 都快；[[r4]]用 pair 排優先次序，打和就比第二個。",
          BulletCard("今集重點", [("top()：最大", "r1"), ("std::greater：最細", "r2"), ("heap：O(log n)", "r3"), ("pair：打和比 second", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用最細先出嘅 priority_queue，印出八、三、九、一、五入面最細嘅三個。[[next]]下一集：deque 同 list。多謝收睇，下次見！",
          EndCard("用 min-heap 由 {8, 3, 9, 1, 5} 印出最細嘅三個：1 3 5。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

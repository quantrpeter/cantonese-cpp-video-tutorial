#!/usr/bin/env python3
"""Video 97 (syllabus 8.10): deque 同 list

std::deque grows at both ends and still has []: 1 2 3 4 | 1. Putting 200,000 ints at the front,
built with -O2: `time ./vf` (vector::insert at begin) really takes about 2.4 s, `time ./df`
(deque::push_front) about 0.002 s. std::list: inserting before an iterator keeps that iterator
valid (it still prints 4; list 0 1 2 3 4), but a list has no [] and walks slowly.
Run `python3 video8.10.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 97
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-10"
FILES = {f: (CODE / f).read_text() for f in ["deque.cpp", "vf.cpp", "df.cpp", "list.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()

(c1, r1, clr, cv, cd, tv, td, clr2, c3, r3, cch, rch) = cpp.session(FILES, [
    "g++ -std=c++20 -Wall -Wextra deque.cpp -o dq", "./dq", "clear",
    "g++ -std=c++20 -O2 vf.cpp -o vf", "g++ -std=c++20 -O2 df.cpp -o df", "time ./vf", "time ./df", "clear",
    "g++ -std=c++20 -Wall -Wextra list.cpp -o ls", "./ls",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "1 2 3 4 | 1\n" and r3.output == "4 | 0 1 2 3 4\n", (r1.output, r3.output)


def secs(r):
    return float(re.search(r"real\s+0m([\d.]+)s", r.output).group(1))


vs, ds = secs(tv), secs(td)
assert tv.output.startswith("199999\n") and td.output.startswith("199999\n") and vs > 100 * max(ds, 0.001), (vs, ds)
assert c1.code == cv.code == cd.code == c3.code == cch.code == 0 and rch.output == "2 8 3 \n"
ZH = dict(zip("0123456789", "零一二三四五六七八九"))
say_vs = "".join(ZH[c] for c in f"{vs:.1f}".split(".")[0]) + "點" + ZH[f"{vs:.1f}".split(".")[1]]

SAY = {"std::deque": "S T D deque", "deque": "deque", "std::list": "S T D list", "list": "list", "push_front": "push front",
       "push_back": "push back", "pop_front": "pop front", "insert": "insert", "v.begin()": "v 點 begin", "-O2": "O 二", "time": "time",
       "std::next": "S T D next", "vector": "vector"}

s = Stage(FILES, title="deque 同 list", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！vector 好多時都係最好嘅選擇，但係喺前面加嘢，佢就好慢。今集睇 deque 同 list：佢哋幾時贏 vector，幾時輸。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "兩頭加減 · 中間插入 · 預設用 vector")),
    Scene("goal",
          "今集會講：[[b1]]deque：兩頭都快；[[b2]]vector 喺前面加有幾慢；[[b3]]list：中間插入，iterator 唔失效；[[b4]]幾時揀邊個。",
          BulletCard("今集學識", [("deque：兩頭 push", "b1"), ("實測：前面加 20 萬個", "b2"), ("list：插入唔失效", "b3"), ("點揀", "b4")])),
    Scene("deque",
          "[[open]]deque 好似 vector，[[front]]但係多咗 push_front，喺前面加都好快。[[idx]]而且一樣有中括號。[[cc]]編譯運行，[[o]]一二三四：一喺前面，四喺後面；第零個係一。",
          s.scene(Open("deque.cpp", at="open"), Mark(5, at="open"), Mark((6, 7), at="front"), Mark(11, at="idx"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("bench",
          "有幾快？[[open]]vf.cpp 用 vector，喺最前面 insert 二十萬次；[[d]]df.cpp 用 deque，push_front 二十萬次，其他完全一樣。[[cc]]兩個都用 O 二編譯，即係叫編譯器盡量優化，咁比較先公平。編譯好之後，就用 time 嚟計時。",
          s.scene(Run(clr, at="open"), Open("vf.cpp", at="open"), Mark(7, at="open"), Open("df.cpp", at="d"), Mark(7, at="d"), Mark(None, at="cc"),
                  Run(cv, at="cc"), Run(cd))),
    Scene("time",
          f"[[cc]]用 time 計時。[[v]]vector 用咗 {say_vs} 秒，要等一陣；[[q]]deque 幾乎係零秒，一下就完。相差成千倍。",
          s.scene(Run(tv, at="cc"), Run(td, at="q"))),
    Scene("why",
          "[[vec]]vector 嘅元素一定連埋一齊，喺前面加一個，後面全部要搬一格；二十萬次，就搬咗二百億次。[[dq]]deque 用一段段嘅記憶體，兩頭都有位，唔使搬。",
          TableCard("喺前面加一個", ["容器", "要做乜"], [
              (["vector", "全部元素向後搬一格：O(n)"], "vec", RED),
              (["deque", "前面一段有位，直接放：O(1)"], "dq", GREEN),
          ], widths=[0.8, 2], code_cols=(0,), size=40)),
    Scene("list",
          "[[open]]list 係一粒粒用指標連住嘅節點。[[it]]it 指住四；[[ins]]喺四前面 insert 三，再喺最前面加零。[[cc]]運行：[[o]]it 仲係指住四，冇失效；成條係零到四。"
          "記得 8.3 嘅 vector，加嘢之後 iterator 可能會失效。",
          s.scene(Run(clr2, at="open"), Open("list.cpp", at="open"), Mark(6, at="open"), Mark(7, at="it"), Mark((8, 9), at="ins"), Mark(None, at="cc"),
                  Run(c3, at="cc"), Run(r3))),
    Scene("choose",
          "點揀？[[v]]預設用 vector：連續記憶體，行得最快；[[d]]要喺兩頭加減，就用 deque；[[l]]要喺中間大量插入刪除，又要 iterator 唔失效，先考慮 list。"
          "[[cost]]但係 list 冇中括號，行一次都慢好多。",
          TableCard("點揀容器？", ["容器", "強項", "弱點"], [
              (["vector", "連續、最快、有 []", "前面加：慢"], "v", GREEN),
              (["deque", "兩頭加減都快、有 []", "唔係完全連續"], "d"),
              (["list", "中間插入；iterator 唔失效", "冇 []；行得慢"], "l"),
          ], widths=[0.8, 1.7, 1.4], code_cols=(0,), size=36, note=("唔肯定：用 vector", "cost"))),
    Scene("recap",
          "總結：[[r1]]vector 喺前面加係 O n，好慢；[[r2]]deque 兩頭都係 O 一，仲有中括號；[[r3]]list 插入唔令 iterator 失效，但係冇中括號；[[r4]]預設用 vector。",
          BulletCard("今集重點", [("vector 前面加：O(n)", "r1"), ("deque：兩頭 O(1)", "r2"), ("list：iterator 穩定，冇 []", "r3"), ("預設 vector", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 deque 做一個只記住最後三個數嘅窗口：新數 push_back，多過三個就 pop_front。[[next]]下一集：lambda。多謝收睇，下次見！",
          EndCard("用 std::deque 做「最後三個」窗口：逐個 push_back {5, 1, 4, 2, 8, 3}，size > 3 就 pop_front；最後應該係 2 8 3。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 139 (syllabus 12.7): 回溯

Backtracking = choose, recurse, un-choose. Permutations of 1..3 really print
123 132 213 231 312 321. N-Queens places one queen per row, skips unsafe columns, and undoes by
overwriting: the real counts are 4: 2, 5: 10, 6: 4, 7: 40, 8: 92. The challenge lists all 8
subsets of {1, 2, 3}. Run `python3 video12.7.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 139
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-07"
FILES = {f: (CODE / f).read_text() for f in ["perm.cpp", "queens.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()

(cp, rp, clr, cq, rq, cch, rch) = cpp.session(FILES, [
    "g++ -std=c++20 -O2 perm.cpp -o perm", "./perm", "clear", "g++ -std=c++20 -O2 queens.cpp -o q", "./q",
    Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert rp.output == "123 132 213 231 312 321 \n" and rq.output == "4: 2\n5: 10\n6: 4\n7: 40\n8: 92\n"
assert cp.code == cq.code == cch.code == 0 and rch.output == "{} {3} {2} {23} {1} {13} {12} {123} \n"

SAY = {"permute": "permute", "used": "used", "cur": "cur", "push_back": "push back", "pop_back": "pop back", "N-Queens": "N 皇后",
       "safe": "safe", "place": "place", "col": "col", "abs": "abs", "subsets": "subsets", "backtracking": "backtracking"}

s = Stage(FILES, title="回溯", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！有啲題目要試晒所有可能：所有排列、所有組合、所有擺法。回溯法就係一步步揀，揀到死路就退返一步，再試下一個。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "揀 · 遞迴 · 退返")),
    Scene("goal",
          "今集會講：[[b1]]回溯三步曲；[[b2]]全排列；[[b3]]N 皇后；[[b4]]剪枝。",
          BulletCard("今集學識", [("揀 → 遞迴 → 退返", "b1"), ("全排列", "b2"), ("N 皇后", "b3"), ("剪枝：死路早啲停", "b4")])),
    Scene("perm",
          "[[done]]cur 已經有 n 個數，就印出嚟。[[loop]]否則試每一個未用過嘅數：[[choose]]揀佢：標記 used，放入 cur；[[rec]]遞迴揀下一個；[[undo]]返嚟之後退返：拎走，取消標記。",
          s.scene(Open("perm.cpp", mode="instant"), Mark((8, 14), at="done"), Mark((15, 16), at="loop"), Mark((17, 18), at="choose"), Mark(19, at="rec"),
                  Mark((20, 21), at="undo"))),
    Scene("run1",
          "[[cc]]編譯運行：[[o]]一二三、一三二……三二一，六個排列。[[tree]]每一層揀一個數，好似行一棵樹，行到葉就印，然後退返去試另一條枝。",
          s.scene(Mark(None), Run(cp, at="cc"), Run(rp, at="o"))),
    Scene("tree",
          "[[l1]]第一層揀一、二或者三；[[l2]]第二層揀剩低嘅；[[l3]]第三層只剩一個。一共三乘二乘一，六個。",
          BoxesCard("排列樹", [
              BoxRow([Box("", "1", "", at="l1", color=BLUE, w=120), Box("", "2", "", at="l1", color=BLUE, w=120), Box("", "3", "", at="l1", color=BLUE, w=120)], gap=200),
              BoxRow([Box("", "12", "", at="l2", w=110), Box("", "13", "", at="l2", w=110), Box("", "21", "", at="l2", w=110), Box("", "23", "", at="l2", w=110),
                      Box("", "31", "", at="l2", w=110), Box("", "32", "", at="l2", w=110)], gap=20),
              BoxRow([Box("", "123", "", at="l3", color=GREEN, w=110), Box("", "132", "", at="l3", color=GREEN, w=110), Box("", "213", "", at="l3", color=GREEN, w=110),
                      Box("", "231", "", at="l3", color=GREEN, w=110), Box("", "312", "", at="l3", color=GREEN, w=110), Box("", "321", "", at="l3", color=GREEN, w=110)], gap=20),
          ], top=CONTENT_TOP, row_h=190, box_h=90, size=38)),
    Scene("queens",
          "N 皇后：[[rule]]n 乘 n 嘅棋盤放 n 隻皇后，唔可以同行、同列、同斜線。[[row]]每行放一隻，col row 記住佢喺邊列。[[safe]]safe 檢查前面每一行：同列，或者行差等於列差，即係同斜線，就唔得。"
          "[[prune]]唔安全就唔遞迴落去，呢個就係剪枝。",
          s.scene(Run(clr, at="rule"), Open("queens.cpp", at="rule"), Mark(5, at="row"), Mark((8, 15), at="safe"), Mark((22, 27), at="prune"))),
    Scene("run2",
          "[[cc]]編譯運行：[[o]]四乘四有兩個擺法，五乘五有十個，六有四個，七有四十個，八皇后有九十二個。",
          s.scene(Mark(None), Run(cq, at="cc"), Run(rq, at="o"))),
    Scene("recap",
          "總結：[[r1]]回溯就係揀、遞迴、退返；[[r2]]行到底就記低一個答案；[[r3]]剪枝：唔得就唔好再行落去；[[r4]]數量增長好快，只可以用喺 n 細嘅題目。",
          BulletCard("今集重點", [("揀 → 遞迴 → 退返", "r1"), ("到底：一個答案", "r2"), ("剪枝", "r3"), ("n 要細（≈ 20 以下）", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用回溯列出一、二、三嘅所有子集：每個數揀或者唔揀，一共八個。[[next]]下一集：位元運算。多謝收睇，下次見！",
          EndCard("subsets(i)：先唔揀 items[i] 遞迴，再揀佢遞迴，最後退返；{1, 2, 3} 一共 8 個子集。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

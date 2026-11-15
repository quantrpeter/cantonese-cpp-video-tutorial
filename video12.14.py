#!/usr/bin/env python3
"""Video 146 (syllabus 12.14): 動態規劃入門

Climbing n stairs one or two steps at a time: ways(n) = ways(n-1) + ways(n-2). For n = 40 the plain
recursion really makes 331,160,281 calls; with memoisation it makes 79; the bottom-up table needs
no recursion at all and also gives n = 90 instantly (4660046610375530309). All three print
165580141. The challenge allows steps of 1, 2 or 3 (274 ways for 10 stairs).
Run `python3 video12.14.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 146
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "12-14"
FINAL = (CODE / "stairs.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LINES = FINAL.split("\n")


def ln(text):
    return next(i + 1 for i, l in enumerate(LINES) if text in l)


(c1, r1, cch, rch) = cpp.session({"stairs.cpp": FINAL}, [
    "g++ -std=c++20 -O2 stairs.cpp -o st", "time ./st", Write("challenge.cpp", CHALLENGE), "g++ -O2 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output.startswith("plain    165580141 calls 331160281\nremember 165580141 calls 79\ntable    165580141\nn=90     4660046610375530309\n"), r1.output
assert c1.code == cch.code == 0 and rch.output == "274\n"

SAY = {"DP": "D P", "dp": "D P", "memo": "memo", "plain": "plain", "remember": "remember", "table": "table", "calls": "calls",
       "memoisation": "memoisation", "tabulation": "tabulation", "O(2ⁿ)": "O 二的 n 次方", "O(n)": "O n", "-1": "負一", "time": "time"}

s = Stage({"stairs.cpp": FINAL}, title="動態規劃入門", code_px=20)

scenes = [
    Scene("intro",
          "歡迎返嚟！行樓梯，每次可以行一級或者兩級，行四十級有幾多種行法？直接遞迴要行幾億次。今集學動態規劃：記住做過嘅答案，唔好重複計。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "記憶化 · 列表 · 行樓梯")),
    Scene("goal",
          "今集會講：[[b1]]搵出遞推式；[[b2]]直接遞迴有幾慢；[[b3]]記憶化；[[b4]]由細到大填表。",
          BulletCard("今集學識", [("ways(n) = ways(n−1) + ways(n−2)", "b1"), ("直接遞迴：重複計", "b2"), ("記憶化", "b3"), ("填表", "b4")])),
    Scene("formula",
          "[[last]]最後一步，要麼由 n 減一行一級上嚟，要麼由 n 減二行兩級上嚟。[[sum]]所以行法數就係兩者相加。[[base]]零級同一級，都只有一種行法。",
          BulletCard("遞推式", [("最後一步：由 n−1 或者 n−2 嚟", "last"), ("ways(n) = ways(n−1) + ways(n−2)", "sum"), ("ways(0) = ways(1) = 1", "base")])),
    Scene("plain",
          "[[fn]]plain 直接照公式遞迴，calls 數吓叫咗幾多次。[[tree]]問題係同一個 n 會被計好多次：計四十要計三十九同三十八，計三十九又再計三十八……",
          s.scene(Open("stairs.cpp", mode="instant"), Mark((ln("long long plain"), ln("return plain(n - 1)") + 1), at="fn"))),
    Scene("memo",
          "[[memo]]記憶化：開一個 memo，負一代表未計過。[[check]]計之前先睇有冇答案，有就直接用；[[store]]冇就計，計完記低。每個 n 只會真正計一次。",
          s.scene(Mark(ln("vector<long long> memo"), at="memo"), Mark((ln("if (memo[n] != -1)"), ln("return memo[n];")), at="check"),
                  Mark(ln("return memo[n] ="), at="store"))),
    Scene("table",
          "[[dp]]或者反過嚟，由細到大填表：dp 零同 dp 一係一，[[loop]]之後每格等於前兩格相加。冇遞迴，一個迴圈搞掂。",
          s.scene(Mark((ln("vector<long long> dp(n + 1);"), ln("dp[0] = dp[1] = 1;")), at="dp"), Mark((ln("for (int i = 2; i <= n; i++)"), ln("dp[i] = dp[i - 1]")), at="loop"))),
    Scene("run",
          "[[cc]]編譯，用 time 運行：[[o]]三個方法答案一樣，一億六千五百萬幾種行法。但係直接遞迴叫咗三億三千萬次；記憶化只係七十九次。填表仲可以一下計到九十級。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("steps",
          "動態規劃四步：[[state]]定義狀態：dp i 代表乜；[[trans]]搵轉移：dp i 由邊幾格嚟；[[base]]起點；[[order]]計算次序：由細到大，或者遞迴加記憶化。",
          TableCard("DP 四步", ["步驟", "行樓梯"], [
              (["狀態", "dp[i] = 行到第 i 級嘅方法數"], "state"),
              (["轉移", "dp[i] = dp[i-1] + dp[i-2]"], "trans"),
              (["起點", "dp[0] = dp[1] = 1"], "base"),
              (["次序", "i 由 2 到 n"], "order"),
          ], widths=[0.8, 2.2], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]先搵遞推式；[[r2]]直接遞迴會重複計，指數級咁慢；[[r3]]記憶化：計過就記低；[[r4]]填表：由細到大，O n。",
          BulletCard("今集重點", [("遞推式", "r1"), ("直接遞迴：重複計", "r2"), ("記憶化", "r3"), ("填表：O(n)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]如果每次可以行一、二或者三級，行十級有幾多種行法？[[next]]下一集：經典動態規劃。多謝收睇，下次見！",
          EndCard("每步可以行 1、2 或 3 級：dp[i] = dp[i−1] + dp[i−2] + dp[i−3]；10 級有 274 種。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

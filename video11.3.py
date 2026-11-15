#!/usr/bin/env python3
"""Video 128 (syllabus 11.3): atomic

Two threads each add 1,000,000 to a counter, built with -O2. std::atomic<int> and a mutex-guarded
int both reach 2000000, but the real timings differ a lot (the numbers spoken are the measured
ones). atomic is enough for one variable updated in one step; several variables that must change
together still need a mutex. Run `python3 video11.3.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 128
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-03"
FINAL = (CODE / "atomic.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CC = "g++ -std=c++20 -O2 -Wall -Wextra atomic.cpp -o at"

(c1, r1, cch, rch) = cpp.session({"atomic.cpp": FINAL}, [
    CC, "./at", Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
fa = int(re.search(r"atomic 2000000 (\d+)ms", r1.output).group(1))
mu = int(re.search(r"mutex  2000000 (\d+)ms", r1.output).group(1))
assert mu > 2 * fa and c1.code == cch.code == 0 and rch.output == "500\n", r1.output
D = "零一二三四五六七八九"


def zh(n):
    """Cantonese reading of 0 <= n < 10000, e.g. 205 -> 二百零五, 15 -> 十五."""
    if n == 0:
        return "零"
    out, gap = "", False
    for unit, name in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        d = n // unit % 10
        if d:
            if gap and out:
                out += "零"
            out += ("" if (unit == 10 and d == 1 and not out) else D[d]) + name
            gap = False
        elif out:
            gap = True
    return out


SAY = {"std::atomic": "S T D atomic", "std::atomic<int>": "atomic int", "atomic": "atomic", "fast++": "fast 加加", "mutex": "mutex",
       "scoped_lock": "scoped lock", "fetch_add": "fetch add", "load": "load", "store": "store", "-O2": "O 二", "ms": "毫秒"}

s = Stage({"atomic.cpp": FINAL}, title="atomic", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集用 mutex 修好咗計數器，但係只係加一，每次都鎖一鎖，有啲大材小用。今集學 std::atomic：一個本身就唔會 data race 嘅變數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::atomic · 幾時夠用")),
    Scene("goal",
          "今集會講：[[b1]]atomic 變數；[[b2]]同 mutex 比較快慢；[[b3]]atomic 幾時夠用；[[b4]]幾時唔夠。",
          BulletCard("今集學識", [("std::atomic<int>", "b1"), ("atomic vs mutex：速度", "b2"), ("一個變數、一步：夠", "b3"), ("幾個變數一齊：唔夠", "b4")])),
    Scene("code",
          "[[fast]]fast 係 atomic int，加加本身就係一個不可分割嘅動作，唔會俾人打斷。[[slow]]slow 係普通 int，用上一集嘅 mutex 保護。[[fa]]addFast 直接加；[[fs]]addSlow 每次都要鎖。"
          "[[main]]main 各用兩個 thread 加一百萬次，計時。",
          s.scene(Open("atomic.cpp", at="fast"), Mark(7, at="fast"), Mark((8, 9), at="slow"), Mark((11, 15), at="fa"), Mark((17, 22), at="fs"),
                  Mark((26, 35), at="main"))),
    Scene("run",
          f"[[cc]]用 O 二編譯運行：[[o]]兩個都係二百萬，全部啱。但係 atomic 只用 {zh(fa)} 毫秒，mutex 用咗 {zh(mu)} 毫秒。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("enough",
          "atomic 幾時夠用？[[one]]一個變數，用一步完成嘅操作：加減、讀、寫，就夠；[[many]]但係如果要「檢查庫存大過零，先減一，再加銷售數字」，幾個步驟同幾個變數要一齊改，"
          "中間可能俾人插隊，就要用 mutex 包住成段。",
          TableCard("atomic 定 mutex？", ["情況", "用"], [
              (["一個計數器 ++、--", "std::atomic"], "one", GREEN),
              (["一個 flag：完成未", "std::atomic<bool>"], "one", GREEN),
              (["檢查再改、幾個變數一齊改", "std::mutex"], "many", AMBER),
          ], widths=[1.8, 1.2], code_cols=(1,), size=38)),
    Scene("recap",
          "總結：[[r1]]std::atomic 嘅操作唔會被打斷，唔會 data race；[[r2]]簡單嘅計數，atomic 比 mutex 快好多；[[r3]]一個變數一步完成，用 atomic；[[r4]]幾步或者幾個變數，用 mutex。",
          BulletCard("今集重點", [("atomic：唔會被打斷", "r1"), ("比 mutex 快", "r2"), ("一個變數一步：atomic", "r3"), ("幾步幾個：mutex", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]開四個 thread，每個負責二百五十個數，用一個 atomic 數零到九百九十九入面有幾多個雙數。[[next]]下一集：deadlock。多謝收睇，下次見！",
          EndCard("4 個 jthread 各數 250 個數，用 std::atomic<int> 數 0 到 999 嘅雙數：答案 500。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

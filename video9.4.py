#!/usr/bin/env python3
"""Video 112 (syllabus 9.4): assert 同 static_assert

average() asserts its vector is not empty: average({72, 64}) prints 68, average({}) really stops
with "Assertion `!v.empty() && "need at least one mark"' failed." and Aborted. Built with
-DNDEBUG the assert is gone and the same call really prints nan. static_assert(sizeof(int) == 8)
is a real compile error ("the comparison reduces to '(4 == 8)'"); with 4 it builds and prints 68.
Run `python3 video112.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 112
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-04"
FINAL = (CODE / "check.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SA = '    static_assert(sizeof(int) == 4, "needs 4-byte int");\n'
CALL1 = "    std::cout << average({72, 64}) << '\\n';\n"
CALL2 = "    std::cout << average({}) << '\\n';\n"
V1 = FINAL.replace(SA, "").replace(CALL1, CALL1 + CALL2)
BAD = FINAL.replace("== 4,", "== 8,")
CC = "g++ -std=c++20 -Wall -Wextra check.cpp -o chk"
ND = "g++ -std=c++20 -DNDEBUG check.cpp -o chk"

(c1, r1, c2, r2, clr, c3, clr2, c4, r4, cch, rch) = cpp.session({"check.cpp": V1}, [
    CC, "./chk", ND, "./chk", "clear", Write("check.cpp", BAD), CC, "clear", Write("check.cpp", FINAL), CC, "./chk",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.startswith("68\n") and "Assertion `!v.empty() && \"need at least one mark\"' failed." in r1.output and r1.code != 0, r1.output
assert r2.output in ("68\nnan\n", "68\n-nan\n") and r2.code == 0, r2.output
nan = r2.output.split("\n")[1]
assert "static assertion failed: needs 4-byte int" in cpp.visible(c3.output) and "(4 == 8)" in cpp.visible(c3.output)
assert r4.output == "68\n" and c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "75\n"

SAY = {"assert": "assert", "static_assert": "static assert", "<cassert>": "c assert", "NDEBUG": "N DEBUG", "-DNDEBUG": "D N DEBUG",
       "nan": "nan", "-nan": "負 nan", "sizeof(int)": "size of int", "average": "average", "Aborted": "Aborted", "percent": "percent"}

s = Stage({"check.cpp": V1}, title="assert 同 static_assert", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！寫 code 嘅時候，我哋成日有啲假設：呢個 vector 唔會係空，int 係四個 byte。今集學 assert 同 static_assert：將假設寫落 code，錯咗即刻知。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "運行時檢查 · 編譯時檢查 · NDEBUG")),
    Scene("goal",
          "今集會講：[[b1]]assert 喺運行時檢查；[[b2]]NDEBUG 會令 assert 消失；[[b3]]static_assert 喺編譯時檢查；[[b4]]assert 同 exception 點分。",
          BulletCard("今集學識", [("assert(條件)", "b1"), ("-DNDEBUG", "b2"), ("static_assert", "b3"), ("assert vs exception", "b4")])),
    Scene("assert",
          "[[fn]]average 假設 vector 唔係空，用 assert 寫低；後面加一句字串，出事時會一齊印出嚟。[[calls]]main 先計兩個分數，再傳一個空 vector。[[cc]]編譯運行：[[o]]六十八；"
          "跟住 assertion failed，連檔名、行數、條件都講埋，程式即刻停。",
          s.scene(Open("check.cpp", at="fn"), Mark(6, at="fn"), Mark((15, 16), at="calls"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("ndebug",
          "[[cc]]如果編譯時加 D N DEBUG，即係正式版本，assert 會全部消失。[[o]]運行：今次冇停，印咗 " + nan + "：零除零，錯誤靜靜雞溜咗過去。",
          s.scene(Run(c2, at="cc"), Run(r2, at="o"), Note("-DNDEBUG：assert 全部消失", at="o", where="editor"))),
    Scene("rules",
          "所以：[[bug]]assert 係用嚟捉自己嘅 bug；[[input]]用家輸入錯、檔案開唔到呢啲預期會發生嘅錯，要用 exception；[[side]]仲有，assert 入面唔好做有用嘅嘢，因為正式版本會被刪走。",
          TableCard("用 assert 定 exception？", ["情況", "用"], [
              (["自己嘅假設（bug）", "assert"], "bug"),
              (["用家輸入、檔案、網絡", "exception"], "input"),
              (["assert(x++ > 0)", "錯！NDEBUG 會刪走"], "side", RED),
          ], widths=[1.6, 1.4], code_cols=(), size=40)),
    Scene("static",
          "[[type]]有啲假設喺編譯時已經知：static_assert。例如假設 int 係八個 byte，再刪走空 vector 嗰句。[[cc]]編譯：[[err]]編譯失敗：static assertion failed，"
          "仲話埋你四唔等於八。",
          s.scene(Note(None), Run(clr, at="type"), Type("check.cpp", SA.replace("== 4,", "== 8,"), after="int main() {\n", at="type", rate=60),
                  Replace("check.cpp", CALL2, ""), Expect("check.cpp", BAD), Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("fix",
          "[[type]]改返四。[[cc]]編譯運行，[[o]]六十八。static_assert 唔使運行就檢查完，正式版本一樣會檢查，亦唔會令程式慢。",
          s.scene(Run(clr2, at="type"), Replace("check.cpp", "== 8,", "== 4,", at="type", rate=20), Expect("check.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("recap",
          "總結：[[r1]]assert 喺運行時檢查假設，錯咗即刻停；[[r2]]D N DEBUG 會刪走 assert，入面唔好有副作用；[[r3]]static_assert 喺編譯時檢查；[[r4]]bug 用 assert，預期嘅錯用 exception。",
          BulletCard("今集重點", [("assert：運行時", "r1"), ("NDEBUG：刪走 assert", "r2"), ("static_assert：編譯時", "r3"), ("bug → assert；預期錯 → exception", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 percent，用 assert 檢查分母大過零、分子喺範圍入面；再用 static_assert 檢查 long long 係八個 byte。[[next]]下一集：C++23 嘅 std::expected。多謝收睇，下次見！",
          EndCard("寫 int percent(int part, int whole)：assert(whole > 0)、assert(0 <= part <= whole)；static_assert(sizeof(long long) == 8)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

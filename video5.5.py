#!/usr/bin/env python3
"""Video 56 (syllabus 5.5): 指標同陣列

int* p = marks (the array decays to &marks[0]); *(p + 2) and p[3]; the real addresses of p and
p + 1 are 4 bytes apart; walking the array with a pointer up to marks + 5; with <= the walk really
reads one past the end, and AddressSanitizer reports a stack-buffer-overflow at that line.
Run `python3 video5.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 56
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-05"
FINAL = (CODE / "walk.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
L = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
SKEL = "#include <iostream>\n\nint main() {\n}\n"
V1 = SKEL.replace("}\n", "".join(L[:4]) + "}\n")
V2 = SKEL.replace("}\n", "".join(L[:5]) + "}\n")
BAD = FINAL.replace("q != marks + 5", "q <= marks + 5")
CC = "g++ -std=c++20 -Wall -Wextra walk.cpp -o walk"
CA = "g++ -std=c++20 -g -fsanitize=address walk.cpp -o walk"

(c1, r1, c2, r2, c3, r3, clr, c4, r4, c5, r5, cch, rch) = cpp.session({"walk.cpp": V1}, [
    CC, "./walk", Write("walk.cpp", V2), CC, "./walk", Write("walk.cpp", FINAL), CC, "./walk",
    Write("walk.cpp", BAD), "clear", CA, "./walk", Write("walk.cpp", FINAL), CA, "./walk",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "72 64\n91\n"
a0, a1 = (int(x, 16) for x in r2.output.split("\n")[2].split())
assert a1 - a0 == 4, (a0, a1)
assert r3.output.split("\n")[3] == "72 85 64 91 58 "
asan = cpp.visible(r4.output)
assert "stack-buffer-overflow" in asan and "walk.cpp:10" in asan and r4.code != 0, asan[:500]
assert r5.code == 0 and rch.output.strip() == "58 91 64 85 72"
P0, P1 = r2.output.split("\n")[2].split()

SAY = {"int* p = marks": "int pointer p 等如 marks", "*(p + 2)": "星 p 加二", "p[3]": "p 三", "p + 1": "p 加一",
       "marks + 5": "marks 加五", "q++": "q plus plus", "<=": "細過或等於", "AddressSanitizer": "Address Sanitizer",
       "stack-buffer-overflow": "stack buffer overflow", "decay": "decay"}

s = Stage({"walk.cpp": SKEL}, title="指標同陣列", split=0.45, code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！4.5 講過，陣列傳入函數會退化做指標。今集睇真啲：指標同陣列，究竟有乜關係。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "decay · p + 1 · p[i]")),
    Scene("goal",
          "今集會講：[[b1]]陣列名會變成第一格嘅地址；[[b2]]指標可以加減；[[b3]]中括號其實就係指標加法；[[b4]]用指標行一次陣列。",
          BulletCard("今集學識", [("陣列名 → &marks[0]", "b1"), ("指標加減", "b2"), ("p[i] 就係 *(p + i)", "b3"), ("用指標行陣列", "b4")])),
    Scene("decay",
          "[[decl]]int 指標 p 等於 marks：唔使 and 號，陣列名自己就會變成第一格嘅地址。[[plus]]星號 p 係第一格；p 加二，就係第三格。"
          "[[idx]]p 中括號三，就係第四格。[[cc]]編譯運行，[[o]]七十二、六十四，同埋九十一。中括號同指標加減，其實係同一回事。",
          s.scene(Open("walk.cpp", mode="instant"), Type("walk.cpp", "".join(L[:2]), before="}", last=True, at="decl", rate=26),
                  Type("walk.cpp", L[2], before="}", last=True, at="plus", rate=26), Type("walk.cpp", L[3], before="}", last=True, at="idx"),
                  Expect("walk.cpp", V1), Run(c1, at="cc"), Run(r1))),
    Scene("arith",
          "[[type]]印出 p 同 p 加一嘅地址。[[cc]]運行：[[o]]兩個地址相差四，唔係一！[[why]]因為 p 係 int 指標，加一就係跳去下一個 int，"
          "一個 int 有四個 byte。",
          s.scene(Type("walk.cpp", L[4], before="}", last=True, at="type"), Expect("walk.cpp", V2), Run(c2, at="cc", recall=True), Run(r2),
                  Note(f"…{P0[-2:]} 同 …{P1[-2:]}：相差 4\n＝ 一個 int", at="why", where="editor"))),
    Scene("boxes",
          "[[cells]]所以 p 加 i，就係由第一格行 i 格；[[same]]p 中括號 i，同星號 p 加 i 完全一樣。[[end]]marks 加五，就係最後一格之後嘅位置："
          "可以用嚟做終點，但係唔可以讀。",
          BoxesCard("int marks[5]", [BoxRow(
              [Box(f"p + {i}" if i else "p", str(v), f"marks[{i}]", at=("cells", 0.3 * i), color=AMBER if i == 2 else BLUE, w=170)
               for i, v in enumerate([72, 85, 64, 91, 58])]
              + [Box("p + 5", "✕", "終點，唔准讀", at="end", color=RED, w=170)], gap=0)],
              top=CONTENT_TOP + 60, box_h=110, size=46, notes=[("p[i] ＝ *(p + i)", "same")])),
    Scene("walk",
          "[[loop]]用指標行一次陣列：q 由 marks 開始，未到 marks 加五，就印星號 q，再 q 加加。[[cc]]運行，[[o]]五個分數全部印出嚟。",
          s.scene(Note(None), Type("walk.cpp", "".join(L[5:]), before="}", last=True, at="loop", rate=26), Expect("walk.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("bug",
          "如果條件寫錯咗做細過或等於呢？[[edit]]就會多行一次，讀埋最後一格之後嘅位置。[[cc]]用 AddressSanitizer 編譯運行：[[o]]即刻捉到，"
          "[[top]]睇返最頂：stack buffer overflow，喺第十行。",
          s.scene(Run(clr, at="edit"), Replace("walk.cpp", "q != marks + 5", "q <= marks + 5", at="edit"), Expect("walk.cpp", BAD),
                  Run(c4, at="cc"), Run(r4), Scroll(at="top"), Note("讀咗 marks[5]\n＝ stack-buffer-overflow", at="top", where="editor"))),
    Scene("fix",
          "[[fix]]改返做唔等於。[[cc]]再運行，[[o]]冇報告，五個數啱晒。[[rule]]所以 C++ 習慣用唔等於終點做條件，終點就係最後一格之後。",
          s.scene(Note(None), Scroll(top=False, at="fix"), Replace("walk.cpp", "q <= marks + 5", "q != marks + 5", at="fix"),
                  Expect("walk.cpp", FINAL), Run(c5, at="cc", recall=True), Run(r5))),
    Scene("recap",
          "總結：[[r1]]陣列名會退化做第一格嘅地址；[[r2]]指標加一，係跳一個元素，唔係一個 byte；[[r3]]p 中括號 i，就係星號 p 加 i；"
          "[[r4]]終點係最後一格之後，用嚟比較，唔可以讀。",
          BulletCard("今集重點", [("marks → &marks[0]", "r1"), ("p + 1：跳一個元素", "r2"), ("p[i] ＝ *(p + i)", "r3"),
                                ("終點 marks + 5：只比較，唔讀", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用指標由最後一格行返去第一格，倒轉印出成個陣列。小心唔好行過頭。"
          "[[next]]下一集，我哋講 const 同指標。多謝收睇，下次見！",
          EndCard("用指標由最後一格行返去第一格，倒轉印出陣列。小心唔好指去第一格之前。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

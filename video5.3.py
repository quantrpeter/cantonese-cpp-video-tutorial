#!/usr/bin/env python3
"""Video 54 (syllabus 5.3): 指標 vs reference

A reference r and a pointer p to the same int; `r = b` does not re-bind r, it really copies b
into a (a becomes 2); `p = &b` re-points p and *p = 20 changes b; p = nullptr; the differences
side by side. Run `python3 video5.3.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 54
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-03"
FINAL = (CODE / "cmp.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
L = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
SKEL = "#include <iostream>\n\nint main() {\n}\n"
V1 = SKEL.replace("}\n", "".join(L[:5]) + "}\n")
V2 = SKEL.replace("}\n", "".join(L[:7]) + "}\n")
V3 = SKEL.replace("}\n", "".join(L[:10]) + "}\n")
CC = "g++ -std=c++20 -Wall -Wextra cmp.cpp -o cmp"

(c1, r1, c2, r2, c3, r3, clr, c4, r4, cch, rch) = cpp.session({"cmp.cpp": V1}, [
    CC, "./cmp", Write("cmp.cpp", V2), CC, "./cmp", Write("cmp.cpp", V3), CC, "./cmp",
    Write("cmp.cpp", FINAL), "clear", CC, "./cmp",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "1 1\n" and r2.output == "1 1\na: 2\n" and r3.output == "1 1\na: 2\nb: 20\n"
assert r4.output == "1 1\na: 2\nb: 20\n1\n" and all(r.code == 0 for r in (c1, c2, c3, c4, cch))
assert rch.output.strip() == "Found -4"

SAY = {"int&": "int and", "int*": "int pointer", "r = b": "r 等如 b", "p = &b": "p 等如 and b", "*p": "星 p",
       "nullptr": "null pointer", "reference": "reference"}

s = Stage({"cmp.cpp": SKEL}, title="指標 vs reference", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！reference 同指標，都可以間接用到另一個變數。佢哋有乜分別？今集將兩樣並排比較。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int& vs int*")),
    Scene("goal",
          "今集會講：[[b1]]兩者嘅寫法；[[b2]]可唔可以轉對象；[[b3]]可唔可以係空嘅；[[b4]]幾時用邊個。",
          BulletCard("今集學識", [("寫法比較", "b1"), ("轉對象", "b2"), ("空：nullptr", "b3"), ("幾時用邊個", "b4")])),
    Scene("v1",
          "[[r]]r 係 a 嘅 reference，[[p]]p 係指住 a 嘅指標。[[use]]用 reference 直接寫 r；用指標，就要加星號。[[cc]]編譯運行：g++ 提我哋 b 未用到，等陣就會用；[[o]]兩個都係一。",
          s.scene(Open("cmp.cpp", mode="instant"), Type("cmp.cpp", "".join(L[:2]), before="}", last=True, rate=30),
                  Type("cmp.cpp", L[2], before="}", last=True, at="r"), Type("cmp.cpp", L[3], before="}", last=True, at="p"),
                  Type("cmp.cpp", L[4], before="}", last=True, at="use", rate=24), Expect("cmp.cpp", V1),
                  Run(c1, at="cc"), Run(r1))),
    Scene("rebind",
          "而家想 r 改去代表 b：[[type]]r 等於 b，得唔得？[[cc]]運行，[[o]]a 竟然變咗二！[[why]]reference 一世只代表 a，"
          "r 等於 b，其實係將 b 嘅值，複製入 a 度。",
          s.scene(Type("cmp.cpp", "".join(L[5:7]), before="}", last=True, at="type", rate=24), Expect("cmp.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2), Note("r = b：唔係轉對象\n係將 b 複製入 a", at="why", where="editor"))),
    Scene("repoint",
          "指標就可以轉對象：[[type]]p 等於 and 號 b，p 而家指住 b；[[set]]星號 p 等於二十，改嘅係 b。[[cc]]運行，[[o]]b 變咗二十。reference 就做唔到咁。",
          s.scene(Note(None), Type("cmp.cpp", L[7], before="}", last=True, at="type"), Type("cmp.cpp", "".join(L[8:10]), before="}", last=True, at="set", rate=24),
                  Expect("cmp.cpp", V3), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("boxes",
          "用盒嚟睇：[[ref]]r 冇自己嘅盒，佢只係 a 嘅另一個名；[[ptr]]p 有自己嘅盒，入面裝住地址，[[move]]可以改裝第二個地址，指去 b。",
          BoxesCard("reference：一個名；指標：一張紙條", [
              BoxRow([Box("a / r", "2", "int", at="ref", color=AMBER, w=260, key="a"),
                      Box("b", "20", "int", at="ref", w=260, key="b")], gap=200),
              BoxRow([Box("p", "&b", "int*", at="ptr", color=PURPLE, w=260, key="p")]),
          ], arrows=[("p", "b", "move", PURPLE)], top=CONTENT_TOP + 20, row_h=250, box_h=120, size=56)),
    Scene("null",
          "仲有：[[null]]指標可以乜都唔指，設做 nullptr；[[ref]]reference 就一定要代表一個變數，冇空嘅 reference。"
          "[[cc]]運行，[[o]]p 等於 nullptr，所以印出一，即係 true。",
          s.scene(Run(clr, at="null"), Type("cmp.cpp", "".join(L[10:]), before="}", last=True, at="null", rate=24), Expect("cmp.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("table",
          "並排比較：[[w]]寫法唔同；[[u]]用 reference 唔使星號；[[m]]reference 一世代表同一個，指標可以轉；[[n]]指標可以係 nullptr；"
          "[[i]]reference 一定要初始化。",
          TableCard("reference vs 指標", ["", "reference", "指標"], [
              (["宣告", "int& r = a;", "int* p = &a;"], "w"),
              (["用", "r", "*p"], "u"),
              (["轉對象", "唔得（r = b 係複製值）", "得：p = &b;"], "m"),
              (["可以係空", "唔得", "得：nullptr"], "n"),
              (["一定要初始化", "要", "唔使（但最好）"], "i"),
          ], widths=[1, 1.4, 1.4], code_cols=(1, 2), size=38)),
    Scene("rule",
          "所以：[[a]]能用 reference，就用 reference，簡單又安全；[[b]]需要轉對象，或者需要表示乜都冇嘅時候，先用指標。",
          TileCard("幾時用邊個？", [
              Tile("🔗", "reference", "預設首選\n函數參數、for 迴圈", "a", GREEN),
              Tile("👉", "指標", "要轉對象\n要表示「冇」：nullptr", "b", PURPLE),
          ], cols=2, height=360)),
    Scene("recap",
          "總結：[[r1]]reference 係第二個名，一世代表同一個變數；[[r2]]指標裝地址，可以轉對象；[[r3]]指標可以係 nullptr；"
          "[[r4]]能用 reference 就用 reference。",
          BulletCard("今集重點", [("reference：一世代表同一個", "r1"), ("指標：可以轉對象", "r2"), ("指標可以係 nullptr", "r3"),
                                ("首選 reference", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數，喺 vector 入面搵第一個負數，回傳指住佢嘅指標；搵唔到，就回傳 nullptr。"
          "[[next]]下一集，我哋睇吓指標用錯會點：nullptr 同懸空指標。多謝收睇，下次見！",
          EndCard("寫 int* findNegative(std::vector<int>& v)：回傳指住第一個負數嘅指標；搵唔到就回傳 nullptr。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

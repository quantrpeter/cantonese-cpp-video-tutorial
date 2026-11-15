#!/usr/bin/env python3
"""Video 98 (syllabus 8.11): Lambda

A lambda square(5) really prints 25. count_if with [pass] counts 3 marks of at least 50.
for_each with [total] is a real "assignment of read-only variable 'total'" error (a by-value
capture is a const copy); [&total] sums to 266. Captured at creation: with bonus changed to 100
afterwards, [bonus] really gives 75 and [&bonus] 170. Run `python3 video98.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 98
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-11"
FINAL = (CODE / "lambda.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()


def cut(a, b):
    return a + FINAL.split(a, 1)[1].split(b, 1)[0]


COUNT = cut("    std::vector<int> marks", "    int total = 0;")
SUM = cut("    int total = 0;", "    int bonus = 5;")
BONUS = "    int bonus = 5;" + FINAL.split("    int bonus = 5;", 1)[1].rsplit("}\n", 1)[0]
V3 = FINAL.replace(BONUS, "")
BAD = V3.replace("[&total](int m)", "[total](int m)")
V2 = V3.replace(SUM, "")
V1 = V2.replace(COUNT, "").replace("#include <algorithm>\n", "").replace("#include <vector>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra lambda.cpp -o lam"

(c1, r1, clr, c2, r2, clr2, c3, clr3, c4, r4, clr4, c5, r5, cch, rch) = cpp.session({"lambda.cpp": V1}, [
    CC, "./lam", "clear", Write("lambda.cpp", V2), CC, "./lam", "clear", Write("lambda.cpp", BAD), CC,
    "clear", Write("lambda.cpp", V3), CC, "./lam", "clear", Write("lambda.cpp", FINAL), CC, "./lam",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "25\n" and r2.output == "25\n3\n" and r4.output == "25\n3\n266\n" and r5.output == "25\n3\n266\n75 170\n", r5.output
assert "assignment of read-only variable 'total'" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == c5.code == cch.code == 0 and rch.output == "2\n"

SAY = {"lambda": "lambda", "[pass]": "中括號 pass", "[&total]": "中括號 and total", "[total]": "中括號 total", "[bonus]": "中括號 bonus",
       "[&bonus]": "中括號 and bonus", "[=]": "中括號等號", "[&]": "中括號 and 號", "[]": "空中括號", "std::count_if": "S T D count if",
       "count_if": "count if", "std::for_each": "S T D for each", "for_each": "for each", "byValue": "by value", "byRef": "by ref",
       "square": "square", "pass": "pass", "total": "total", "bonus": "bonus", "auto": "auto"}

s = Stage({"lambda.cpp": V1}, title="Lambda", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！好多演算法都要你畀一個「做乜」嘅小函數，例如點樣算合格。每次都另外寫一個函數好麻煩。今集學 lambda：喺用嘅地方，即場寫一個函數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "[capture](params) { body }")),
    Scene("goal",
          "今集會講：[[b1]]lambda 嘅寫法；[[b2]]傳俾演算法；[[b3]]capture by value 同 by reference；[[b4]]capture 嘅時間。",
          BulletCard("今集學識", [("[](int x) { return x * x; }", "b1"), ("count_if、for_each", "b2"), ("[x] vs [&x]", "b3"), ("幾時影低個值", "b4")])),
    Scene("first",
          "[[lam]]square 係一個 lambda：中括號、參數、大括號入面係內容，用 auto 接住。[[call]]用法同普通函數一樣。[[cc]]編譯運行，[[o]]二十五，五乘五。佢冇名，所以用一個變數接住，類型就交俾 auto。",
          s.scene(Open("lambda.cpp", at="lam"), Mark(4, at="lam"), Mark(5, at="call"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("parts",
          "[[cap]]中括號叫 capture，決定可以用外面邊啲變數；[[par]]小括號係參數；[[body]]大括號係內容，return 嘅類型編譯器會自己推斷。",
          AnatomyCard("lambda 嘅樣", [
              Part("[pass]", "capture：用外面嘅變數", AMBER, "cap"), Part("(int m)", "參數", BLUE, "par"),
              Part("{ return m >= pass; }", "內容", GREEN, "body"),
          ], size=64)),
    Scene("count",
          "[[type]]數有幾多個合格：count_if 收一段範圍，同埋一個 lambda。[[cap]]lambda 要用到外面嘅 pass，所以喺中括號寫 pass。[[cc]]運行，[[o]]三個合格：七十二、九十一同五十八。四十五唔合格。",
          s.scene(Run(clr, at="type"), Replace("lambda.cpp", "#include <iostream>\n", "#include <algorithm>\n#include <iostream>\n#include <vector>\n", at="type", rate=40),
                  Type("lambda.cpp", COUNT, before="}", last=True, rate=60), Expect("lambda.cpp", V2), Mark(11, at="cap"), Mark(None, at="cc"),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("readonly",
          "[[type]]再用 for_each 計總分：lambda 將每個分數加落 total。中括號寫 total。[[cc]]編譯：[[err]]錯誤！total 係唯讀。",
          s.scene(Run(clr2, at="type"), Type("lambda.cpp", SUM.replace("[&total]", "[total]"), before="}", last=True, at="type", rate=60),
                  Expect("lambda.cpp", BAD), Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("ref",
          "[[why]]因為中括號直接寫個名，係 capture by value：lambda 入面係一份唯讀嘅副本，改唔到外面。[[type]]要改外面，就要加 and 號：capture by reference。"
          "[[cc]]運行，[[o]]二百六十六，四個分數加埋。",
          s.scene(Note("[total]：唯讀副本\n[&total]：真正嘅 total", at="why", where="editor"), Run(clr3, at="type"), Note(None, at="type"),
                  Replace("lambda.cpp", "[total](int m)", "[&total](int m)", at="type", rate=20), Expect("lambda.cpp", V3),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("when",
          "[[type]]最後一個細節：bonus 係五，byValue 影低一份，byRef 用 reference；[[change]]然後先將 bonus 改做一百。[[cc]]運行：[[o]]七十五同一百七十！"
          "[[why]]by value 喺整 lambda 嗰一刻已經影低咗五；by reference 用嘅係而家嘅一百。",
          s.scene(Run(clr4, at="type"), Type("lambda.cpp", BONUS, before="}", last=True, at="type", rate=70), Expect("lambda.cpp", FINAL),
                  Mark((18, 19), at="type"), Mark(20, at="change"), Mark(None, at="cc"), Run(c5, at="cc", recall=True), Run(r5))),
    Scene("caps",
          "capture 嘅寫法：[[none]]空中括號，乜都唔用；[[v]]寫名，影低一份；[[r]]and 加名，用 reference；[[all]]等號同 and 號，就係全部 by value 或者全部 by reference。"
          "最好寫清楚要邊啲。",
          TableCard("capture 寫法", ["寫法", "意思"], [
              (["[]", "乜都唔 capture"], "none"),
              (["[x]", "x 嘅副本（唯讀）"], "v"),
              (["[&x]", "x 嘅 reference（改得）"], "r"),
              (["[=] / [&]", "全部副本 / 全部 reference"], "all"),
          ], widths=[1, 2], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]lambda 就係即場寫嘅函數；[[r2]]最常傳俾演算法；[[r3]]寫名係副本，唯讀，加 and 號先改到外面；[[r4]]副本喺整 lambda 嗰陣已經影低。",
          BulletCard("今集重點", [("[capture](params) { body }", "r1"), ("傳俾 count_if、for_each…", "r2"), ("[x] 唯讀副本；[&x] 改得", "r3"),
                                ("副本：整嘅時候影低", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 count_if 同一個 capture 咗 k 嘅 lambda，數一個字串 vector 入面有幾多個字長過三個字母。[[next]]下一集：sort 同自訂比較。多謝收睇，下次見！",
          EndCard("words {\"hi\", \"hello\", \"cpp\", \"lambda\"}，k = 3：用 count_if 加 [k] lambda 數長過 k 嘅字，答案係 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 115 (syllabus 9.7): stringstream 同解析文字

std::istringstream reads "72 64 abc 91" like cin: >> stops at "abc", so the real sum is 136 (91
is never reached). std::getline(csv, field, ',') splits "Amy,72,A" into [Amy][72][A]; std::stoi
and std::ostringstream build "Amy got 77". Run `python3 video115.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 115
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-07"
FINAL = (CODE / "parse.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
OUT = "    std::ostringstream out;" + FINAL.split("    std::ostringstream out;")[1].rsplit("}\n", 1)[0]
CSV = "    std::istringstream csv" + FINAL.split("    std::istringstream csv")[1].split("    std::ostringstream out;")[0]
V2 = FINAL.replace(OUT, "")
V1 = V2.replace(CSV, "").replace("#include <vector>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra parse.cpp -o parse"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"parse.cpp": V1}, [
    CC, "./parse", "clear", Write("parse.cpp", V2), CC, "./parse", "clear", Write("parse.cpp", FINAL), CC, "./parse",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "136\n" and r2.output == "136\n[Amy][72][A]\n" and r3.output == "136\n[Amy][72][A]\nAmy got 77\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "12\n"

SAY = {"std::istringstream": "S T D i string stream", "istringstream": "i string stream", "std::ostringstream": "S T D o string stream",
       "ostringstream": "o string stream", "<sstream>": "s stream", "std::getline": "S T D get line", "getline": "get line",
       "std::stoi": "S T D s to i", "stoi": "s to i", "out.str()": "out 點 str", "CSV": "C S V", "abc": "a b c", "Amy": "Amy",
       "words >> x": "words 兩個大過號 x", ">>": "兩個大過號"}

s = Stage({"parse.cpp": V1}, title="stringstream 同解析文字", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！cin 可以由鍵盤讀數字，如果啲文字已經喺一個 string 入面呢？例如由檔案讀入嘅一行 CSV。今集學 stringstream：將字串當做輸入輸出嚟用。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "istringstream · getline · CSV")),
    Scene("goal",
          "今集會講：[[b1]]istringstream 好似 cin；[[b2]]讀到唔啱嘅嘢會點；[[b3]]用 getline 按逗號拆；[[b4]]ostringstream 砌字串。",
          BulletCard("今集學識", [("istringstream：字串版 cin", "b1"), (">> 讀錯：停", "b2"), ("getline(…, ',')", "b3"), ("ostringstream", "b4")])),
    Scene("words",
          "[[open]]words 係一個 istringstream，入面係四樣嘢：七十二、六十四、abc、九十一。[[loop]]用兩個大過號，好似 cin 咁逐個讀數加起嚟。[[cc]]編譯運行：[[o]]一百三十六？"
          "九十一冇加到！七十二加六十四，就停咗。",
          s.scene(Open("parse.cpp", at="open"), Mark(6, at="open"), Mark((9, 11), at="loop"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("fail",
          "[[a]]讀到 abc，唔係數字，讀取失敗；[[stop]]stream 一失敗就停低，while 條件變 false，後面嘅九十一都唔會再讀。[[same]]cin 都係一樣，所以讀完要檢查。",
          BoxesCard("\"72 64 abc 91\"", [
              BoxRow([Box("", "72", "OK", at="a", color=GREEN, w=150), Box("", "64", "OK", at="a", color=GREEN, w=150),
                      Box("", "abc", "失敗", at="a", color=RED, w=150), Box("", "91", "冇讀", at="stop", w=150)], gap=16),
          ], notes=[("一失敗：之後全部唔讀", "stop"), ("cin 都一樣", "same")], top=CONTENT_TOP + 40, row_h=250, box_h=110, size=44)),
    Scene("csv",
          "[[type]]CSV 一行用逗號分隔：Amy、七十二、A。[[split]]getline 加第三個參數逗號，就會讀到逗號為止；每讀一段，就放入 vector。[[cc]]運行：[[o]]三段：Amy、七十二、A，逗號冇咗。",
          s.scene(Run(clr, at="type"), Replace("parse.cpp", "#include <string>\n", "#include <string>\n#include <vector>\n", at="type", rate=40),
                  Type("parse.cpp", CSV, before="}", last=True, rate=60), Expect("parse.cpp", V2), Mark((17, 19), at="split"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("out",
          "[[type]]反方向：ostringstream 好似 cout，但係寫入一個 string。[[stoi]]七十二仲係字串，要用 stoi 變做 int 先加得五。[[str]]out 點 str 攞返成個字串。[[cc]]運行：[[o]]Amy got 七十七：七十二加五。",
          s.scene(Run(clr2, at="type"), Type("parse.cpp", OUT, before="}", last=True, at="type", rate=50), Expect("parse.cpp", FINAL),
                  Mark(25, at="stoi"), Mark(26, at="str"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("tools",
          "[[i]]istringstream 由字串讀；[[o]]ostringstream 寫入字串；[[g]]getline 加分隔符號就可以拆欄；[[s]]stoi、stod 將字串變數字，錯咗會 throw。",
          TableCard("解析文字工具", ["工具", "用途"], [
              (["std::istringstream", "由字串讀（好似 cin）"], "i"),
              (["std::ostringstream", "寫入字串（好似 cout）"], "o"),
              (["std::getline(s, f, ',')", "讀到逗號為止"], "g"),
              (["std::stoi / std::stod", "字串 → 數字（錯就 throw）"], "s"),
          ], widths=[1.6, 1.6], code_cols=(0,), size=36)),
    Scene("recap",
          "總結：[[r1]]stringstream 令字串可以好似 cin、cout 咁用；[[r2]]兩個大過號讀錯就停，記得檢查；[[r3]]getline 加逗號拆 CSV；[[r4]]stoi 變數字，ostringstream 砌字串。",
          BulletCard("今集重點", [("istringstream / ostringstream", "r1"), (">> 失敗就停", "r2"), ("getline(…, ',')", "r3"), ("stoi、out.str()", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將三逗號四逗號五拆開，每段 stoi 變數字，加埋。[[next]]下一集：std::filesystem。多謝收睇，下次見！",
          EndCard("拆 \"3,4,5\"：getline 加 ','，每段 std::stoi，加埋係 12。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

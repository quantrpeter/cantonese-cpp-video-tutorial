#!/usr/bin/env python3
"""Video 99 (syllabus 8.12): sort 同自訂比較

std::sort on a vector<Student> with no comparator is a real 131-line template error whose own
line says "required from here" at the sort call, followed by "no match for 'operator<'". A lambda
comparing marks (higher first) really prints Amy 91, Cat 72, Ben 72, Dan 58; adding a name
tie-break gives Amy, Ben, Cat, Dan. Run `python3 video8.12.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 99
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-12"
FINAL = (CODE / "sort.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD_SORT = "    std::sort(s.begin(), s.end(),\n"
CMP = FINAL.split(HEAD_SORT)[1].split("    for (")[0]
TIE = "                  if (a.mark != b.mark) {\n                      return a.mark > b.mark;\n                  }\n                  return a.name < b.name;\n"
ONE = "                  return a.mark > b.mark;\n"
V2 = FINAL.replace(TIE, ONE)
BAD = FINAL.replace(HEAD_SORT + CMP, "    std::sort(s.begin(), s.end());\n")
CC = "g++ -std=c++20 -Wall -Wextra sort.cpp -o sort"

(c1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"sort.cpp": BAD}, [
    CC, "clear", Write("sort.cpp", V2), CC, "./sort", "clear", Write("sort.cpp", FINAL), CC, "./sort",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
e1 = cpp.visible(c1.output)
assert "sort.cpp:14:14:   required from here" in e1 and "no match for 'operator<' (operand types are 'Student' and 'Student')" in e1, e1[:300]
assert r2.output == "Amy 91\nCat 72\nBen 72\nDan 58\n" and r3.output == "Amy 91\nBen 72\nCat 72\nDan 58\n", (r2.output, r3.output)
assert c2.code == c3.code == cch.code == 0 and rch.output == "fig kiwi pear apple \n"
nlines = len(e1.strip().splitlines())
say_n = {131: "一百三十一"}.get(nlines, str(nlines))

SAY = {"std::sort": "S T D sort", "std::stable_sort": "S T D stable sort", "stable_sort": "stable sort", "operator<": "operator 細過",
       "a.mark > b.mark": "a 嘅分數大過 b", "a.name < b.name": "a 嘅名細過 b", "Student": "Student", "required from here": "required from here",
       "Amy": "Amy", "Ben": "Ben", "Cat": "Cat", "Dan": "Dan", "<=": "細過或等於", "comparator": "comparator"}

s = Stage({"sort.cpp": BAD}, title="sort 同自訂比較", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！std::sort 一句就排好一堆數。但係排學生呢？按分數由高到低，同分就按名，排序嘅規則要由你話佢知。今集學自訂比較。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::sort · comparator · 同分點排")),
    Scene("goal",
          "今集會講：[[b1]]點解 sort 唔識排 Student；[[b2]]用 lambda 寫比較；[[b3]]同分嘅時候點算；[[b4]]比較函數嘅規矩。",
          BulletCard("今集學識", [("冇 operator<：排唔到", "b1"), ("lambda 比較", "b2"), ("同分：再比名", "b3"), ("規矩：用 <，唔用 <=", "b4")])),
    Scene("nocmp",
          "[[open]]四個學生，有名同分數。[[sort]]直接 std::sort。[[cc]]編譯：[[err]]一大堆錯誤，成" + say_n + "行！[[here]]搵自己個檔：第十四行，required from here；"
          "下面就講：Student 冇細過號，sort 唔知點比。",
          s.scene(Open("sort.cpp", at="open"), Mark((12, 13), at="open"), Mark(14, at="sort"), Mark(None, at="cc"), Run(c1, at="cc"),
                  Scroll(at="here", find="required from here"), Mark(14, at="here"))),
    Scene("lambda",
          "[[type]]俾 sort 第三個參數：一個 lambda，收兩個學生 a 同 b。[[rule]]意思係：如果 a 應該排喺 b 前面，就回傳 true。分數高嘅排前，所以係 a 嘅分數大過 b。"
          "[[cc]]運行：[[o]]Amy 第一，Dan 最尾。",
          s.scene(Mark(None), Run(clr, at="type"), Replace("sort.cpp", "    std::sort(s.begin(), s.end());\n", HEAD_SORT + CMP.replace(TIE, ONE), at="type", rate=60),
                  Expect("sort.cpp", V2), Mark(16, at="rule"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("tie",
          "[[same]]但係 Cat 同 Ben 都係七十二，邊個先？std::sort 唔保證打和嘅次序。[[type]]所以要寫埋：分數唔同就比分數；同分，就比名，名細嘅排前。"
          "[[cc]]運行：[[o]]Ben 排喺 Cat 前面，次序固定，每次運行都一樣。",
          s.scene(Note("Cat 72、Ben 72：邊個先？", at="same", where="editor"), Note(None, at="type"), Run(clr2, at="type"),
                  Replace("sort.cpp", ONE, TIE, at="type", rate=50), Expect("sort.cpp", FINAL), Mark((16, 19), at="type"), Mark(None, at="cc"),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("rules",
          "比較函數有規矩：[[t]]a 應該排前，先回傳 true；[[eq]]兩個一樣，一定要回傳 false，所以用細過、大過，唔好用細過或等於，否則 sort 可能出錯，甚至當機；"
          "[[stable]]想打和保持原本次序，就用 std::stable_sort。",
          TableCard("比較函數嘅規矩", ["規矩", "例子"], [
              (["a 排前 → true", "return a.mark > b.mark;"], "t"),
              (["一樣 → 一定 false", "用 < >，唔好用 <= >="], "eq", RED),
              (["打和保持原次序", "std::stable_sort"], "stable"),
          ], widths=[1.1, 1.6], code_cols=(1,), size=38)),
    Scene("recap",
          "總結：[[r1]]sort 唔識比較你嘅類型，就要俾一個比較函數；[[r2]]lambda 回傳 a 係咪應該排喺 b 前面；[[r3]]打和要自己再比，或者用 stable_sort；[[r4]]用細過，唔好用細過或等於。",
          BulletCard("今集重點", [("sort(begin, end, 比較)", "r1"), ("a 排前 → true", "r2"), ("打和：再比 / stable_sort", "r3"), ("< 唔係 <=", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將幾個字按長度由短到長排，一樣長就按字母。[[next]]下一集：常用演算法。多謝收睇，下次見！",
          EndCard("{\"pear\", \"fig\", \"apple\", \"kiwi\"}：先按長度，同長再按字母，應該係 fig kiwi pear apple。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

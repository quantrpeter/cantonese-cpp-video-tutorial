#!/usr/bin/env python3
"""Video 43 (syllabus 4.2): Range-based for

for (int m : marks) prints every mark without an index; doubling with `int m` really changes
nothing (m is a copy); auto& changes the vector; const auto& reads without copying.
Run `python3 video4.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 43
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-02"
FINAL = (CODE / "mark.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
INIT = "    std::vector<int> marks{72, 85, 64};\n"
PRINT1 = "    for (int m : marks) {\n        std::cout << m << ' ';\n    }\n    std::cout << '\\n';\n"
DOUBLE = "    for (auto& m : marks) {\n        m = m * 2;\n    }\n"
PRINT2 = "    for (const auto& m : marks) {\n        std::cout << m << ' ';\n    }\n    std::cout << '\\n';\n"
SKEL = "#include <iostream>\n#include <vector>\n\nint main() {\n}\n"
assert SKEL.replace("}\n", INIT + PRINT1 + DOUBLE + PRINT2 + "}\n") == FINAL
V1 = SKEL.replace("}\n", INIT + PRINT1 + "}\n")
V2 = SKEL.replace("}\n", INIT + PRINT1 + DOUBLE.replace("auto& m", "int m") + PRINT2.replace("const auto& m", "int m") + "}\n")
V3 = V2.replace("for (int m : marks) {\n        m = m * 2;", "for (auto& m : marks) {\n        m = m * 2;")
CC = "g++ -std=c++20 -Wall -Wextra mark.cpp -o mark"

(c1, r1, c2, r2, c3, r3, c4, r4, cch, rch) = cpp.session({"mark.cpp": V1}, [
    CC, "./mark", Write("mark.cpp", V2), CC, "./mark", Write("mark.cpp", V3), CC, "./mark",
    Write("mark.cpp", FINAL), CC, "./mark",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["72", "85", "64"] and r2.output.split() == ["72", "85", "64"] * 2
assert r3.output.split() == r4.output.split() == ["72", "85", "64", "144", "170", "128"]
warn2 = "set but not used" in cpp.visible(c2.output)
assert c1.code == c2.code == c3.code == c4.code == cch.code == 0 and rch.output.split()[:1] == ["211"]

SAY = {"auto&": "auto and", "const auto&": "const auto and", "int m : marks": "int m 冒號 marks", "range-based for": "range based for"}

s = Stage({"mark.cpp": SKEL}, title="Range-based for", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集用 i 由零數到 size 減一，逐個攞出嚟，有啲煩。今集學 range-based for：直接逐個攞，唔使理位置。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "for (x : v) · auto& · const auto&")),
    Scene("goal",
          "今集會講：[[b1]]range-based for 點寫；[[b2]]想改 vector 入面嘅值，要用 auto&；[[b3]]淨係讀，就用 const auto&。",
          BulletCard("今集學識", [("for (int m : marks)", "b1"), ("改值：auto&", "b2"), ("淨係讀：const auto&", "b3")])),
    Scene("v1",
          "[[init]]vector 可以用大括號，一開始就放入三個分數。[[loop]]for 括號入面：int m，冒號，marks，"
          "讀做：marks 入面嘅每一個 m。[[cc]]編譯運行，[[o]]七十二、八十五、六十四，三個分數逐個印咗出嚟。",
          s.scene(Open("mark.cpp", mode="instant"), Type("mark.cpp", INIT, before="}", last=True, at="init"),
                  Type("mark.cpp", PRINT1, before="}", last=True, at="loop", rate=24), Expect("mark.cpp", V1),
                  Run(c1, at="cc"), Run(r1))),
    Scene("compare",
          "[[old]]同上一集嘅寫法比較：唔使 i，唔使 size，亦唔使中括號，[[new]]短咗，亦都唔會數錯位置。",
          CodeCompareCard("兩種寫法", [
              Pane("用位置", "for (std::size_t i = 0;\n     i < marks.size(); i++) {\n    std::cout << marks[i];\n}", True, "old"),
              Pane("range-based for", "for (int m : marks) {\n    std::cout << m;\n}", True, "new"),
          ], size=32)),
    Scene("copy",
          "而家想將每個分數乘二。[[type]]寫多個迴圈：for int m，m 等於 m 乘二；[[print]]之後再印一次所有分數。"
          "[[cc]]編譯運行，[[o]]第二行，竟然冇變！乘咗二嘅分數去咗邊？",
          s.scene(Type("mark.cpp", DOUBLE.replace("auto& m", "int m"), before="}", last=True, at="type", rate=24),
                  Type("mark.cpp", PRINT2.replace("const auto& m", "int m"), before="}", last=True, at="print", rate=30),
                  Expect("mark.cpp", V2), Run(c2, at="cc", recall=True), Run(r2),
                  Note("乘二之後，冇變？", at="o", where="editor"))),
    Scene("ref",
          "因為 int m 只係一個副本，記得 3.4？每次攞出嚟嘅，只係影印本，改咗都冇用。[[fix]]要改原本嘅值，就用 reference：auto&。"
          "[[cc]]再運行，[[o]]今次係一百四十四、一百七十、一百二十八。",
          s.scene(Note(None), Replace("mark.cpp", "for (int m : marks) {\n        m = m * 2;",
                                      "for (auto& m : marks) {\n        m = m * 2;", at="fix"), Expect("mark.cpp", V3),
                  Mark(10, at="fix"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("const",
          "淨係讀嘅時候，[[c]]就用 const auto&：唔使複製，對於字串呢啲大嘅嘢特別有用；[[safe]]const 仲保證唔會唔小心改咗佢。"
          "[[cc]]運行，[[o]]結果一樣。以後淨係讀，就用 const auto&。",
          s.scene(Mark(None), Replace("mark.cpp", "for (int m : marks) {\n        std::cout << m << ' ';\n    }\n    std::cout << '\\n';\n}",
                                      "for (const auto& m : marks) {\n        std::cout << m << ' ';\n    }\n    std::cout << '\\n';\n}", at="c"),
                  Expect("mark.cpp", FINAL), Mark(13, at="c"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("table",
          "三種寫法：[[a]]int m 係副本，改唔到 vector；[[b]]auto& 係第二個名，改得到；[[c]]const auto& 都係第二個名，但係唔准改，"
          "最啱淨係讀。[[auto]]auto 會自動用 vector 入面嘅型別。",
          TableCard("for 入面嘅 m 係乜？", ["寫法", "m 係", "用途"], [
              (["for (int m : marks)", "副本", "改咗冇用"], "a", RED),
              (["for (auto& m : marks)", "第二個名", "改 vector 入面嘅值"], "b", GREEN),
              (["for (const auto& m : marks)", "第二個名，唔准改", "淨係讀，唔使複製"], "c", BLUE),
          ], widths=[1.7, 1.1, 1.3], code_cols=(0,), size=38, note=("auto：自動用 vector 入面嘅型別", "auto"))),
    Scene("recap",
          "總結：[[r1]]range-based for 逐個攞出 vector 入面嘅值；[[r2]]要改值，用 auto&；[[r3]]淨係讀，用 const auto&；"
          "[[r4]]需要知道位置嘅時候，先至用返 i。",
          BulletCard("今集重點", [("for (x : v)：逐個攞出嚟", "r1"), ("改值：auto&", "r2"), ("淨係讀：const auto&", "r3"),
                                ("要位置：用返 i", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 range-based for 計所有分數嘅總和，再將所有細過五十嘅分數改做五十。"
          "[[next]]下一集，我哋學 vector 嘅常用操作。多謝收睇，下次見！",
          EndCard("用 range-based for 計所有分數嘅總和；再將所有細過 50 嘅分數改做 50。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

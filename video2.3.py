#!/usr/bin/env python3
"""Video 21 (syllabus 2.3): else if 同巢狀 if

Grades A to F with an else-if chain; with the A and B branches swapped, 90 really prints B
(the first true condition wins); an if without braces where "Well done!" prints for 30 marks,
with g++'s -Wmisleading-indentation warning; a nested if. Run `python3 video2.3.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 21
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-03"
GRADE = (CODE / "grade.cpp").read_text()
NEST = (CODE / "nest.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
A_ = '    if (mark >= 85) {\n        std::cout << "A'
B_ = '} else if (mark >= 70) {\n        std::cout << "B'
SWAP = GRADE.replace(A_, "@1").replace(B_, "@2").replace("@1", '    if (mark >= 70) {\n        std::cout << "B') \
            .replace("@2", '} else if (mark >= 85) {\n        std::cout << "A')
INNER = "        if (mark >= 85) {\n            std::cout << \"Excellent!\\n\";\n        }\n"
N2 = NEST.replace(INNER, "")
N1 = N2.replace("if (mark >= 50) {", "if (mark >= 50)").replace("    }\n}", "}")
CG = "g++ -std=c++20 -Wall -Wextra grade.cpp -o grade"
CN = "g++ -std=c++20 -Wall -Wextra nest.cpp -o nest"

(g1, rg1, g2, rg2, rg3, rg4, clr, n1, rn1, n2, rn2, n3, rn3, rn4, cch, rch) = cpp.session(
    {"grade.cpp": SWAP, "nest.cpp": N1}, [
        CG, Input("./grade", ["90"]),
        Write("grade.cpp", GRADE), CG, Input("./grade", ["90"]), Input("./grade", ["72"]), Input("./grade", ["30"]),
        "clear", CN, Input("./nest", ["30"]),
        Write("nest.cpp", N2), CN, Input("./nest", ["30"]),
        Write("nest.cpp", NEST), CN, Input("./nest", ["90"]), Input("./nest", ["60"]),
        Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["25"]),
    ], refresh=opts.fresh_runs, cols=48)
assert rg1.output.endswith("B\n") and rg2.output.endswith("A\n") and rg3.output.endswith("B\n") and rg4.output.endswith("F\n")
assert "misleadingly indented" in cpp.visible(n1.output) or "does not guard" in cpp.visible(n1.output), n1.output
assert rn1.output.endswith("Well done!\n") and "Pass" not in rn1.output and rn2.output == "Mark: 30\n"
assert rn3.output.endswith("Pass\nWell done!\nExcellent!\n") and rn4.output.endswith("Pass\nWell done!\n")
assert all(r.code == 0 for r in (g1, g2, n1, n2, n3, cch)) and rch.output.endswith("Warm\n")

SAY = {"else if": "else if", "if": "if", "else": "else", "Well done": "Well done", "Excellent": "Excellent"}

s = Stage({"grade.cpp": SWAP, "nest.cpp": N1}, title="else if 同巢狀 if", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集學咗 if 同 else，但係如果有多過兩個選擇呢？今集學 else if，同埋 if 入面再有 if。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "else if · 巢狀 if · 大括號")),
    Scene("goal",
          "今集會講：[[b1]]用 else if 處理多個選擇；[[b2]]點解條件嘅次序好重要；[[b3]]巢狀 if；[[b4]]點解一定要寫大括號。",
          BulletCard("今集學識", [("else if：多個選擇", "b1"), ("條件次序好重要", "b2"), ("巢狀 if", "b3"),
                                ("大括號一定要寫", "b4")])),
    Scene("table",
          "今次將分數轉做等級：[[a]]八十五分或以上係 A，[[b]]七十分或以上係 B，[[c]]五十五分 C，[[d]]四十分 D，[[f]]四十分以下就係 F。",
          TableCard("分數 → 等級", ["分數", "等級"], [
              (["85 或以上", "A"], "a"), (["70 – 84", "B"], "b"), (["55 – 69", "C"], "c"), (["40 – 54", "D"], "d"),
              (["40 以下", "F"], "f", RED),
          ], widths=[1, 1], code_cols=(1,), size=42)),
    Scene("chain",
          "[[open]]用 else if 就可以一路接落去：如果呢個條件唔成立，就試下一個；[[else]]全部都唔成立，就行最後嘅 else。",
          s.scene(Open("grade.cpp", at="open"), Mark((7, 10), at=("open", 1.5)), Mark((15, 17), at="else"))),
    Scene("run_chain",
          "[[cc]]編譯運行，[[t]]輸入九十分。[[o]]竟然係 B？九十分，應該係 A 先啱。",
          s.scene(Mark(None), Run(g1, at="cc"), Run(rg1, keys=("t",)), Note("90 分應該係 A！", at="o", where="editor"))),
    Scene("order",
          "原因係次序。[[first]]else if 由上至下逐個檢查，第一個成立嘅條件，就會行佢嗰段，後面嘅全部唔理。"
          "[[why]]九十大過七十，第一個條件已經成立，所以印咗 B，根本行唔到 A 嗰段。",
          s.scene(Note(None), Mark(7, at="first"), Note("90 >= 70 已經成立\n後面嘅唔會再檢查", at="why", where="editor"))),
    Scene("fix",
          "[[fix]]所以要由最高分寫起：先檢查八十五分，再檢查七十分。",
          s.scene(Note(None), Mark(None), Replace("grade.cpp", '    if (mark >= 70) {\n        std::cout << "B', A_, at="fix"),
                  Replace("grade.cpp", '} else if (mark >= 85) {\n        std::cout << "A', B_), Expect("grade.cpp", GRADE))),
    Scene("run_fix",
          "[[cc]]再編譯運行。[[t1]]九十分，[[o1]]係 A；[[t2]]七十二分，[[o2]]係 B；[[t3]]三十分，[[o3]]係 F。全部都啱晒：條件由高分排到低分，就唔會再出錯。",
          s.scene(Run(g2, at="cc", recall=True), Run(rg2, recall=True, keys=("t1",)),
                  Run(rg3, at="t2", recall=True, keys=(("t2", 0.9),)), Run(rg4, at="t3", recall=True, keys=(("t3", 0.9),)))),
    Scene("flow",
          "記住 else if 嘅規則：[[q1]]由上至下，逐個問；[[q2]]第一個答係嘅，就行嗰段，[[stop]]然後成條鏈就完咗。"
          "[[rule]]所以範圍要由窄到闊，或者由高到低咁排。",
          FlowCard("else if：第一個成立就停", [Row("90 分", "由上至下", BLUE, [
              Node(">= 85？", "是 → A", "q1"), Node(">= 70？", "唔會問", "q2"), Node(">= 55？", "唔會問", "q2"),
              Node("else", "唔會到", "stop"),
          ], note="由高到低排，第一個成立就停", note_at="rule")])),
    Scene("brace1",
          "跟住講大括號。[[open]]呢個程式嘅 if 冇寫大括號，下面兩句都縮咗排，睇落好似兩句都屬於 if。"
          "[[cc]]編譯，[[warn]]g++ 警告：呢個 if 其實冇包住第二句。[[t]]照運行，輸入三十分，[[o]]竟然印出 Well done！",
          s.scene(Run(clr), Open("nest.cpp", at="open"), Mark((7, 9), at=("open", 1.0)), Mark(None, at="cc"),
                  Run(n1, at="cc"), Run(rn1, keys=(("t", 0.8),)), Note("30 分都 Well done？", at="o", where="editor"))),
    Scene("brace2",
          "因為冇大括號嘅 if，只會管住下一句；縮排只係俾人睇，編譯器完全唔理。[[fix]]加返大括號，兩句先會一齊屬於 if。"
          "[[cc]]再運行，[[t]]三十分，[[o]]今次乜都冇印，啱晒。[[rule]]所以就算得一句，都建議寫大括號。",
          s.scene(Note(None), Type("nest.cpp", " {", after="if (mark >= 50)", at="fix"),
                  Type("nest.cpp", "    }\n", before="}", last=True), Expect("nest.cpp", N2),
                  Run(n2, at="cc", recall=True), Run(rn2, recall=True, keys=("t",)),
                  Note("冇大括號：if 只管下一句\n就算一句，都寫大括號", at="rule", where="editor"))),
    Scene("nested",
          "最後，if 入面可以再有 if，叫巢狀 if。[[type]]合格之後，再檢查係咪八十五分以上。[[cc]]運行，"
          "[[t1]]輸入九十分：[[o1]]Pass、Well done，同埋 Excellent；[[t2]]再試六十分：[[o2]]合格，但係冇 Excellent，因為裏面嗰個條件唔成立。",
          s.scene(Note(None), Type("nest.cpp", INNER, after='"Well done!\\n";\n', at="type"), Expect("nest.cpp", NEST),
                  Run(n3, at="cc", recall=True), Run(rn3, recall=True, keys=("t1",)), Run(rn4, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("recap",
          "總結：[[r1]]else if 可以處理多個選擇；[[r2]]由上至下，第一個成立就停，所以次序好重要；[[r3]]if 入面可以再有 if；"
          "[[r4]]冇大括號，if 只管一句，所以一定要寫大括號。",
          BulletCard("今集重點", [("else if：多個選擇", "r1"), ("第一個成立就停：次序好重要", "r2"),
                                ("巢狀 if：if 入面再有 if", "r3"), ("永遠寫大括號 { }", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入溫度：三十度或以上印 Hot，二十至二十九度印 Warm，其他印 Cold。"
          "[[next]]下一集，我哋學 switch，另一種處理多個選擇嘅方法。多謝收睇，下次見！",
          EndCard("讀入溫度：30 度或以上印 Hot，20 至 29 度印 Warm，其他印 Cold。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

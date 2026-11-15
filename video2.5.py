#!/usr/bin/env python3
"""Video 23 (syllabus 2.5): 條件運算子

apple or apples: six lines of if/else become one line with ?:; inside cout without brackets it
is a real flood of errors (<< binds tighter than ==); brackets fix it; nested ?: versus a
readable else-if. Run `python3 video2.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 23
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-05"
FINAL = (CODE / "word.cpp").read_text()
TRAP = (CODE / "trap.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
ONE = "    std::string word = n == 1 ? \"apple\" : \"apples\";\n"
IFELSE = ("    std::string word;\n    if (n == 1) {\n        word = \"apple\";\n    } else {\n"
          "        word = \"apples\";\n    }\n")
V1 = FINAL.replace(ONE, IFELSE)
TRAP_BAD = TRAP.replace('(n == 1 ? "apple" : "apples")', 'n == 1 ? "apple" : "apples"')
CC = "g++ -std=c++20 -Wall -Wextra word.cpp -o word"
CT = "g++ -std=c++20 -Wall -Wextra trap.cpp -o trap"

(c1, r1, r3, c2, s1, s3, clr, t1, t2, rt, cch, rch) = cpp.session({"word.cpp": V1, "trap.cpp": TRAP_BAD}, [
    CC, Input("./word", ["1"]), Input("./word", ["3"]),
    Write("word.cpp", FINAL), CC, Input("./word", ["1"]), Input("./word", ["3"]),
    "clear", CT, Write("trap.cpp", TRAP), CT, "./trap",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["4 9"]),
], refresh=opts.fresh_runs, cols=48)
for a, b in ((r1, s1), (r3, s3)):
    assert a.output == b.output, (a.output, b.output)
assert r1.output.endswith("1 apple\n") and r3.output.endswith("3 apples\n")
err = cpp.visible(t1.output)
first = next(l for l in err.splitlines() if ": error: " in l)
assert "no match for 'operator=='" in first and t1.code != 0 and len(err.splitlines()) > 50, first
assert rt.output.strip() == "apples" and c1.code == c2.code == t2.code == cch.code == 0 and rch.output.endswith("Bigger: 9\n")

SAY = {"?:": "問號冒號", "?": "問號", "apple": "apple", "apples": "apples", "if else": "if else"}

s = Stage({"word.cpp": V1, "trap.cpp": TRAP_BAD}, title="條件運算子 ?:", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！有時 if else 只係為咗喺兩個值之間揀一個，寫成六行好似有啲長。今集學條件運算子：問號同冒號。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "條件 ? 值一 : 值二")),
    Scene("goal",
          "今集會講：[[b1]]條件運算子點寫；[[b2]]放入 cout 嘅陷阱；[[b3]]幾時唔好用。",
          BulletCard("今集學識", [("條件 ? 甲 : 乙", "b1"), ("放入 cout 要加括號", "b2"), ("幾時唔好用", "b3")])),
    Scene("ifelse",
          "[[open]]呢個程式問你有幾多個蘋果。[[if]]一個，就用單數 apple；[[else]]其他數目，就用複數 apples。"
          "[[long]]為咗揀一個字，寫咗六行。",
          s.scene(Open("word.cpp", at="open"), Mark((9, 11), at="if"), Mark((11, 13), at="else"), Mark((8, 13), at="long"))),
    Scene("run1",
          "[[cc]]先編譯運行試吓。[[t1]]輸入一，[[o1]]印出一個 apple；[[t2]]再運行，輸入三，[[o2]]就係三個 apples。單數同複數都啱。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("t1",)), Run(r3, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("ternary",
          "[[rep]]用條件運算子，一行就寫完。[[q]]問號前面係條件；[[a]]條件成立，就用冒號前面嘅值；[[b]]唔成立，就用冒號後面嘅值。",
          s.scene(Replace("word.cpp", IFELSE, ONE, at="rep"), Expect("word.cpp", FINAL), Mark(8, at="q"))),
    Scene("anatomy",
          "[[cond]]讀法係：n 係咪等於一？[[yes]]係嘅話，結果係 apple；[[no]]唔係，結果就係 apples。"
          "[[val]]成個式會變成一個值，再放入 word。",
          AnatomyCard("條件運算子", [
              Part("n == 1", "條件", BLUE, "cond"),
              Part(" ?", "", AMBER, "cond"),
              Part(" \"apple\"", "成立：用呢個", GREEN, "yes"),
              Part(" :", "", AMBER, "no"),
              Part(" \"apples\"", "唔成立：用呢個", RED, "no"),
          ], size=72, note=("成個式係一個值：放入 word", "val"))),
    Scene("run2",
          "[[cc]]編譯運行，[[t1]]一個，[[o1]]apple；[[t2]]三個，[[o2]]apples，同 if else 嘅結果一模一樣。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(s1, recall=True, keys=("t1",)),
                  Run(s3, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("trap",
          "可唔可以直接放入 cout？[[open]]試吓咁寫。[[cc]]編譯，[[err]]出咗成百行錯誤！[[first]]記住，先睇第一個錯誤："
          "佢話 cout 同一，冇得用兩個等號比較。",
          s.scene(Run(clr), Open("trap.cpp", at="open"), Mark(5, at="open"), Run(t1, at="cc"),
                  Note("第一個 error：\nno match for 'operator=='", at="first", where="editor"))),
    Scene("trap_why",
          "因為兩個細過號嘅優先次序，比兩個等號高。[[order]]C++ 會先計 cout 輸出 n，再攞個結果同一比較，當然唔得。"
          "[[fix]]加返括號，先計條件運算子。[[cc]]再編譯運行，[[o]]印出 apples，因為 n 係二。今次冇問題。",
          s.scene(Note("<< 比 == 先計：\n(cout << n) == 1 ？", at="order", where="editor"), Note(None, at="fix"),
                  Replace("trap.cpp", 'n == 1 ? "apple" : "apples"', '(n == 1 ? "apple" : "apples")', at="fix"),
                  Expect("trap.cpp", TRAP), Run(clr, at="cc"), Run(t2, recall=True), Run(rt))),
    Scene("when",
          "條件運算子適合簡單嘅二揀一。[[bad]]如果一層包一層，好似咁計等級，就好難睇；[[good]]呢個時候，用返 else if 會清楚好多。",
          CodeCompareCard("幾時唔好用？", [
              Pane("一層包一層", "char g = m >= 85 ? 'A'\n       : m >= 70 ? 'B'\n       : m >= 55 ? 'C' : 'F';",
                   False, "bad"),
              Pane("用 else if", "if (m >= 85) {\n    g = 'A';\n} else if (m >= 70) {\n    g = 'B';\n} else ...",
                   True, "good"),
          ], size=28)),
    Scene("recap",
          "總結：[[r1]]條件問號甲冒號乙：成立就係甲，唔成立就係乙；[[r2]]成個式係一個值；[[r3]]放入 cout 記得加括號；"
          "[[r4]]複雜嘅條件，用返 if else。",
          BulletCard("今集重點", [("條件 ? 甲 : 乙", "r1"), ("成個式係一個值", "r2"), ("放入 cout：加括號", "r3"),
                                ("複雜就用 if else", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入兩個整數，用條件運算子揀出比較大嗰個，印出嚟。"
          "[[next]]下一集開始學迴圈：while。多謝收睇，下次見！",
          EndCard("讀入兩個整數，用條件運算子揀出比較大嗰個，印出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

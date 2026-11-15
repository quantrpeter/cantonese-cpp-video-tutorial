#!/usr/bin/env python3
"""Video 18 (syllabus 1.12): 小項目：BMI 計算機

Part 1's project: read weight and height, convert cm to m with a named constant, compute BMI,
print one decimal place. The natural first try `kg / m * m` really prints the weight back
(60.0); brackets fix it. Run `python3 video18.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 18
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-12"
FINAL = (CODE / "bmi.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SKEL = "#include <iostream>\n\nint main() {\n}\n"
INC = "#include <iomanip>\n"
CONST = "    constexpr double cmPerM = 100.0;\n"
IN_KG = "    double kg{};\n    std::cout << \"Weight (kg): \";\n    std::cin >> kg;\n"
IN_CM = "    double cm{};\n    std::cout << \"Height (cm): \";\n    std::cin >> cm;\n"
CALC_M = "\n    double m = cm / cmPerM;\n"
CALC_BAD = "    double bmi = kg / m * m;\n"
OUT = "    std::cout << std::fixed << std::setprecision(1);\n    std::cout << \"BMI: \" << bmi << '\\n';\n"
BAD = SKEL.replace("#include <iostream>\n", "#include <iostream>\n" + INC).replace("}\n", CONST + IN_KG + IN_CM + CALC_M + CALC_BAD + OUT + "}\n")
assert BAD.replace("kg / m * m", "kg / (m * m)") == FINAL
CC = "g++ -std=c++20 -Wall -Wextra bmi.cpp -o bmi"

(c1, r1, c2, r2, r3, cch, rch) = cpp.session({"bmi.cpp": BAD}, [
    CC, Input("./bmi", ["60", "165"]),
    Write("bmi.cpp", FINAL), CC, Input("./bmi", ["60", "165"]), Input("./bmi", ["70", "175"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["165"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("BMI: 60.0\n") and r2.output.endswith("BMI: 22.0\n") and r3.output.endswith("BMI: 22.9\n")
assert c1.code == c2.code == cch.code == 0 and "Healthy weight: 50.4 - 62.3 kg" in rch.output, rch.output

SAY = {"setprecision(1)": "set precision 一", "setprecision": "set precision", "iomanip": "I O manip",
       "constexpr": "const expr", "BMI": "B M I", "std::fixed": "S T D fixed", "fixed": "fixed"}

s = Stage({"bmi.cpp": SKEL}, title="小項目：BMI 計算機", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！第一章嘅小項目：BMI 計算機。我哋會用晒呢一章學過嘅嘢：變數、輸入、計數、常數，同埋格式化輸出。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "輸入 · 計算 · 輸出")),
    Scene("plan",
          "先諗清楚步驟：[[in]]讀入體重同身高；[[conv]]身高用厘米輸入，要轉做米；[[calc]]BMI 等於體重，除以身高嘅平方；"
          "[[out]]最後印出，保留一個小數位。",
          FlowCard("BMI 計算機：四個步驟", [Row("BMI", "計算機", BLUE, [
              Node("輸入", "kg、cm", "in"), Node("轉做米", "cm ÷ 100", "conv"),
              Node("計 BMI", "kg ÷ m²", "calc"), Node("輸出", "1 個小數位", "out"),
          ], note="輸入 → 處理 → 輸出", note_at="out")])),
    Scene("setup",
          "[[inc]]setprecision 要用 iomanip。[[c]]一米有一百厘米：用 constexpr 俾佢一個名，唔好寫神秘數字。",
          s.scene(Open("bmi.cpp", mode="instant"), Type("bmi.cpp", INC, after="#include <iostream>\n", at="inc"),
                  Type("bmi.cpp", CONST, after="int main() {\n", at="c"))),
    Scene("input",
          "[[kg]]讀體重，[[cm]]再讀身高。兩個都用 double，因為可能有小數；亦都記得初始化。",
          s.scene(Type("bmi.cpp", IN_KG, before="}", last=True, at="kg", rate=24),
                  Type("bmi.cpp", IN_CM, before="}", last=True, at="cm", rate=24))),
    Scene("calc",
          "[[m]]厘米除一百，變做米。[[bmi]]BMI 係體重除身高嘅平方，即係除 m 乘 m。",
          s.scene(Type("bmi.cpp", CALC_M, before="}", last=True, at="m", rate=20),
                  Type("bmi.cpp", CALC_BAD, before="}", last=True, at="bmi", rate=20))),
    Scene("output",
          "[[fmt]]用 fixed 加 setprecision(1)，印一個小數位；[[pr]]再印出 BMI。",
          s.scene(Type("bmi.cpp", OUT.splitlines(True)[0], before="}", last=True, at="fmt", rate=24),
                  Type("bmi.cpp", OUT.splitlines(True)[1], before="}", last=True, at="pr", rate=24), Expect("bmi.cpp", BAD))),
    Scene("run1",
          "[[cc]]編譯運行。[[w]]體重輸入六十公斤，[[h]]身高一百六十五厘米。[[out]]BMI 係六十？同體重一樣，好明顯唔啱。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("w", "h")), Note("BMI = 60.0？", at="out", where="editor"))),
    Scene("bug",
          "問題喺呢一行。[[mark]]除同乘嘅優先次序一樣，所以由左到右計：[[ltr]]先計 kg 除 m，再乘返 m，除咗又乘返，"
          "結果就係體重本身。[[fix]]要加括號，先計 m 乘 m。",
          s.scene(Note(None), Mark(14, at="mark"), Note("kg / m * m\n= (kg / m) * m = kg！", at="ltr", where="editor"),
                  Note(None, at="fix"), Replace("bmi.cpp", "kg / m * m", "kg / (m * m)", at="fix"), Expect("bmi.cpp", FINAL))),
    Scene("run2",
          "[[cc]]再編譯運行，同樣輸入六十同一百六十五，[[out]]BMI 係二十二點零，啱晒。"
          "[[again]]再試七十公斤、一百七十五厘米：[[out2]]二十二點九。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(r2, recall=True),
                  Run(r3, at="again", recall=True, keys=(("again", 1.6), "out2")))),
    Scene("structure",
          "睇返成個程式：[[k]]頂部係常數；[[i]]然後讀輸入；[[c]]再計數；[[o]]最後輸出。"
          "[[all]]輸入、處理、輸出：差唔多所有程式，都係呢個結構。",
          CodeCard("bmi.cpp", FINAL, "bmi.cpp", marks=[
              ((5, 5), "常數", "k", PURPLE), ((6, 11), "輸入", "i", BLUE),
              ((13, 14), "處理", "c", AMBER), ((15, 16), "輸出", "o", GREEN)], size=26)),
    Scene("recap",
          "第一章完成！我哋學咗：[[r1]]變數同基本型別；[[r2]]用 cin 讀輸入，同埋字串；[[r3]]算術運算，同整數除法、溢位、精度呢啲陷阱；"
          "[[r4]]常數同 auto。",
          BulletCard("第一章重點", [("變數、型別、初始化", "r1"), ("cin 輸入、std::string", "r2"),
                                  ("算術：整數除法、溢位、精度", "r3"), ("const、constexpr、auto", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 constexpr 加入健康 BMI 範圍：十八點五至二十二點九，計出你身高對應嘅健康體重範圍。"
          "[[next]]下一章，我哋學流程控制，等程式識得做決定。多謝收睇，下次見！",
          EndCard("用 constexpr 加入健康 BMI 範圍 18.5 至 22.9，計出你身高對應嘅健康體重範圍（體重 = BMI × m × m）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

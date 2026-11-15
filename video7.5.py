#!/usr/bin/env python3
"""Video 85 (syllabus 7.5): constexpr 函數同 if constexpr

static_assert(square(4) == 16) passes only while square is constexpr: without it the real error
is "call to non-'constexpr' function". consteval cube(3) works (25 27) but cube(n) with a plain
int n is a real "not a constant expression" error. describe() with a plain if fails for both
types (int has no .size(), string has no * 2); if constexpr compiles only the matching branch:
number 42 / text 5. Run `python3 video7.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 85
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-05"
FINAL = (CODE / "cexpr.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CUBE = "consteval int cube(int x) {\n    return x * x * x;\n}\n\n"
DESCRIBE = "template <typename T>" + FINAL.split("template <typename T>")[1].split("int main")[0]
CALLS = "    describe(21);\n    describe(std::string{\"hello\"});\n"
INCS = "#include <string>\n#include <type_traits>\n"
PRINT2 = "    std::cout << square(5) << ' ' << cube(3) << '\\n';\n"
PRINT1 = "    std::cout << square(5) << '\\n';\n"
BADB = FINAL.replace("if constexpr", "if")
V2 = FINAL.replace(INCS, "").replace(DESCRIBE, "").replace(CALLS, "")
V2C = V2.replace(PRINT2, "    int n = 3;\n" + PRINT2.replace("cube(3)", "cube(n)"))
V1 = V2.replace(CUBE, "").replace(PRINT2, PRINT1)
BADA = V1.replace("constexpr int square", "int square")
CC = "g++ -std=c++20 -Wall -Wextra cexpr.cpp -o ce"

(c1, r1, c2, clr, c3, r3, c4, clr2, c5, clr3, c6, r6, cch, rch) = cpp.session({"cexpr.cpp": V1}, [
    CC, "./ce", Write("cexpr.cpp", BADA), CC, "clear", Write("cexpr.cpp", V2), CC, "./ce", Write("cexpr.cpp", V2C), CC,
    "clear", Write("cexpr.cpp", BADB), CC, "clear", Write("cexpr.cpp", FINAL), CC, "./ce",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "25\n" and r3.output == "25 27\n" and r6.output == "25 27\nnumber 42\ntext 5\n", (r1.output, r6.output)
assert "call to non-'constexpr' function 'int square(int)'" in cpp.visible(c2.output)
assert "the value of 'n' is not usable in a constant expression" in cpp.visible(c4.output)
e5 = cpp.visible(c5.output)
assert "request for member 'size' in 'value', which is of non-class type 'const int'" in e5 and "no match for 'operator*'" in e5
assert c1.code == c3.code == c6.code == cch.code == 0 and rch.output == "3628800\n"

SAY = {"constexpr": "const expr", "consteval": "const eval", "if constexpr": "if const expr", "static_assert": "static assert",
       "std::is_integral_v<T>": "is integral v T", "is_integral_v": "is integral v", "square": "square", "cube": "cube",
       "describe": "describe", "value.size()": "value 點 size", "type_traits": "type traits", "factorial": "factorial", "T": "T"}

s = Stage({"cexpr.cpp": V1}, title="constexpr 同 if constexpr", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！有啲計數，答案喺編譯嗰陣已經知道，點解要留到運行先計？今集學 constexpr 同 consteval：叫編譯器幫你計；仲有 if constexpr：按類型揀 code。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "constexpr · consteval · if constexpr")),
    Scene("goal",
          "今集會講：[[b1]]constexpr 函數；[[b2]]static_assert 喺編譯時檢查；[[b3]]consteval，一定要喺編譯時計；[[b4]]if constexpr 按類型揀分支。",
          BulletCard("今集學識", [("constexpr 函數", "b1"), ("static_assert", "b2"), ("consteval", "b3"), ("if constexpr", "b4")])),
    Scene("cexpr",
          "[[fn]]square 前面加 constexpr：佢可以喺編譯嗰陣計。[[sa]]static_assert 喺編譯時檢查：square 四一定要係十六，唔係就編譯失敗。"
          "[[cc]]main 再印 square 五。編譯運行，[[o]]二十五：佢平時運行嗰陣都照用得，同普通函數一樣。",
          s.scene(Open("cexpr.cpp", at="fn"), Mark(3, at="fn"), Mark(8, at="sa"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("noce",
          "[[type]]如果刪走 constexpr 呢？[[cc]]編譯：[[err]]錯誤，static_assert 唔可以叫一個唔係 constexpr 嘅函數，因為編譯器唔肯定佢可以喺編譯時計。",
          s.scene(Replace("cexpr.cpp", "constexpr int square", "int square", at="type"), Expect("cexpr.cpp", BADA),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("ceval",
          "[[fix]]加返 constexpr。[[type]]再寫一個 cube，用 consteval：佢一定要喺編譯時計。[[cc]]印埋 cube 三，編譯運行，[[o]]二十五同二十七。二十七喺編譯嗰陣已經計好。",
          s.scene(Run(clr, at="fix"), Replace("cexpr.cpp", "int square", "constexpr int square", at="fix"),
                  Type("cexpr.cpp", CUBE, before="int main", at="type", rate=30), Replace("cexpr.cpp", PRINT1, PRINT2, at="cc"),
                  Expect("cexpr.cpp", V2), Run(c3, recall=True), Run(r3, at="o"))),
    Scene("evalerr",
          "[[type]]如果傳一個普通變數 n 入 cube 呢？[[cc]]編譯：[[err]]錯誤：n 唔係常數，cube 冇辦法喺編譯時計。consteval 就係咁嚴格。",
          s.scene(Replace("cexpr.cpp", PRINT2, "    int n = 3;\n" + PRINT2.replace("cube(3)", "cube(n)"), at="type"), Expect("cexpr.cpp", V2C),
                  Run(c4, at="cc", recall=True), Scroll(at="err"))),
    Scene("compare",
          "[[ce]]constexpr：可以喺編譯時計，亦可以喺運行時計。[[cv]]consteval：一定要喺編譯時計。[[sa]]static_assert：編譯時檢查一個條件。",
          TableCard("三個 const 字頭", ["關鍵字", "幾時計"], [
              (["constexpr", "編譯時或者運行時"], "ce"),
              (["consteval", "一定喺編譯時"], "cv", AMBER),
              (["static_assert", "編譯時檢查條件"], "sa"),
          ], widths=[1.1, 1.6], code_cols=(0,), size=42)),
    Scene("plainif",
          "而家睇 if constexpr。[[type]]先 include string 同 type traits。describe 係一個模板：is integral v T 問 T 係咪整數；係，就印佢乘二；"
          "唔係，就當佢係字串，印佢嘅長度。"
          "[[call]]main 分別傳一個 int 同一個 string 入去。",
          s.scene(Run(clr2, at="type"), Replace("cexpr.cpp", V2C.split("int main")[1].rstrip("\n"), V2.split("int main")[1].rstrip("\n"), rate=30),
                  Replace("cexpr.cpp", "#include <iostream>\n", "#include <iostream>\n" + INCS, rate=40),
                  Type("cexpr.cpp", DESCRIBE.replace("if constexpr", "if"), before="int main", rate=70),
                  Type("cexpr.cpp", CALLS, before="}", last=True, at="call", rate=36), Expect("cexpr.cpp", BADB))),
    Scene("plainerr",
          "[[cc]]用普通 if，編譯：[[err]]兩個錯誤：T 係 int 嗰陣，int 冇 size；T 係 string 嗰陣，string 唔可以乘二。點解會咁？",
          s.scene(Run(c5, at="cc", recall=True), Scroll(at="err"))),
    Scene("why",
          "因為普通 if，兩個分支都要編譯得到；[[i]]T 係 int 嗰陣，else 嗰邊嘅 size 就錯；[[s]]T 係 string 嗰陣，乘二又錯。"
          "[[fix]]改做 if constexpr：條件喺編譯時決定，唔啱嗰個分支，直接唔編譯。",
          s.scene(Mark(18, at="i"), Mark(16, at="s"), Mark(15, at="fix"), Run(clr3, at="fix"),
                  Replace("cexpr.cpp", "    if (std::is_integral_v", "    if constexpr (std::is_integral_v", at="fix"), Expect("cexpr.cpp", FINAL))),
    Scene("run",
          "[[cc]]編譯運行：[[o]]二十五、二十七；number 四十二；text 五。同一個 describe，兩個類型各自行自己嘅分支。",
          s.scene(Mark(None), Run(c6, at="cc", recall=True), Run(r6))),
    Scene("recap",
          "總結：[[r1]]constexpr 函數可以喺編譯時計；[[r2]]static_assert 喺編譯時檢查；[[r3]]consteval 一定要喺編譯時計；"
          "[[r4]]if constexpr 喺編譯時揀分支，唔啱嘅分支唔會編譯。",
          BulletCard("今集重點", [("constexpr：編譯時都計得", "r1"), ("static_assert：編譯時檢查", "r2"), ("consteval：一定編譯時", "r3"),
                                ("if constexpr：按類型揀分支", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 constexpr 嘅 factorial，用 static_assert 檢查 factorial 五係一百二十，再印出 factorial 十。[[next]]下一集：variadic templates。"
          "多謝收睇，下次見！",
          EndCard("寫 constexpr long long factorial(int n)；static_assert(factorial(5) == 120)；印出 factorial(10)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

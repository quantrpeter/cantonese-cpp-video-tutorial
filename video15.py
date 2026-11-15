#!/usr/bin/env python3
"""Video 15 (syllabus 1.9): const 同 constexpr

A circle program (area.cpp) with the magic number 3.14159 typed twice (once wrong, 3.14195); a named
`const` fixes both; changing it is a real "read-only variable" error; constexpr with
std::numbers::pi; and the real error when a constexpr needs a value read with cin.
Run `python3 video15.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 15
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-09"
FINAL = (CODE / "area.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
V2 = FINAL.replace("#include <numbers>\n", "").replace("constexpr double pi = std::numbers::pi;", "const double pi = 3.14159;")
V1 = (V2.replace("    const double pi = 3.14159;\n", "").replace("pi * r * r", "3.14159 * r * r")
      .replace("2 * pi * r", "2 * 3.14195 * r"))
V3 = V2.replace("    double r{};\n", "    pi = 3;\n    double r{};\n")
V5 = FINAL.replace("    double area", "    constexpr double area")
CC = "g++ -std=c++20 -Wall -Wextra area.cpp -o area"

(c1, r1, c2, r2, c3, clr, c4, r4, c5, cch, rch) = cpp.session({"area.cpp": V1}, [
    CC, Input("./area", ["10"]),
    Write("area.cpp", V2), CC, Input("./area", ["10"]),
    Write("area.cpp", V3), CC,
    Write("area.cpp", FINAL), "clear", CC, Input("./area", ["10"]),
    Write("area.cpp", V5), CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
o1, o2, o4 = (r.output.split("\n")[1].split() for r in (r1, r2, r4))
assert o1 == ["314.159", "62.839"] and o2 == ["314.159", "62.8318"] and o4 == ["314.159", "62.8319"], (o1, o2, o4)
assert "assignment of read-only variable 'pi'" in cpp.visible(c3.output)
assert "not usable in a constant expression" in cpp.visible(c5.output)
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output.strip() == str(365 * 24 * 3600)

SAY = {"std::numbers::pi": "S T D numbers pi", "constexpr": "const expr", "numbers": "numbers"}

s = Stage({"area.cpp": V1}, title="const 同 constexpr")

scenes = [
    Scene("intro",
          "歡迎返嚟！程式入面突然出現嘅數字，例如三點一四一五九，叫做神秘數字。今集學點樣用 const 同 constexpr，俾佢哋一個名。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "const · constexpr · std::numbers::pi")),
    Scene("goal",
          "今集會講：[[b1]]乜嘢係神秘數字；[[b2]]const：唔可以改嘅變數；[[b3]]constexpr，同埋 C++20 嘅 std::numbers::pi。",
          BulletCard("今集學識", [("神秘數字 magic number", "b1"), ("const：唔可以改", "b2"),
                                ("constexpr 同 std::numbers::pi", "b3")])),
    Scene("magic",
          "[[open]]呢個程式計圓形嘅面積同周長。[[cc]]編譯運行，[[type]]半徑輸入十，"
          f"[[out]]面積係{zh_num(float(o1[0]), 3)}，周長係{zh_num(float(o1[1]), 3)}。",
          s.scene(Open("area.cpp", at="open"), Run(c1, at="cc"), Run(r1, keys=("type",)))),
    Scene("problem",
          "睇落冇問題。但係[[m1]]三點一四一五九寫咗兩次，[[m2]]而且第二個其實打錯咗，變咗一四一九五！"
          "[[what]]呢啲突然出現、冇名嘅數字，叫做神秘數字：人哋睇唔明係乜，要改又要逐個搵，好容易出錯。",
          s.scene(Mark(7, at="m1"), Mark(8, at="m2"), Note("3.14195？打錯咗！", at="m2", where="editor"),
                  Note("神秘數字：冇名、\n重複、容易打錯", at="what", where="editor"))),
    Scene("const",
          "解決方法：[[type]]喺頂部宣告一個常數 pi，前面加 const；[[rep]]然後將兩個數字都換做 pi。"
          f"[[cc]]編譯運行，[[out]]周長今次啱咗：{zh_num(float(o2[1]), 4)}。",
          s.scene(Note(None), Mark(None), Type("area.cpp", "    const double pi = 3.14159;\n", after="int main() {\n", at="type"),
                  Replace("area.cpp", "3.14159 * r * r", "pi * r * r", at="rep"),
                  Replace("area.cpp", "2 * 3.14195 * r", "2 * pi * r"), Expect("area.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=(("cc", 4.0),)))),
    Scene("const_err",
          "const 嘅意思係：設定咗之後，就唔可以再改。[[type]]如果試吓將 pi 改做三，[[cc]]編譯，"
          "[[err]]g++ 就會出錯：pi 係唯讀變數，唔可以改。[[undo]]刪走呢句。",
          s.scene(Type("area.cpp", "    pi = 3;\n", before="    double r{};", at="type"), Expect("area.cpp", V3),
                  Run(c3, at="cc", recall=True), Note("read-only variable：\n唯讀，唔可以改", at="err", where="editor"),
                  Replace("area.cpp", "    pi = 3;\n", "", at="undo"), Note(None), Expect("area.cpp", V2))),
    Scene("constexpr",
          "再進一步：[[cx]]將 const 改做 constexpr，意思係呢個值喺編譯嗰陣已經知道。[[inc]]C++20 仲有現成嘅 pi："
          f"include numbers，[[np]]就可以用 std::numbers::pi，比我哋自己打嘅更準確。[[cc]]編譯運行，[[out]]周長變咗{zh_num(float(o4[1]), 4)}，仲準確啲。",
          s.scene(Replace("area.cpp", "const double pi", "constexpr double pi", at="cx"),
                  Type("area.cpp", "#include <numbers>\n", after="#include <iostream>\n", at="inc"),
                  Replace("area.cpp", "3.14159;", "std::numbers::pi;", at="np"), Expect("area.cpp", FINAL),
                  Run(clr, at="cc"), Run(c4, recall=True), Run(r4, recall=True))),
    Scene("cx_err",
          "constexpr 有個限制。[[type]]如果將面積都寫成 constexpr，[[cc]]編譯，[[err]]就會出錯：r 嘅值唔可以用喺常數表達式，"
          "因為 r 要等運行嗰陣，使用者輸入咗先知道。[[undo]]改返做普通變數就得。",
          s.scene(Type("area.cpp", "constexpr ", before="double area", at="type"), Expect("area.cpp", V5),
                  Run(c5, at="cc", recall=True), Note("r 要運行時先知道：\n唔可以 constexpr", at="err", where="editor"),
                  Replace("area.cpp", "constexpr double area", "double area", at="undo"), Expect("area.cpp", FINAL))),
    Scene("table",
          "比較兩者：[[c]]const 係唔可以改，但個值可以等運行時先知道；[[cx]]constexpr 更嚴格，編譯嗰陣已經要知道個值。"
          "[[rule]]真正固定嘅常數，例如圓周率、一日有幾多秒，就用 constexpr。",
          TableCard("const 同 constexpr", ["寫法", "意思", "例子"], [
              (["const", "設定咗就唔可以改；個值可以運行時先知", "const double area = pi * r * r;"], "c"),
              (["constexpr", "編譯嗰陣已經要知道個值", "constexpr double pi = std::numbers::pi;"], "cx"),
          ], widths=[0.7, 1.3, 1.9], code_cols=(0, 2), size=38,
              note=("真正固定嘅常數（圓周率、一日幾多秒）：用 constexpr", "rule"))),
    Scene("recap",
          "總結：[[r1]]唔好用神秘數字，俾佢一個名；[[r2]]const 變數設定咗就唔可以改；[[r3]]constexpr 嘅值喺編譯時已經知道；"
          "[[r4]]C++20 有 std::numbers::pi。",
          BulletCard("今集重點", [("神秘數字 → 有名嘅常數", "r1"), ("const：唔可以改", "r2"),
                                ("constexpr：編譯時已經知道", "r3"), ("#include <numbers>：std::numbers::pi", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 constexpr 定義一年有幾多日、一日有幾多秒，再計出一年有幾多秒。"
          "[[next]]下一集，我哋講 auto：等編譯器幫你推斷型別。多謝收睇，下次見！",
          EndCard("用 constexpr 定義一年有幾多日、一日有幾多秒，再計出一年有幾多秒。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

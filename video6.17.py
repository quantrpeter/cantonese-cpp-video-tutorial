#!/usr/bin/env python3
"""Video 79 (syllabus 6.17): enum class

A plain enum Light really prints 0 for Red and converts to int silently; adding enum Fruit with
its own Orange is a real "'Orange' conflicts with a previous declaration" error. enum class fixes
the clash (Light::Orange) and refuses `int n = l;` (real error) until static_cast<int>. A switch
missing the Orange case is a real -Wswitch warning and a real bug (red green orange orange);
with every case: red green orange red. Run `python3 video79.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 79
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-17"
FINAL = (CODE / "light.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
A = "#include <iostream>\n\nenum Light { Red, Orange, Green };\n\nint main() {\n    Light l = Red;\n    int n = l;\n    std::cout << n << '\\n';\n}\n"
FRUIT = "enum Fruit { Apple, Orange };\n"
B = A.replace("enum Light", FRUIT + "enum Light")
C = B.replace("enum ", "enum class ").replace("= Red;", "= Light::Red;")
D = C.replace("int n = l;", "int n = static_cast<int>(l);")
CASE = "    case Light::Orange:\n        return Light::Red;\n"
MISS = FINAL.replace(CASE, "")
NEXT_MISS = "Light next" + MISS.split("Light next")[1].split("int main")[0]
MAIN_D = "int main" + D.split("int main")[1]
MAIN_F = "int main" + FINAL.split("int main")[1]
assert MISS == D.replace(MAIN_D, NEXT_MISS + MAIN_F)
CC = "g++ -std=c++20 -Wall -Wextra light.cpp -o light"

(c1, r1, c2, clr, c3, c4, r4, clr2, c5, r5, clr3, c6, r6, cch, rch) = cpp.session({"light.cpp": A}, [
    CC, "./light", Write("light.cpp", B), CC, "clear", Write("light.cpp", C), CC, Write("light.cpp", D), CC, "./light",
    "clear", Write("light.cpp", MISS), CC, "./light", "clear", Write("light.cpp", FINAL), CC, "./light",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "0\n" == r4.output and r5.output == "red green orange orange \n" and r6.output == "red green orange red \n"
assert "'Orange' conflicts with a previous declaration" in cpp.visible(c2.output)
assert "cannot convert 'Light' to 'int'" in cpp.visible(c3.output)
assert "enumeration value 'Orange' not handled in switch" in cpp.visible(c5.output) and c5.code == 0
assert c1.code == c4.code == c6.code == cch.code == 0 and rch.output == "1 0\n"

SAY = {"enum class": "enum class", "enum": "enum", "Light::Red": "Light 兩個冒號 Red", "Light::Orange": "Light 兩個冒號 Orange",
       "static_cast<int>": "static cast int", "static_cast": "static cast", "switch": "switch", "case": "case", "-Wswitch": "W switch",
       "Light": "Light", "Fruit": "Fruit", "Orange": "Orange", "Red": "Red", "Green": "Green", "Apple": "Apple", "next": "next",
       "Day": "Day", "isWeekend": "is weekend"}

s = Stage({"light.cpp": A}, title="enum class", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！交通燈得三種狀態：紅、橙、綠。用整數一、二、三去代表，好易搞亂。今集學 enum class：一個自己定義嘅類型，只有幾個有名嘅值。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "enum class · switch · 交通燈")),
    Scene("goal",
          "今集會講：[[b1]]舊式 enum 嘅兩個問題；[[b2]]enum class；[[b3]]static cast 變返整數；[[b4]]用 switch 處理每一個值。",
          BulletCard("今集學識", [("舊式 enum 嘅問題", "b1"), ("enum class", "b2"), ("static_cast<int>", "b3"), ("switch 處理晒", "b4")])),
    Scene("plain",
          "[[open]]舊式 enum：Light 有 Red、Orange、Green。[[int]]佢其實係整數，可以靜靜雞變成 int。[[cc]]編譯運行，[[o]]Red 係零，Orange 係一，Green 係二。佢只係幾個有名嘅整數。",
          s.scene(Open("light.cpp", at="open"), Mark(3, at="open"), Mark(7, at="int"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("clash",
          "[[type]]再加一個 Fruit，有 Apple 同 Orange。[[cc]]編譯：[[err]]錯誤！Orange 撞名。因為舊式 enum 嘅名，直接放咗喺外面。",
          s.scene(Type("light.cpp", FRUIT, before="enum Light", at="type"), Expect("light.cpp", B), Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("eclass",
          "[[type]]兩個都改做 enum class。[[scope]]而家每個名都收埋喺自己嘅類型入面，用嘅時候要寫 Light 兩個冒號 Red。[[cc]]編譯：[[err]]又錯："
          "Light 唔可以靜靜雞變 int。",
          s.scene(Run(clr, at="type"), Replace("light.cpp", "enum Fruit", "enum class Fruit", at="type"),
                  Replace("light.cpp", "enum Light", "enum class Light"), Replace("light.cpp", "= Red;", "= Light::Red;", at="scope"),
                  Expect("light.cpp", C), Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("cast",
          "[[why]]呢個係好事：唔會無意中當咗數字用。[[type]]真係要個數，就要講明：static cast int。[[cc]]編譯運行，[[o]]印出零，同之前一樣，但係而家係我哋自己講明要轉。",
          s.scene(Note("enum class：唔會自動變 int", at="why", where="editor"), Note(None, at="type"),
                  Replace("light.cpp", "int n = l;", "int n = static_cast<int>(l);", at="type"), Expect("light.cpp", D),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("compare",
          "比較一下：[[name]]舊式 enum 嘅名放喺外面，會撞；enum class 要加類型名，唔會撞。[[conv]]舊式會自動變 int；enum class 要 static cast。",
          TableCard("enum vs enum class", ["", "enum", "enum class"], [
              (["名", "Red：會撞名", "Light::Red"], "name"),
              (["變 int", "自動", "static_cast<int>"], "conv"),
          ], widths=[0.7, 1.3, 1.5], code_cols=(), size=42, note=("新 code：一律用 enum class", "conv"))),
    Scene("switch",
          "[[fn]]寫 next：用 switch 決定下一個燈，紅變綠，綠變橙。[[loop]]main 由紅色開始，轉四次，用個數做 index 印個名。"
          "[[cc]]編譯：[[warn]]有警告：Orange 冇處理！運行：[[o]]紅、綠、橙，之後一直係橙，因為 Orange 冇 case，行到最尾 return l。燈壞咗。",
          s.scene(Run(clr2, at="fn"), Type("light.cpp", NEXT_MISS, before="int main", at="fn", rate=50),
                  Replace("light.cpp", MAIN_D.rstrip("\n"), MAIN_F.rstrip("\n"), at="loop", rate=60), Expect("light.cpp", MISS),
                  Run(c5, at="cc", recall=True), Scroll(at="warn"), Run(r5, at="o"))),
    Scene("fix",
          "[[type]]補返 Orange 嘅 case：橙之後變返紅。[[cc]]編譯運行，[[o]]冇警告，紅、綠、橙、紅。[[tip]]switch 一個 enum class，唔好寫 default，"
          "咁將來加新嘅值，g++ 就會提你。",
          s.scene(Run(clr3, at="type"), Type("light.cpp", CASE, after="        return Light::Orange;\n", at="type"), Expect("light.cpp", FINAL),
                  Run(c6, at="cc", recall=True), Run(r6), Note("switch enum：唔寫 default\n漏咗 g++ 會提你", at="tip", where="editor"))),
    Scene("recap",
          "總結：[[r1]]舊式 enum 會撞名，又會自動變 int；[[r2]]enum class 嘅值要寫類型名兩個冒號；[[r3]]要個數就用 static cast；"
          "[[r4]]switch 處理晒每個值，漏咗有警告。",
          BulletCard("今集重點", [("舊式 enum：撞名、變 int", "r1"), ("enum class：Light::Red", "r2"), ("static_cast<int>(l)", "r3"),
                                ("switch：處理晒，唔寫 default", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 Day，星期一到星期日，再寫 isWeekend，用 switch 判斷係咪週末。[[next]]下一集：第六部分嘅小項目，圖形面積計算器。"
          "多謝收睇，下次見！",
          EndCard("寫 enum class Day { Mon, …, Sun }；bool isWeekend(Day) 用 switch 處理晒七日。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

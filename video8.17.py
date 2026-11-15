#!/usr/bin/env python3
"""Video 104 (syllabus 8.17): variant 同 visit

std::variant<int, double, std::string> holding 42 has index() 0 and std::get<int> gives 42.
After v = "Amy", std::get<int>(v) really throws std::bad_variant_access ("std::get: wrong
index for variant", Aborted); holds_alternative<int>(v) answers 0 safely (index 2). std::visit
calls one lambda with whatever type is inside: 42 3.5 Ben. Run `python3 video104.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 104
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-17"
FINAL = (CODE / "variant.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SAFE = "    std::cout << std::holds_alternative<int>(v) << '\\n';\n"
GET = "    std::cout << std::get<int>(v) << '\\n';\n"
AMY = "    v = std::string{\"Amy\"};\n    std::cout << v.index() << ' ';\n"
ROW = "    std::vector<Value> row" + FINAL.split("    std::vector<Value> row")[1].rsplit("}\n", 1)[0]
V3 = FINAL.replace(ROW, "")
BAD = V3.replace(SAFE, GET)
V1 = BAD.replace(AMY + GET, "")
CC = "g++ -std=c++20 -Wall -Wextra variant.cpp -o var"

(c1, r1, c2, r2, clr, c3, r3, clr2, c4, r4, cch, rch) = cpp.session({"variant.cpp": V1}, [
    CC, "./var", Write("variant.cpp", BAD), CC, "./var", "clear", Write("variant.cpp", V3), CC, "./var",
    "clear", Write("variant.cpp", FINAL), CC, "./var",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "0 42\n" and r3.output == "0 42\n2 0\n" and r4.output == "0 42\n2 0\n42 3.5 Ben \n", r4.output
assert "std::bad_variant_access" in r2.output and r2.output.rstrip().endswith("Aborted") and r2.code != 0, r2.output
assert c1.code == c2.code == c3.code == c4.code == cch.code == 0 and rch.output == "2\n"

SAY = {"std::variant": "S T D variant", "variant": "variant", "std::visit": "S T D visit", "visit": "visit", "std::get<int>": "get int",
       "std::get": "S T D get", "index()": "index", "std::holds_alternative<int>": "holds alternative int", "holds_alternative": "holds alternative",
       "bad_variant_access": "bad variant access", "Value": "Value", "using": "using", "auto": "auto", "Amy": "Amy", "Ben": "Ben",
       "print": "print", "union": "union"}

s = Stage({"variant.cpp": V1}, title="variant 同 visit", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！試算表嘅一格，可能係整數、小數，又可能係文字。一個變數，點樣裝「幾種類型其中一種」？今集學 std::variant，同埋 std::visit。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "幾揀一 · get · visit")),
    Scene("goal",
          "今集會講：[[b1]]variant 係乜；[[b2]]index 同 get；[[b3]]攞錯類型會點；[[b4]]visit 自動按類型處理。",
          BulletCard("今集學識", [("variant<int, double, string>", "b1"), ("index()、std::get<int>", "b2"), ("攞錯：bad_variant_access", "b3"),
                                ("std::visit", "b4")])),
    Scene("basic",
          "[[using]]用 using 改個短名：Value 可以係 int、double 或者 string，但係每次只會係其中一種。[[set]]v 而家裝住四十二。[[get]]index 話裝緊第幾種，"
          "零即係 int；std::get int 攞個值出嚟。[[cc]]編譯運行，[[o]]零，四十二。同一個 v，之後亦可以改裝 double 或者 string。",
          s.scene(Open("variant.cpp", at="using"), Mark(6, at="using"), Mark(9, at="set"), Mark(10, at="get"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("box",
          "[[one]]variant 好似一個盒，入面有幾個位，但係同一時間只會用一個；[[idx]]index 就係講緊而家用緊邊個位。[[change]]重新賦值，就會換做另一種類型。",
          BoxesCard("std::variant<int, double, std::string>", [
              BoxRow([Box("0: int", "42", "用緊", at="one", color=GREEN, w=240), Box("1: double", "", "", at="one", w=240),
                      Box("2: string", "", "", at="one", w=240)], gap=20),
          ], notes=[("index()：用緊第幾個", "idx"), ("v = \"Amy\" → 換做 2", "change")], top=CONTENT_TOP + 40, row_h=250, box_h=110, size=40)),
    Scene("wrong",
          "[[type]]將 v 改做字串 Amy，印 index，再用 get int 攞值。[[cc]]編譯運行：[[o]]當機！bad variant access：入面係 string，你硬要攞 int。",
          s.scene(Type("variant.cpp", AMY + GET, before="}", last=True, at="type", rate=40), Expect("variant.cpp", BAD),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("safe",
          "[[type]]唔肯定入面係乜，就先問：holds_alternative int，有冇裝住 int。[[cc]]運行：[[o]]index 二，即係 string；係唔係 int？零，唔係。",
          s.scene(Run(clr, at="type"), Replace("variant.cpp", GET, SAFE, at="type", rate=40), Expect("variant.cpp", V3),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("visit",
          "逐個問好麻煩。[[type]]一行裝住三種嘅資料，[[lam]]寫一個 lambda，參數係 const auto reference：乜類型都收。[[visit]]std::visit 會睇清楚入面係乜，"
          "再用嗰個類型叫 lambda。[[cc]]運行：[[o]]四十二、三點五、Ben。",
          s.scene(Run(clr2, at="type"), Type("variant.cpp", ROW, before="}", last=True, at="type", rate=60), Expect("variant.cpp", FINAL),
                  Mark(15, at="lam"), Mark(17, at="visit"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("api",
          "[[i]]index 問第幾種；[[h]]holds_alternative 問係咪某種；[[g]]get 攞值，攞錯會當機；[[v]]visit 交俾一個函數，按真正嘅類型處理。",
          TableCard("std::variant 點用", ["寫法", "做乜"], [
              (["v.index()", "用緊第幾種"], "i"),
              (["std::holds_alternative<T>(v)", "係唔係 T"], "h"),
              (["std::get<T>(v)", "攞值；錯就拋 bad_variant_access"], "g", AMBER),
              (["std::visit(f, v)", "用真正類型叫 f"], "v", GREEN),
          ], widths=[1.6, 1.6], code_cols=(0,), size=36)),
    Scene("recap",
          "總結：[[r1]]variant 係幾種類型揀其中一種；[[r2]]index 同 holds_alternative 問入面係乜；[[r3]]get 攞錯類型會當機；[[r4]]visit 最方便，自動按類型處理。",
          BulletCard("今集重點", [("variant：幾揀一", "r1"), ("index / holds_alternative", "r2"), ("get 攞錯：當機", "r3"), ("std::visit", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]一行資料入面有數字同文字，用 holds_alternative 數有幾多格係文字。[[next]]下一集：string_view 同 span。多謝收睇，下次見！",
          EndCard("row {1, \"a\", 2.5, \"b\"}：用 std::holds_alternative<std::string> 數有幾多格係文字（答案 2）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

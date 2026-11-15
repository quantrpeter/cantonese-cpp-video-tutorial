#!/usr/bin/env python3
"""Video 113 (syllabus 9.5): std::expected

parseInt returns std::expected<int, std::string> (C++23, built with -std=c++23): a value, or
std::unexpected with the reason. The real run over "42", "4x2" and "" prints ok 42 / error: not a
digit / error: empty; value_or(-1) on "7x" prints -1. Compared with optional (no reason) and
exceptions (control jumps away). Run `python3 video9.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 113
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-05"
FINAL = (CODE / "parse.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
OR = "    std::cout << parseInt(\"7x\").value_or(-1) << '\\n';\n"
V1 = FINAL.replace(OR, "")
FN = "std::expected" + FINAL.split("std::expected", 1)[1].split("int main")[0]
MAIN1 = "int main" + V1.split("int main")[1]
S0 = FINAL.split("std::expected<int")[0] + MAIN1
CC = "g++ -std=c++23 -Wall -Wextra parse.cpp -o parse"

(c1, r1, c2, r2, cch, rch) = cpp.session({"parse.cpp": V1}, [
    CC, "./parse", Write("parse.cpp", FINAL), CC, "./parse",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++23 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
OUT = "ok 42\nerror: not a digit\nerror: empty\n"
assert r1.output == OUT and r2.output == OUT + "-1\n", r2.output
assert c1.code == c2.code == cch.code == 0 and rch.output == "3\nerror: divide by zero\n"

SAY = {"std::expected": "S T D expected", "std::expected<int, std::string>": "expected int string", "expected": "expected",
       "std::unexpected": "S T D unexpected", "unexpected": "unexpected", "r.error()": "r 點 error", "error()": "error", "*r": "星 r",
       "value_or(-1)": "value or 負一", "value_or": "value or", "parseInt": "parse int", "optional": "optional", "C++23": "C++ 二十三",
       "-std=c++23": "C++ 二十三", "4x2": "四 x 二", "7x": "七 x", "safeDivide": "safe divide"}

s = Stage({"parse.cpp": S0}, title="std::expected", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！將字串變做整數，可能會失敗：可能係空嘅，可能有唔係數字嘅字元。optional 只話到你失敗，唔話到你點解；exception 又會令程式跳走。"
          "C++23 嘅 std::expected，兩樣都兼顧。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "值 或者 錯誤 · C++23")),
    Scene("goal",
          "今集會講：[[b1]]expected 裝乜；[[b2]]成功同失敗點樣回傳；[[b3]]點樣檢查同攞值；[[b4]]同 optional、exception 比較。",
          BulletCard("今集學識", [("expected<T, E>", "b1"), ("return 值 / std::unexpected(…)", "b2"), ("if (r)、*r、r.error()", "b3"), ("vs optional、exception", "b4")])),
    Scene("fn",
          "[[type]]parseInt 回傳 expected int string：成功就係 int，失敗就係一個講原因嘅 string。[[empty]]空字串，就 return std::unexpected empty；[[digit]]見到唔係數字，"
          "return unexpected not a digit；[[ok]]成功就直接 return 個值。",
          s.scene(Open("parse.cpp", mode="instant"), Type("parse.cpp", FN, before="int main", at="type", rate=80), Mark((5, 6), at="type"),
                  Mark((7, 9), at="empty"), Mark((12, 14), at="digit"), Mark(17, at="ok"))),
    Scene("use",
          "[[loop]]main 試三個字串。[[check]]if r 檢查係咪成功，星號 r 攞個值；[[err]]失敗就用 r 點 error 攞原因。[[cc]]編譯，要用 C++ 二十三；運行：[[o]]ok 四十二；"
          "四 x 二，not a digit；空字串，empty。",
          s.scene(Mark(21, at="loop"), Mark((23, 24), at="check"), Mark((25, 26), at="err"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("valueor",
          "[[type]]唔理原因，只要一個預設值，就用 value_or。[[cc]]運行，[[o]]七 x 失敗，所以係負一。",
          s.scene(Type("parse.cpp", OR, before="}", last=True, at="type", rate=40), Expect("parse.cpp", FINAL), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("compare",
          "三種做法：[[opt]]optional 只話有冇，唔講原因；[[exc]]exception 講到原因，但係會跳過中間嘅 code，要有人 catch；[[exp]]expected 將值同原因一齊回傳，"
          "叫嘅人一定睇到，亦唔會跳走。",
          TableCard("失敗點樣通知？", ["做法", "講原因？", "控制流程"], [
              (["optional<T>", "唔講", "正常 return"], "opt"),
              (["throw exception", "講", "跳去 catch"], "exc"),
              (["expected<T, E>", "講", "正常 return"], "exp", GREEN),
          ], widths=[1.4, 0.9, 1.2], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]expected 裝一個值，或者一個錯誤；[[r2]]失敗用 std::unexpected 回傳原因；[[r3]]if r 檢查，星號攞值，error 攞原因，value_or 俾預設；[[r4]]要用 C++ 二十三。",
          BulletCard("今集重點", [("expected<T, E>：值或錯誤", "r1"), ("return std::unexpected(原因)", "r2"), ("if (r)、*r、r.error()、value_or", "r3"),
                                ("-std=c++23", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 safeDivide，除數係零就回傳錯誤 divide by zero，試十二除四同十二除零。[[next]]下一集：讀寫檔案。多謝收睇，下次見！",
          EndCard("寫 std::expected<int, std::string> safeDivide(int a, int b)：b 係 0 就 unexpected(\"divide by zero\")；試 12/4 同 12/0。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

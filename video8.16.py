#!/usr/bin/env python3
"""Video 103 (syllabus 8.16): optional

findMark returns std::optional<int>: found → 91 (checked with if (a), read with *a); not found →
std::nullopt, so has_value() is 0 and value_or(-1) gives -1. Calling .value() on the empty one
really ends the program: "terminate called after throwing an instance of
'std::bad_optional_access'" then Aborted. Run `python3 video8.16.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 103
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-16"
FINAL = (CODE / "find.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
ZOE = "    auto b = findMark(list, \"Zoe\");\n    std::cout << b.has_value() << ' ';\n    std::cout << b.value_or(-1) << '\\n';\n"
CRASH = "    std::cout << b.value() << '\\n';\n"
V1 = FINAL.replace(ZOE, "")
BAD = FINAL.replace(ZOE, ZOE.split("\n")[0] + "\n" + CRASH)
CC = "g++ -std=c++20 -Wall -Wextra find.cpp -o find"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"find.cpp": V1}, [
    CC, "./find", "clear", Write("find.cpp", BAD), CC, "./find", "clear", Write("find.cpp", FINAL), CC, "./find",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "91\n" and r3.output == "91\n0 -1\n", (r1.output, r3.output)
assert "std::bad_optional_access" in r2.output and r2.output.rstrip().endswith("Aborted") and r2.code != 0, r2.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "7 -1\n"

SAY = {"std::optional": "S T D optional", "std::optional<int>": "optional int", "optional": "optional", "std::nullopt": "S T D null opt",
       "nullopt": "null opt", "has_value()": "has value", "value_or(-1)": "value or 負一", "value_or": "value or", "value()": "value",
       "*a": "星 a", "if (a)": "if a", "findMark": "find mark", "bad_optional_access": "bad optional access", "Zoe": "Zoe", "Ben": "Ben",
       "Amy": "Amy", "-1": "負一", "toDigit": "to digit"}

s = Stage({"find.cpp": V1}, title="optional", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！一個搵學生分數嘅函數，如果搵唔到，應該回傳乜？負一？如果真係有人負一分呢？今集學 std::optional：一個可能有、可能冇嘅值。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "有定冇 · nullopt · value_or")),
    Scene("goal",
          "今集會講：[[b1]]魔術數字嘅問題；[[b2]]回傳 optional；[[b3]]檢查同攞值；[[b4]]冇值仲硬攞會點。",
          BulletCard("今集學識", [("-1 代表搵唔到？", "b1"), ("std::optional<int>", "b2"), ("if (a)、*a、value_or", "b3"), ("空嘅 .value()：當機", "b4")])),
    Scene("magic",
          "[[old]]以前好多人用一個特別嘅數，代表搵唔到，例如負一。[[bad]]但係呼叫嘅人好易忘記檢查，負一就當咗係分數；如果負一本身都係合法嘅值，就更加分唔到。",
          TableCard("點表示「搵唔到」？", ["做法", "問題"], [
              (["return -1;", "唔記得檢查 → 當咗係分數"], "old", RED),
              (["return std::nullopt;", "類型話明：可能冇"], "bad", GREEN),
          ], widths=[1.3, 1.7], code_cols=(0,), size=40)),
    Scene("code",
          "[[ret]]findMark 回傳 optional int。[[found]]搵到就直接 return 分數；[[none]]搵唔到就 return std::nullopt，即係冇值。[[use]]用嘅時候，if a 檢查有冇，"
          "星號 a 攞個值。[[cc]]編譯運行，[[o]]Ben 九十一分。一睇函數嘅回傳類型，就知道可能搵唔到。",
          s.scene(Open("find.cpp", at="ret"), Mark((11, 12), at="ret"), Mark(15, at="found"), Mark(18, at="none"), Mark((23, 26), at="use"),
                  Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("crash",
          "[[type]]如果搵 Zoe，佢唔喺度，但係我哋冇檢查，直接叫 value。[[cc]]編譯運行：[[o]]程式當機！話 bad optional access。冇值仲硬攞，就會咁。9.1 會再講呢種錯誤。",
          s.scene(Mark(None), Run(clr, at="type"), Type("find.cpp", ZOE.split("\n")[0] + "\n" + CRASH, before="}", last=True, at="type", rate=40),
                  Expect("find.cpp", BAD), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("safe",
          "[[type]]安全啲嘅做法：has_value 問有冇；value_or 負一：有就攞個值，冇就用負一代替，但係呢個係我哋喺用嘅地方自己揀嘅。[[cc]]運行：[[o]]零，即係冇值；同負一。今次冇當機。",
          s.scene(Run(clr2, at="type"), Replace("find.cpp", CRASH, ZOE.split("\n", 1)[1], at="type", rate=40), Expect("find.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("api",
          "optional 常用：[[chk]]if 或者 has_value 檢查；[[star]]星號攞值，冇值就未定義；[[val]]value 攞值，冇值就當機；[[or]]value_or 冇值就用預設。",
          TableCard("std::optional 點用", ["寫法", "冇值嘅時候"], [
              (["if (a) / a.has_value()", "false"], "chk"),
              (["*a", "未定義行為！"], "star", RED),
              (["a.value()", "拋出 bad_optional_access"], "val", AMBER),
              (["a.value_or(x)", "回傳 x"], "or", GREEN),
          ], widths=[1.5, 1.5], code_cols=(0,), size=38)),
    Scene("recap",
          "總結：[[r1]]optional 表示一個可能冇嘅值；[[r2]]冇值就回傳 std::nullopt；[[r3]]用之前先檢查，或者用 value_or；[[r4]]比魔術數字安全，因為類型本身已經講明。",
          BulletCard("今集重點", [("optional<T>：可能冇", "r1"), ("return std::nullopt;", "r2"), ("先檢查 / value_or", "r3"), ("勝過魔術數字", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 toDigit，收一個字元，係數字就回傳佢嘅值，唔係就回傳 nullopt。[[next]]下一集：variant 同 visit。多謝收睇，下次見！",
          EndCard("寫 std::optional<int> toDigit(char c)：'7' → 7，'x' → nullopt；用 value_or(-1) 印出 7 -1。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

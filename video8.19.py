#!/usr/bin/env python3
"""Video 106 (syllabus 8.19): std::format 同 std::print

The << chain really prints "Amy got 72, avg 68.456"; std::format with {:.1f} gives 68.5. A format
string asking for three values with only two given is a real compile-time error (call to
consteval function ... not a constant expression). C++23 std::print / std::println (built with
-std=c++23) really print "Amy   |   72|", 0068.456 and "ff 101". Run `python3 video8.19.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 106
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-19"
FINAL = (CODE / "fmt.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
FMT = '    std::string line = std::format("{} got {}, avg {:.1f}",\n                                   name, mark, avg);\n    std::cout << line << \'\\n\';\n'
PRINTS = "    std::print" + FINAL.split("    std::print", 1)[1].rsplit("}\n", 1)[0]
V2 = FINAL.replace(PRINTS, "").replace("#include <print>\n", "")
BAD = V2.replace("name, mark, avg);", "name, mark);")
V1 = V2.replace(FMT, "").replace("#include <format>\n", "")
CC = "g++ -std=c++23 -Wall -Wextra fmt.cpp -o fmt"

(c1, r1, clr, c2, r2, c3, clr2, c4, r4, cch, rch) = cpp.session({"fmt.cpp": V1}, [
    CC, "./fmt", "clear", Write("fmt.cpp", V2), CC, "./fmt", Write("fmt.cpp", BAD), CC, "clear", Write("fmt.cpp", FINAL), CC, "./fmt",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++23 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
L1, L2 = "Amy got 72, avg 68.456\n", "Amy got 72, avg 68.5\n"
assert r1.output == L1 and r2.output == L1 + L2 and r4.output == L1 + L2 + "Amy   |   72|\n0068.456\nff 101\n", r4.output
assert "call to consteval function" in cpp.visible(c3.output) and c3.code != 0
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "Amy     72\nBen      9\nCathy  100\n"

SAY = {"std::format": "S T D format", "std::print": "S T D print", "std::println": "S T D print line", "println": "print line",
       "{:.1f}": "大括號 冒號 點一 f", "{}": "大括號", "{:<6}": "靠左六格", "{:>5}": "靠右五格", "{:08.3f}": "零八點三 f", "{:x}": "x",
       "{:b}": "b", "consteval": "const eval", "-std=c++23": "C++ 二十三", "C++23": "C++ 二十三", "<<": "兩個細過號", "Amy": "Amy"}

s = Stage({"fmt.cpp": V1}, title="std::format 同 std::print", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！用 cout 一路接兩個細過號，又要控制小數位、對齊，寫起嚟好亂。C++20 有 std::format，C++23 再有 std::print：好似填表咁，一句搞掂。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "{} · {:.1f} · 對齊 · C++23")),
    Scene("goal",
          "今集會講：[[b1]]std::format 嘅大括號；[[b2]]小數位同對齊；[[b3]]編譯時檢查；[[b4]]C++23 嘅 print 同 println。",
          BulletCard("今集學識", [("std::format(\"{} …\", …)", "b1"), ("{:.1f}、{:<6}、{:>5}", "b2"), ("錯咗：編譯唔過", "b3"), ("std::print、std::println", "b4")])),
    Scene("old",
          "[[open]]傳統寫法：一段字、一個變數咁駁。[[cc]]編譯，今集用 C++ 二十三；運行：[[o]]平均分印咗六十八點四五六，想要一個小數位就麻煩。",
          s.scene(Open("fmt.cpp", at="open"), Mark((8, 9), at="open"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("format",
          "[[type]]用 std::format：先寫一句完整嘅句子，要填嘢嘅地方放大括號，再按次序將值放喺後面。[[spec]]冒號點一 f，就係一個小數位。"
          "[[cc]]運行：[[o]]六十八點五。成句字一眼睇晒，唔使再數兩個細過號。",
          s.scene(Run(clr, at="type"), Replace("fmt.cpp", "#include <iostream>\n", "#include <format>\n#include <iostream>\n", at="type", rate=40),
                  Type("fmt.cpp", FMT, before="}", last=True, rate=60), Expect("fmt.cpp", V2), Mark((11, 12), at="spec"), Mark(None, at="cc"),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("check",
          "[[type]]如果大括號有三個，但係只俾兩個值呢？[[cc]]編譯：[[err]]錯誤！format 字串喺編譯嗰陣已經檢查，數量唔夾就編譯唔過，唔會等到運行先出事。",
          s.scene(Replace("fmt.cpp", "name, mark, avg);", "name, mark);", at="type", rate=20), Expect("fmt.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("print",
          "[[fix]]補返 avg。[[type]]C++23 嘅 std::print 直接印，唔使 cout：[[align]]小於六係靠左佔六格，大於五係靠右佔五格；[[zero]]println 自動換行，"
          "零八點三 f 係用零補夠八格；[[hex]]x 係十六進制，b 係二進制。[[cc]]運行：Amy 後面補咗空格，七十二靠右；八格嘅零零六八；同埋 f f 同一零一。",
          s.scene(Run(clr2, at="fix"), Replace("fmt.cpp", "name, mark);", "name, mark, avg);", at="fix", rate=20),
                  Replace("fmt.cpp", "#include <iostream>\n", "#include <iostream>\n#include <print>\n", at="type", rate=40),
                  Type("fmt.cpp", PRINTS, before="}", last=True, rate=50), Expect("fmt.cpp", FINAL), Mark(15, at="align"), Mark(16, at="zero"),
                  Mark(17, at="hex"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("spec",
          "格式說明喺冒號後面：[[a]]靠左、靠右同寬度；[[f]]小數位；[[z]]用零補位；[[b]]進制。",
          TableCard("{:…} 格式", ["寫法", "結果"], [
              (["{:<6} / {:>5}", "Amy   |   72|"], "a"),
              (["{:.1f}", "68.5"], "f"),
              (["{:08.3f}", "0068.456"], "z"),
              (["{:x} / {:b}", "ff / 101"], "b"),
          ], widths=[1.2, 1.4], code_cols=(0, 1), size=40)),
    Scene("recap",
          "總結：[[r1]]std::format 用大括號填值，回傳一個 string；[[r2]]冒號後面寫格式：小數位、對齊、進制；[[r3]]數量唔夾，編譯已經捉到；[[r4]]C++23 嘅 print 同 println 直接印出嚟。",
          BulletCard("今集重點", [("std::format(\"{}\", x)", "r1"), ("{:.1f}、{:<6}、{:x}", "r2"), ("編譯時檢查", "r3"), ("std::print / println（C++23）", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 println 印一個整齊嘅表：名靠左佔六格，分數靠右佔四格。[[next]]下一集：chrono，計時間。多謝收睇，下次見！",
          EndCard("用 std::println(\"{:<6}{:>4}\", name, mark) 印 Amy 72、Ben 9、Cathy 100，令分數對齊。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

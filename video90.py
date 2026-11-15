#!/usr/bin/env python3
"""Video 90 (syllabus 8.3): vector 深入

Real capacity growth while pushing 9 ints: 1 2 4 4 8 8 8 8 16; with reserve(9) it stays 9.
emplace_back("Amy", 72) builds a Student in place (Amy 72). An iterator taken before a
push_back that reallocates really prints garbage, and AddressSanitizer really reports
heap-use-after-free on the old 12-byte block; taking the iterator after the push_back prints 1.
Run `python3 video90.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 90
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-03"
FINAL = (CODE / "vec.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
OK_ORDER = "    nums.push_back(4);\n    auto it = nums.begin();\n"
BAD_ORDER = "    auto it = nums.begin();\n    nums.push_back(4);\n"
NUMS = "    std::vector<int> nums{1, 2, 3};\n" + BAD_ORDER + "    std::cout << *it << '\\n';\n"
EMPLACE = "    std::vector<Student> s;\n    s.emplace_back(\"Amy\", 72);\n    std::cout << s[0].name << ' ' << s[0].mark << '\\n';\n"
STUDENT = "struct Student {\n    std::string name;\n    int mark;\n};\n\n"
DANGER = FINAL.replace(OK_ORDER, BAD_ORDER)
V3 = DANGER.replace(NUMS, "")
V2 = V3.replace(EMPLACE, "").replace(STUDENT, "").replace("#include <string>\n", "")
V1 = V2.replace("    v.reserve(9);\n", "")
CC = "g++ -std=c++20 -Wall -Wextra vec.cpp -o v"
ASAN = "g++ -std=c++20 -fsanitize=address vec.cpp -o v"

(c1, r1, c2, r2, clr, c3, r3, clr2, c4, r4, ca, ra, clr3, c5, r5, cch, rch) = cpp.session({"vec.cpp": V1}, [
    CC, "./v", Write("vec.cpp", V2), CC, "./v", "clear", Write("vec.cpp", V3), CC, "./v", "clear", Write("vec.cpp", DANGER), CC, "./v",
    ASAN, "./v", "clear", Write("vec.cpp", FINAL), CC, "./v",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
CAPS = "1 2 4 4 8 8 8 8 16 \n"
NINES = "9 9 9 9 9 9 9 9 9 \n"
assert r1.output == CAPS and r2.output == NINES and r3.output == NINES + "Amy 72\n", (r1.output, r2.output, r3.output)
junk = r4.output.split("\n")[2]
assert r4.output.startswith(NINES + "Amy 72\n") and junk != "1", r4.output
assert "heap-use-after-free" in ra.output and "12-byte region" in ra.output and ra.code != 0, ra.output[:400]
assert r5.output == NINES + "Amy 72\n1\n" and c1.code == c2.code == c3.code == c4.code == ca.code == c5.code == cch.code == 0
assert rch.output == "0 9\n0 0\n"

SAY = {"capacity": "capacity", "size": "size", "reserve": "reserve", "reserve(9)": "reserve 九", "emplace_back": "emplace back",
       "push_back": "push back", "push_back(4)": "push back 四", "*it": "星 it", "nums.begin()": "nums 點 begin",
       "heap-use-after-free": "heap use after free", "AddressSanitizer": "Address Sanitizer", "shrink_to_fit": "shrink to fit",
       "clear": "clear", "Student": "Student", "Amy": "Amy"}

s = Stage({"vec.cpp": V1}, title="vector 深入", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！vector 用咗咁耐，佢入面其實點運作？今集講 size 同 capacity、reserve、emplace_back，同埋一個好危險嘅陷阱：iterator 失效。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "capacity · reserve · emplace_back")),
    Scene("goal",
          "今集會講：[[b1]]size 同 capacity；[[b2]]reserve 預先留位；[[b3]]emplace_back 就地建立；[[b4]]iterator 失效。",
          BulletCard("今集學識", [("size vs capacity", "b1"), ("reserve", "b2"), ("emplace_back", "b3"), ("iterator 失效", "b4")])),
    Scene("cap",
          "[[loop]]逐個 push 九個數，每次印 capacity，即係而家總共有幾多格位。[[cc]]編譯運行：[[o]]一、二、四、四、八……十六。滿咗就加倍，同 7.7 嘅 MiniVector 一樣。",
          s.scene(Open("vec.cpp", at="loop"), Mark((6, 9), at="loop"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("realloc",
          "[[size]]size 係用咗幾多格，[[cap]]capacity 係開咗幾多格。[[move]]每次加倍，vector 要開一排新嘅記憶體，將舊嘢搬過去，再還舊嗰排。搬嘅次數唔多，但係每次都要時間。",
          BoxesCard("size vs capacity", [
              BoxRow([Box("", "0", "", at="size", color=BLUE, w=120), Box("", "1", "", at="size", color=BLUE, w=120),
                      Box("", "2", "", at="size", color=BLUE, w=120), Box("", "3", "", at="size", color=BLUE, w=120),
                      Box("", "4", "", at="size", color=BLUE, w=120), Box("", "", "", at="cap", w=120), Box("", "", "", at="cap", w=120),
                      Box("", "", "", at="cap", w=120)], gap=8, label="size 5 / capacity 8"),
          ], notes=[("滿咗：開新一排 → 搬過去 → 還舊嘅", "move")], top=CONTENT_TOP + 60, row_h=250, box_h=110, size=40)),
    Scene("reserve",
          "如果一早知道要放幾多個，[[type]]就用 reserve 預先開定位。[[cc]]運行，[[o]]由頭到尾都係九：一次都冇搬過。",
          s.scene(Type("vec.cpp", "    v.reserve(9);\n", after="    std::vector<int> v;\n", at="type"), Expect("vec.cpp", V2), Mark(6, at="type"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("emplace",
          "[[st]]再整一個 Student。[[em]]emplace_back 直接收建構嘅參數：名同分數，喺 vector 入面就地整出嚟，唔使先整一個再複製入去。"
          "[[cc]]運行，[[o]]Amy，七十二。",
          s.scene(Run(clr, at="st"), Replace("vec.cpp", "#include <iostream>\n", "#include <iostream>\n#include <string>\n", at="st", rate=40),
                  Type("vec.cpp", STUDENT, before="int main", rate=40), Type("vec.cpp", EMPLACE, before="}", last=True, at="em", rate=50),
                  Expect("vec.cpp", V3), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("danger",
          "而家係陷阱：[[take]]nums 有三個數，it 指住第一個。[[push]]然後 push_back 第四個。[[cc]]印星號 it，編譯運行：[[o]]印出 " + junk + "？唔係一！",
          s.scene(Run(clr2, at="take"), Type("vec.cpp", NUMS, before="}", last=True, at="take", rate=50), Expect("vec.cpp", DANGER),
                  Mark(22, at="take"), Mark(23, at="push"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("why",
          "[[full]]nums 一開始 capacity 係三，已經滿咗。[[move]]push_back 第四個，vector 就搬去一排新嘅記憶體，[[dangle]]舊嗰排還咗，"
          "但係 it 仲指住舊嗰度：iterator 失效。",
          BoxesCard("iterator 失效", [
              BoxRow([Box("舊（已還）", "1 2 3", "capacity 3", at="full", color=RED, w=320, key="old"),
                      Box("新", "1 2 3 4", "capacity 6", at="move", color=GREEN, w=360, key="new")], gap=160),
              BoxRow([Box("it", "仲指住舊嗰度", "", at="dangle", color=AMBER, w=360, key="it")]),
          ], arrows=[("old", "new", "move", GREEN), ("it", "old", "dangle", RED)], top=CONTENT_TOP + 10, row_h=260, box_h=110, size=40)),
    Scene("asan",
          "[[cc]]用 address sanitizer 證明：[[o]]heap use after free：讀咗一塊已經還咗嘅記憶體，[[sz]]正正係舊嗰排，十二 byte，即係三個 int。",
          s.scene(Run(ca, at="cc"), Run(ra, at="o"), Scroll(at="o"), Scroll(at="sz", find="is located"))),
    Scene("fix",
          "[[type]]解決方法：改完 vector 之後，先至攞 iterator；或者一早用 reserve 留夠位。[[cc]]運行，[[o]]一，正確。",
          s.scene(Run(clr3, at="type"), Replace("vec.cpp", BAD_ORDER, OK_ORDER, at="type", rate=30), Expect("vec.cpp", FINAL),
                  Run(c5, at="cc", recall=True), Run(r5))),
    Scene("recap",
          "總結：[[r1]]size 係用咗幾多，capacity 係開咗幾多，滿咗就加倍；[[r2]]知道數量就 reserve；[[r3]]emplace_back 就地建立；"
          "[[r4]]會令 vector 搬家嘅操作，會令舊嘅 iterator、指標同 reference 全部失效。",
          BulletCard("今集重點", [("size vs capacity", "r1"), ("reserve(n)", "r2"), ("emplace_back(參數…)", "r3"),
                                ("搬家之後：舊 iterator 失效", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個有九個元素嘅 vector，clear 之後印 size 同 capacity，再 shrink_to_fit，再印一次。[[next]]下一集：pair、tuple 同 structured bindings。"
          "多謝收睇，下次見！",
          EndCard("std::vector<int> v(9, 1); 之後 clear()，印 size、capacity；再 shrink_to_fit()，再印。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 94 (syllabus 8.7): set 同 multiset

Distinct visitors: "Amy Ben Amy Cat Ben Amy" into a std::set really gives 3: Amy Ben Cat
(sorted, no repeats). insert() returns {iterator, added}, so repeats can be reported (again: Amy,
again: Ben, again: Amy). A std::multiset keeps duplicates: count(72) is 3; erase(find(72))
removes one (64 72 72 91) but erase(72) removes all (size 2). Run `python3 video8.7.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 94
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-07"
FINAL = (CODE / "visit.cpp").read_text()
MULTI = (CODE / "multi.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
ADDED = ("        auto [it, added] = visitors.insert(name);\n        if (!added) {\n"
         "            std::cout << \"again: \" << name << '\\n';\n        }\n")
V1 = FINAL.replace(ADDED, "        visitors.insert(name);\n")
CC = "g++ -std=c++20 -Wall -Wextra visit.cpp -o visit"
IN = ["Amy Ben Amy Cat Ben Amy", "^D"]

(c1, r1, clr, c2, r2, clr2, cm, rm, cch, rch) = cpp.session({"visit.cpp": V1, "multi.cpp": MULTI}, [
    CC, Input("./visit", IN), "clear", Write("visit.cpp", FINAL), CC, Input("./visit", IN), "clear",
    "g++ -std=c++20 -Wall -Wextra multi.cpp -o multi", "./multi",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Amy Ben Amy Cat Ben Amy\n3: Amy Ben Cat\n", r1.output
assert r2.output == "Amy Ben Amy Cat Ben Amy\nagain: Amy\nagain: Ben\nagain: Amy\n3: Amy Ben Cat\n", r2.output
assert rm.output == "3\n64 72 72 91 \n2\n" and c1.code == c2.code == cm.code == cch.code == 0 and rch.output == "Amy Ben \n"

SAY = {"std::set": "S T D set", "std::multiset": "S T D multiset", "multiset": "multiset", "unordered_set": "unordered set",
       "insert": "insert", "added": "added", "count(72)": "count 七十二", "erase(72)": "erase 七十二", "find(72)": "find 七十二",
       "erase": "erase", "find": "find", "contains": "contains", "Amy": "Amy", "Ben": "Ben", "Cat": "Cat", "Dan": "Dan", "again": "again"}

s = Stage({"visit.cpp": V1, "multi.cpp": MULTI}, title="set 同 multiset", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！想知今日有幾多個唔同嘅人嚟過，同一個人嚟幾次都只計一次。今集學 std::set：自動去重複，仲排好序；同埋可以重複嘅 multiset。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "唔重複 · 排好序 · multiset")),
    Scene("goal",
          "今集會講：[[b1]]set 嘅特性；[[b2]]insert 回傳乜；[[b3]]multiset 容許重複；[[b4]]erase 嘅陷阱。",
          BulletCard("今集學識", [("set：唔重複、排好序", "b1"), ("auto [it, added] = insert(…)", "b2"), ("multiset：可以重複", "b3"),
                                ("erase(72) vs erase(find(72))", "b4")])),
    Scene("set",
          "[[decl]]一個裝名嘅 set。[[ins]]每讀到一個名就 insert。[[out]]最後印有幾多個，同埋全部名。[[cc]]編譯運行，[[t]]輸入六個名，Amy 嚟咗三次。"
          "[[o]]三個：Amy、Ben、Cat，重複嘅自動冇咗，仲排好序。我哋一句檢查都冇寫。",
          s.scene(Open("visit.cpp", at="decl"), Mark(6, at="decl"), Mark(9, at="ins"), Mark((11, 14), at="out"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1, at="t", type_rate=20))),
    Scene("what",
          "[[uniq]]set 同 map 好似，不過只有 key，冇 value。[[dup]]已經有嘅，再 insert 都唔會加。[[sorted]]而且一樣係排好序。",
          BoxesCard("std::set<std::string>", [
              BoxRow([Box("", "Amy", "", at="uniq", color=BLUE, w=200), Box("", "Ben", "", at="uniq", color=BLUE, w=200),
                      Box("", "Cat", "", at="uniq", color=BLUE, w=200)], gap=20),
              BoxRow([Box("insert", "\"Amy\"", "已經有：唔加", at="dup", color=RED, w=280)]),
          ], notes=[("只有 key、唔重複、排好序", "sorted")], top=CONTENT_TOP + 20, row_h=250, box_h=110, size=44)),
    Scene("insert",
          "想知邊個係重複？[[type]]insert 其實會回傳一個 pair：一個 iterator，同埋一個 bool：有冇真係加到。用 8.4 嘅 structured bindings 接住。"
          "[[cc]]運行，[[o]]Amy 兩次、Ben 一次，都話 again；最後一樣係三個人。added 係 false，就代表本身已經有。",
          s.scene(Run(clr, at="type"), Replace("visit.cpp", "        visitors.insert(name);\n", ADDED, at="type", rate=50), Expect("visit.cpp", FINAL),
                  Mark(9, at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2, type_rate=30))),
    Scene("multi",
          "如果想保留重複呢？[[open]]用 multiset。[[cnt]]五個分數，七十二有三個，count 七十二就係三。[[one]]erase find 七十二，只刪一個；"
          "[[all]]但係 erase 七十二，會刪晒全部七十二！[[cc]]運行：[[o]]三；刪一個之後仲有兩個七十二；最後淨返兩個數：六十四同九十一。",
          s.scene(Run(clr2, at="open"), Open("multi.cpp", at="open"), Mark(5, at="open"), Mark(6, at="cnt"), Mark(7, at="one"), Mark(12, at="all"),
                  Mark(None, at="cc"), Run(cm, at="cc"), Run(rm))),
    Scene("family",
          "[[s]]set：唔重複，排好序；[[m]]multiset：可以重複，排好序；[[u]]unordered_set：唔重複，冇次序，用 hash，平均最快。",
          TableCard("set 家族", ["容器", "重複", "次序"], [
              (["std::set", "唔得", "排好序"], "s"),
              (["std::multiset", "得", "排好序"], "m"),
              (["std::unordered_set", "唔得", "冇（hash）"], "u"),
          ], widths=[1.4, 0.8, 1], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]set 自動去重複，仲排好序；[[r2]]insert 回傳有冇加到；[[r3]]multiset 容許重複，count 數有幾多個；[[r4]]erase 一個值會刪晒，想刪一個就 erase find。",
          BulletCard("今集重點", [("set：唔重複、排好序", "r1"), ("insert → {it, added}", "r2"), ("multiset + count", "r3"),
                                ("erase(v) 刪晒；erase(find(v)) 刪一個", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]星期一同星期二各有一批訪客，用 set 搵出兩日都有嚟嘅人。[[next]]下一集：stack 同 queue。多謝收睇，下次見！",
          EndCard("monday {Amy, Ben, Cat}、tuesday {Ben, Dan, Amy}：用 set 同 contains 搵兩日都有嚟嘅人。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 92 (syllabus 8.5): map

Word count with std::map<std::string, int>: typing "the cat and the hat / and the bat" then
Ctrl+D really prints the words in alphabetical order (and 2, bat 1, cat 1, hat 1, the 3).
The trap: just reading count["dog"] really inserts it (size 5 → 6); count.contains("dog") does
not (5 0 5). Run `python3 video92.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 92
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-05"
FINAL = (CODE / "words.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SIZES = "    std::cout << count.size() << ' ';\n" + FINAL.split("    std::cout << count.size() << ' ';\n", 1)[1].rsplit("}\n", 1)[0]
V1 = FINAL.replace(SIZES, "")
BAD = FINAL.replace('count.contains("dog")', 'count["dog"]')
CC = "g++ -std=c++20 -Wall -Wextra words.cpp -o words"
IN = ["the cat and the hat", "and the bat", "^D"]
LIST = "and 2\nbat 1\ncat 1\nhat 1\nthe 3\n"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"words.cpp": V1}, [
    CC, Input("./words", IN), "clear", Write("words.cpp", BAD), CC, Input("./words", IN), "clear", Write("words.cpp", FINAL), CC,
    Input("./words", IN), Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
TYPED = "the cat and the hat\nand the bat\n"
assert r1.output == TYPED + LIST and r2.output == TYPED + LIST + "5 0 6\n" and r3.output == TYPED + LIST + "5 0 5\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "a 3\nb 1\nn 2\n"

SAY = {"std::map": "S T D map", "std::map<std::string, int>": "map string int", "count[word]++": "count 中括號 word 加加",
       "count[\"dog\"]": "count 中括號 dog", "contains": "contains", "count.contains(\"dog\")": "count 點 contains dog", "find": "find",
       "erase": "erase", "size": "size", "key": "key", "value": "value", "Ctrl+D": "Control D", "dog": "dog", "the": "the",
       "cat": "cat", "hat": "hat", "bat": "bat", "and": "and"}

s = Stage({"words.cpp": V1}, title="map", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！想數一篇文章入面每個字出現幾多次，就需要由「字」查到「次數」。今集學 std::map：一個由 key 對應去 value 嘅容器。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "key → value · 數字數")),
    Scene("goal",
          "今集會講：[[b1]]map 嘅樣；[[b2]]用中括號加一；[[b3]]map 自動排好序；[[b4]]一個查嘢嘅陷阱。",
          BulletCard("今集學識", [("key → value", "b1"), ("count[word]++", "b2"), ("按 key 排好序", "b3"), ("[] 查嘢會加嘢！", "b4")])),
    Scene("what",
          "[[kv]]map 入面每一格都係一對：key 同 value，好似字典：字係 key，次數係 value。[[uniq]]同一個 key 只會有一格。[[sort]]而且 map 永遠按 key 排好序。",
          BoxesCard("std::map<std::string, int>", [
              BoxRow([Box("and", "2", "", at="kv", color=BLUE, w=180), Box("bat", "1", "", at="kv", color=BLUE, w=180),
                      Box("cat", "1", "", at="kv", color=BLUE, w=180), Box("the", "3", "", at="kv", color=BLUE, w=180)], gap=20,
                     label="key：value"),
          ], notes=[("key 唔會重複", "uniq"), ("按 key 由細到大", "sort")], top=CONTENT_TOP + 60, row_h=250, box_h=110, size=44)),
    Scene("code",
          "[[decl]]map string 對 int。[[read]]不斷讀字；[[inc]]count 中括號 word 加加：呢個字嘅次數加一。[[print]]最後用 structured bindings，逐對印出嚟。",
          s.scene(Open("words.cpp", at="decl"), Mark(6, at="decl"), Mark(8, at="read"), Mark(9, at="inc"), Mark((11, 13), at="print"))),
    Scene("run1",
          "[[cc]]編譯運行，[[t]]輸入兩行字，再按 Control D 表示輸入完。[[o]]the 三次，and 兩次。留意次序：and、bat、cat、hat、the，係按字母排好嘅。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="t", type_rate=14))),
    Scene("brackets",
          "點解一句加加就得？[[miss]]中括號搵唔到個 key，就會自動加一格，value 由零開始；[[hit]]搵到，就直接攞嗰格。所以第一次見到就係零加一。",
          TableCard("count[word]++ 做咗乜", ["情況", "結果"], [
              (["word 未有", "加一格 {word, 0}，再加一 → 1"], "miss"),
              (["word 已經有", "嗰格加一"], "hit"),
          ], widths=[1, 2], code_cols=(), size=40)),
    Scene("trap",
          "但係呢個特性有陷阱。[[type]]印 size，再用中括號睇吓 dog 有幾多次，再印 size。[[cc]]運行：[[o]]五、零、六！只係查一查，map 就多咗一格 dog。因為中括號搵唔到，就會自動加一格，value 係零。如果 map 好大，查一次就加一格，好浪費，仲會改變結果。",
          s.scene(Run(clr, at="type"), Type("words.cpp", SIZES.replace('count.contains("dog")', 'count["dog"]'), before="}", last=True, at="type", rate=40),
                  Expect("words.cpp", BAD), Run(c2, at="cc", recall=True), Run(r2, type_rate=30))),
    Scene("contains",
          "[[type]]淨係想問有冇，就用 contains，C++20 先有。佢只係查，唔會加嘢。[[cc]]運行：[[o]]五、零、五，size 冇變。零即係 false：冇呢個字。淨係想問有冇，就唔好用中括號。",
          s.scene(Run(clr2, at="type"), Replace("words.cpp", 'count["dog"]', 'count.contains("dog")', at="type", rate=30), Expect("words.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3, type_rate=30))),
    Scene("ops",
          "常用操作：[[b]]中括號：攞或者加；[[c]]contains：問有冇；[[f]]find：搵到就回傳 iterator，搵唔到就係 end；[[e]]erase：刪走一格。",
          TableCard("map 常用操作", ["寫法", "做乜"], [
              (["m[k]", "攞；冇就加一格"], "b", AMBER),
              (["m.contains(k)", "有冇？唔會加"], "c", GREEN),
              (["m.find(k)", "iterator；冇就係 m.end()"], "f"),
              (["m.erase(k)", "刪走"], "e"),
          ], widths=[1.2, 1.6], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]map 由 key 對應 value，key 唔重複；[[r2]]永遠按 key 排好序；[[r3]]中括號攞唔到會自動加一格，數嘢好方便；[[r4]]淨係查，就用 contains 或者 find。",
          BulletCard("今集重點", [("key → value，key 唔重複", "r1"), ("按 key 排序", "r2"), ("m[k]：冇就加", "r3"), ("查：contains / find", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 map char 對 int，數 banana 每個字母出現幾多次。[[next]]下一集：unordered_map。多謝收睇，下次見！",
          EndCard("用 std::map<char, int> 數 \"banana\" 每個字母：應該係 a 3、b 1、n 2。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

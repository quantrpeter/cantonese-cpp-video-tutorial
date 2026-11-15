#!/usr/bin/env python3
"""Video 88 (syllabus 8.1): STL 全景

The standard library as three parts: containers, iterators, algorithms. One algorithm
(std::count) really works on a std::vector, a std::list and a std::string through
begin()/end(): 2 3 3. std::sort on the vector really prints 64 64 72 91.
Run `python3 video88.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 88
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-01"
FINAL = (CODE / "stl.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
COUNTS = "    auto a =" + FINAL.split("    auto a =")[1].split("    std::sort")[0]
SORT = "    std::sort" + FINAL.split("    std::sort")[1].rsplit("}\n", 1)[0]
V1 = FINAL.replace(SORT, "")
S0 = V1.replace(COUNTS, "")
CC = "g++ -std=c++20 -Wall -Wextra stl.cpp -o stl"

(c1, r1, c2, r2, cch, rch) = cpp.session({"stl.cpp": V1}, [
    CC, "./stl", Write("stl.cpp", FINAL), CC, "./stl",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "2 3 3\n" and r2.output == "2 3 3\n64 64 72 91 \n", (r1.output, r2.output)
assert c1.code == c2.code == cch.code == 0 and rch.output == "91 64 72 ananab\n"

SAY = {"STL": "S T L", "std::count": "S T D count", "std::sort": "S T D sort", "std::list": "S T D list", "std::vector": "S T D vector",
       "std::string": "S T D string", "begin()": "begin", "end()": "end", "begin": "begin", "end": "end", "iterator": "iterator",
       "iterators": "iterators", "unordered_map": "unordered map", "priority_queue": "priority queue", "std::reverse": "S T D reverse",
       "map": "map", "set": "set", "deque": "deque", "list": "list", "queue": "queue", "stack": "stack", "banana": "banana"}

s = Stage({"stl.cpp": S0}, title="STL 全景", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第八部分講 C++ 標準函式庫，通常叫 STL。佢有好多現成嘅容器同演算法，識得用，就唔使自己由零寫起。今集先睇全景。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "容器 · iterator · 演算法")),
    Scene("map",
          "STL 有三大部分：[[c]]容器，負責裝嘢，好似 vector、list、map；[[a]]演算法，負責做嘢，好似 sort、find、count；"
          "[[i]]中間用 iterator 連埋：演算法唔直接掂容器，而係經 iterator 一格一格咁行。",
          BoxesCard("STL 三大部分", [
              BoxRow([Box("容器", "vector · list · map", "裝嘢", at="c", color=BLUE, w=700, key="c")]),
              BoxRow([Box("iterator", "begin() … end()", "連接", at="i", color=AMBER, w=560, key="i")]),
              BoxRow([Box("演算法", "sort · find · count", "做嘢", at="a", color=GREEN, w=700, key="a")]),
          ], arrows=[("c", "i", "i", AMBER), ("i", "a", "i", AMBER)], top=CONTENT_TOP, row_h=250, box_h=120, size=54)),
    Scene("kinds",
          "容器有幾類：[[seq]]順序容器，按放入嘅次序排；[[assoc]]關聯容器，按 key 排好；[[hash]]無序容器，用 hash 搵得快；"
          "[[adapt]]仲有 stack、queue 呢啲轉接器。第八部分會逐個講。",
          TableCard("容器家族", ["類別", "例子", "邊集講"], [
              (["順序", "vector · deque · list · array", "8.3、8.10"], "seq"),
              (["關聯（排好序）", "map · set · multiset", "8.5、8.7"], "assoc"),
              (["無序（hash）", "unordered_map", "8.6"], "hash"),
              (["轉接器", "stack · queue · priority_queue", "8.8、8.9"], "adapt"),
          ], widths=[1, 1.9, 0.8], code_cols=(1,), size=34)),
    Scene("count",
          "[[open]]三個唔同嘅容器：一個 vector，一個 list，一個 string。[[type]]用同一個 std::count，分別數 vector 有幾多個六十四，list 有幾多個三，"
          "string 有幾多個 a。三次都係傳 begin 同 end。",
          s.scene(Open("stl.cpp", at="open"), Mark((8, 10), at="open"), Type("stl.cpp", COUNTS, before="}", last=True, at="type", rate=60),
                  Expect("stl.cpp", V1), Mark((11, 13), at=("type", 3.5)))),
    Scene("run1",
          "[[cc]]編譯運行：[[o]]二、三、三。[[why]]std::count 唔知亦唔理佢數緊乜容器，只係由 begin 行到 end，逐格比較。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1), Note("同一個演算法\n三種容器", at="why", where="editor"))),
    Scene("range",
          "[[b]]begin 指住第一個元素；[[e]]end 唔係最後一個，而係最後一個再後一格。[[half]]所以範圍係由 begin 開始，去到 end 之前。8.2 會詳細講。",
          BoxesCard("begin() 同 end()", [
              BoxRow([Box("", "72", "begin()", at="b", color=GREEN, w=140, key="b0"), Box("", "64", "", at="b", w=140),
                      Box("", "91", "", at="b", w=140), Box("", "64", "", at="b", w=140),
                      Box("", "（冇）", "end()", at="e", color=RED, w=140, key="e")], gap=10),
          ], notes=[("[begin, end)：包頭唔包尾", "half")], top=CONTENT_TOP + 60, row_h=250, box_h=120, size=40)),
    Scene("sort",
          "[[type]]再用 std::sort 將 vector 由細到大排，跟住逐個印出。[[cc]]編譯運行：[[o]]六十四、六十四、七十二、九十一。一句就排好。",
          s.scene(Note(None), Type("stl.cpp", SORT, before="}", last=True, at="type", rate=50), Expect("stl.cpp", FINAL),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("why",
          "點解要咁設計？[[nm]]如果有十種容器，二十個演算法，每個配搭都寫一次，就要寫二百次。[[it]]用 iterator 隔開，十種容器加二十個演算法，"
          "寫三十樣就夠。",
          TableCard("點解用 iterator？", ["設計", "要寫幾多次"], [
              (["每個容器 × 每個演算法", "10 × 20 = 200"], "nm", RED),
              (["容器 + iterator + 演算法", "10 + 20 = 30"], "it", GREEN),
          ], widths=[1.6, 1.2], code_cols=(), size=40)),
    Scene("recap",
          "總結：[[r1]]STL 有容器、iterator、演算法三部分；[[r2]]演算法經 begin 同 end 處理一段範圍；[[r3]]同一個演算法，可以用喺唔同容器；"
          "[[r4]]範圍包頭唔包尾。",
          BulletCard("今集重點", [("容器、iterator、演算法", "r1"), ("演算法：begin() 到 end()", "r2"), ("一個演算法，多種容器", "r3"),
                                ("[begin, end)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 std::reverse，將一個 vector 同一個 string 都倒轉，再印出嚟。[[next]]下一集：iterator。多謝收睇，下次見！",
          EndCard("用 std::reverse(begin, end) 倒轉 vector{72, 64, 91} 同 string \"banana\"，再印出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

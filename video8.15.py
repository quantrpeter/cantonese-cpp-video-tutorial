#!/usr/bin/env python3
"""Video 102 (syllabus 8.15): Ranges 同 views

std::sort(m.begin(), m.end()) becomes std::ranges::sort(m): 45 58 64 72 91. A pipeline
m | views::filter(pass) | views::transform(plus5) really prints 69 77 96, and because views are
lazy, after m[2] = 100 the same view prints 105 77 96. Run `python3 video8.15.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 102
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-15"
FINAL = (CODE / "ranges.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LOOP = "    for (int x : good) {\n        std::cout << x << ' ';\n    }\n    std::cout << '\\n';\n"
VIEW = "    auto pass" + FINAL.split("    auto pass")[1].split("    m[2] = 100;")[0]
AGAIN = "    m[2] = 100;\n" + LOOP
V2 = FINAL.replace(AGAIN, "")
V1 = V2.replace(VIEW, "").replace("#include <ranges>\n", "")
V0 = V1.replace("std::ranges::sort(m);", "std::sort(m.begin(), m.end());")
CC = "g++ -std=c++20 -Wall -Wextra ranges.cpp -o rg"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"ranges.cpp": V1}, [
    CC, "./rg", "clear", Write("ranges.cpp", V2), CC, "./rg", "clear", Write("ranges.cpp", FINAL), CC, "./rg",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
S = "45 58 64 72 91 \n"
assert r1.output == S and r2.output == S + "69 77 96 \n" and r3.output == S + "69 77 96 \n105 77 96 \n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "4 16 36 \n"

SAY = {"std::ranges::sort": "ranges sort", "std::ranges": "S T D ranges", "ranges": "ranges", "views": "views",
       "std::views::filter": "views filter", "views::filter": "views filter", "std::views::transform": "views transform",
       "views::transform": "views transform", "views::take": "views take", "views::iota": "views iota", "pass": "pass", "plus5": "plus 五",
       "good": "good", "m[2] = 100": "m 二 等如一百", "|": "直線", "<ranges>": "ranges"}

s = Stage({"ranges.cpp": V0}, title="Ranges 同 views", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！每次用演算法都要寫 begin 同 end，好長氣。C++20 嘅 ranges 可以直接傳成個容器；views 仲可以好似水管咁，一節節駁埋處理。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "ranges::sort · filter · transform · |")),
    Scene("goal",
          "今集會講：[[b1]]std::ranges 版本嘅演算法；[[b2]]views::filter 同 transform；[[b3]]用直線駁埋；[[b4]]views 係懶惰嘅。",
          BulletCard("今集學識", [("std::ranges::sort(m)", "b1"), ("views::filter、views::transform", "b2"), ("| 管道", "b3"), ("懶惰：用嗰陣先計", "b4")])),
    Scene("sort",
          "[[old]]以前要寫 begin 同 end。[[type]]改用 std::ranges::sort，直接傳 m 就得。[[cc]]編譯運行，[[o]]由細到大排好，結果同以前一樣，但係短咗好多。",
          s.scene(Open("ranges.cpp", at="old"), Mark(7, at="old"), Replace("ranges.cpp", "std::sort(m.begin(), m.end());", "std::ranges::sort(m);", at="type", rate=30),
                  Expect("ranges.cpp", V1), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("views",
          "[[type]]先寫兩個 lambda：pass 判斷合格，plus5 加五分。[[pipe]]然後 m 直線 filter pass，再直線 transform plus5：好似水管，資料由左流去右。"
          "[[cc]]運行，[[o]]六十九、七十七、九十六：合格嘅先加五分。",
          s.scene(Run(clr, at="type"), Replace("ranges.cpp", "#include <iostream>\n", "#include <iostream>\n#include <ranges>\n", at="type", rate=40),
                  Type("ranges.cpp", VIEW, before="}", last=True, rate=70), Expect("ranges.cpp", V2), Mark((15, 16), at="pipe"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("pipe",
          "[[m]]m 係原本嘅分數；[[f]]filter 只留低六十分或以上；[[t]]transform 將每個加五。[[nocopy]]中間冇整任何新嘅 vector。",
          BoxesCard("m | filter | transform", [
              BoxRow([Box("m", "45 58 64 72 91", "", at="m", color=BLUE, w=420, key="a")]),
              BoxRow([Box("filter(pass)", "64 72 91", "", at="f", color=AMBER, w=420, key="b")]),
              BoxRow([Box("transform(plus5)", "69 77 96", "", at="t", color=GREEN, w=420, key="c")]),
          ], arrows=[("a", "b", "f", AMBER), ("b", "c", "t", GREEN)], notes=[("唔使開新 vector", "nocopy")],
              top=CONTENT_TOP - 20, row_h=200, box_h=100, size=40)),
    Scene("lazy",
          "views 係懶惰嘅：[[type]]改 m 第二格做一百，再用返同一個 good 行一次。[[cc]]運行：[[o]]一百零五、七十七、九十六！[[why]]good 只係一個計法，"
          "每次行嘅時候先至睇 m 而家嘅值。",
          s.scene(Run(clr2, at="type"), Type("ranges.cpp", AGAIN, before="}", last=True, at="type", rate=50), Expect("ranges.cpp", FINAL),
                  Mark(21, at="type"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3),
                  Note("view：每次行先計\n冇自己嘅副本", at="why", where="editor"))),
    Scene("more",
          "常用嘅 views：[[f]]filter 揀；[[t]]transform 轉；[[k]]take 攞頭幾個；[[i]]iota 生成一串數。[[warn]]記住 view 冇自己嘅資料，原本嘅容器唔可以比 view 早消失。",
          TableCard("常用 views", ["view", "做乜"], [
              (["views::filter(f)", "留低 f 係 true 嘅"], "f"),
              (["views::transform(f)", "每個變成 f(x)"], "t"),
              (["views::take(n)", "頭 n 個"], "k"),
              (["views::iota(a, b)", "a、a+1 … b-1"], "i"),
          ], widths=[1.5, 1.5], code_cols=(0,), size=40, note=("view 唔擁有資料：原容器要仲喺度", "warn"))),
    Scene("recap",
          "總結：[[r1]]std::ranges 嘅演算法直接收成個容器；[[r2]]views 用直線駁埋，好似水管；[[r3]]中間唔使開新 vector；[[r4]]views 係懶惰嘅，每次行先計。",
          BulletCard("今集重點", [("ranges::sort(m)", "r1"), ("m | filter | transform", "r2"), ("冇中間 vector", "r3"), ("懶惰：每次行先計", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]由一到十九，揀雙數，平方，攞頭三個，用一條管道寫出嚟。[[next]]下一集：optional。多謝收睇，下次見！",
          EndCard("views::iota(1, 20) | filter(雙數) | transform(平方) | take(3)：應該係 4 16 36。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

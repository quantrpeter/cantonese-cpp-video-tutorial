#!/usr/bin/env python3
"""Video 22 (syllabus 2.4): switch

A drinks menu with switch, case, break and default; without one break, choice 1 really prints
Tea and Coffee (g++'s -Wimplicit-fallthrough warning); milk tea falls through on purpose with
[[fallthrough]]. Run `python3 video22.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 22
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-04"
FINAL = (CODE / "menu.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
MILK = "    case 3:\n        std::cout << \"Milk + \";\n        [[fallthrough]];\n"
V1 = FINAL.replace(MILK, "")
TEA_BREAK = "        std::cout << \"Tea\\n\";\n        break;\n"
NOBREAK = V1.replace(TEA_BREAK, "        std::cout << \"Tea\\n\";\n")
CC = "g++ -std=c++20 -Wall -Wextra menu.cpp -o menu"

(c1, r1, r2, r5, c2, rb, clr, c3, r3, r1b, cch, rch) = cpp.session({"menu.cpp": V1}, [
    CC, Input("./menu", ["1"]), Input("./menu", ["2"]), Input("./menu", ["5"]),
    Write("menu.cpp", NOBREAK), CC, Input("./menu", ["1"]),
    Write("menu.cpp", FINAL), "clear", CC, Input("./menu", ["3"]), Input("./menu", ["1"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["5"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("Tea\n") and r2.output.endswith("Coffee\n") and r5.output.endswith("No such drink\n")
assert "may fall through" in cpp.visible(c2.output), c2.output
assert rb.output.endswith("Tea\nCoffee\n") and r3.output.endswith("Milk + Tea\n") and r1b.output.endswith(": 1\nTea\n")
assert c1.code == c2.code == c3.code == cch.code == 0 and c3.output.strip() == "" and rch.output.endswith("Friday\n")

SAY = {"switch": "switch", "case": "case", "break": "break", "default": "default", "fall through": "fall through",
       "fallthrough": "fall through", "Milk + Tea": "Milk 加 Tea"}

s = Stage({"menu.cpp": V1}, title="switch：飲品餐牌", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！如果要根據一個數值，揀做邊樣嘢，好似餐牌咁，除咗 else if，仲可以用 switch。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "switch · case · break · default")),
    Scene("goal",
          "今集會講：[[b1]]switch 同 case；[[b2]]break 嘅作用；[[b3]]default；[[b4]]仲有 fall through，即係跌落去下一個 case。",
          BulletCard("今集學識", [("switch 同 case", "b1"), ("break：跳出 switch", "b2"), ("default：其他情況", "b3"),
                                ("fall through", "b4")])),
    Scene("open",
          "[[open]]呢個係飲品餐牌。[[sw]]switch 後面嘅括號，放要檢查嘅值；[[case]]每個 case 係一個可能嘅值，後面加冒號；"
          "[[brk]]break 就係跳出 switch；[[def]]全部 case 都唔啱，就會行 default。",
          s.scene(Open("menu.cpp", at="open"), Mark(8, at="sw"), Mark((9, 11), at="case"), Mark(11, at="brk"),
                  Mark((15, 16), at="def"))),
    Scene("run1",
          "[[cc]]編譯運行。[[t1]]揀一，[[o1]]印出 Tea。[[t2]]再運行，揀二，[[o2]]印出 Coffee。"
          "[[t3]]最後試吓揀五：[[o3]]餐牌冇第五款，所以行 default，印出 No such drink。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("t1",)), Run(r2, at="t2", recall=True, keys=(("t2", 0.9),)),
                  Run(r5, at="t3", recall=True, keys=(("t3", 0.9),)))),
    Scene("bug",
          "如果唔記得 break 會點？[[del]]刪走 Tea 後面嘅 break。[[cc]]編譯，[[warn]]g++ 警告：呢句可能會 fall through。"
          "[[t]]照運行，揀一，[[o]]Tea 同 Coffee 都印埋出嚟！",
          s.scene(Replace("menu.cpp", TEA_BREAK, "        std::cout << \"Tea\\n\";\n", at="del"), Expect("menu.cpp", NOBREAK),
                  Run(c2, at="cc", recall=True), Run(rb, at="t", recall=True, keys=(("t", 1.0),)),
                  Note("揀 1：Tea 同 Coffee 都有？", at="o", where="editor"))),
    Scene("why",
          "因為 case 只係一個入口：[[enter]]switch 跳咗去 case 一之後，[[down]]就會一直向下行，直到遇到 break，或者 switch 完結。"
          "[[fix]]所以每個 case 最尾，都要記得加 break。",
          s.scene(Note(None), Mark(9, at="enter"), Mark((9, 13), at="down"),
                  Note("case 係入口：入咗去就一直行\n直到 break", at="down", where="editor"),
                  Note(None, at="fix"), Mark(None, at="fix"), Type("menu.cpp", "        break;\n", after='"Tea\\n";\n', at="fix"),
                  Expect("menu.cpp", V1))),
    Scene("milk",
          "不過有時跌落去，正正係我哋想要嘅。[[menu]]餐牌第三款係奶茶，而家揀三係冇嘅。[[type]]奶茶即係奶加茶："
          "case 三先印 Milk，再故意跌落去 case 一，印 Tea。[[attr]]fallthrough 呢個標記，就係話俾編譯器聽：我係故意嘅，唔使警告。",
          s.scene(Mark(5, at="menu"), Mark(None, at="type"), Type("menu.cpp", MILK, after="switch (choice) {\n", at="type"),
                  Expect("menu.cpp", FINAL), Mark(11, at="attr"))),
    Scene("run2",
          "[[cc]]編譯，今次冇警告。[[t1]]揀三，[[o1]]Milk + Tea；[[t2]]揀一，[[o2]]就淨係 Tea，因為 Tea 後面有 break。",
          s.scene(Mark(None), Run(clr, at="cc"), Run(c3, recall=True), Run(r3, recall=True, keys=("t1",)),
                  Run(r1b, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("compare",
          "幾時用 switch，幾時用 else if？[[sw]]switch 適合一個值對多個固定選擇，例如餐牌編號、字元；"
          "[[ei]]但係範圍，例如八十五分或以上，switch 做唔到，就要用 else if。",
          TileCard("switch 定 else if？", [
              Tile("🎛️", "switch", "一個整數或者字元\n對幾個固定嘅值：1、2、3", "sw", BLUE),
              Tile("🪜", "else if", "範圍、複雜條件\n例如 mark >= 85", "ei", PURPLE),
          ], cols=2, height=360)),
    Scene("recap",
          "總結：[[r1]]switch 根據一個值，跳去對應嘅 case；[[r2]]每個 case 尾要加 break，唔係就會跌落去下一個；"
          "[[r3]]default 處理其他情況；[[r4]]故意跌落去，就用 fallthrough 標記。",
          BulletCard("今集重點", [("switch：跳去對應嘅 case", "r1"), ("每個 case 尾加 break", "r2"),
                                ("default：其他情況", "r3"), ("故意跌落去：[[fallthrough]];", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一至七嘅數字，用 switch 印出星期幾，其他數字就印 Invalid。"
          "[[next]]下一集，我哋學條件運算子：一個問號同一個冒號。多謝收睇，下次見！",
          EndCard("讀入 1 至 7 嘅數字，用 switch 印出星期幾（Monday … Sunday），其他數字印 Invalid。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

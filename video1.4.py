#!/usr/bin/env python3
"""Video 10 (syllabus 1.4): 用 cin 讀輸入

std::cin >> reads one number, then two in one statement; the input is typed into the real
program (cpp.Input), on one line, on two lines, with extra spaces, and as "abc", which makes
cin fail. Run `python3 video1.4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 10
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-04"
FINAL = (CODE / "add.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SKEL = "#include <iostream>\n\nint main() {\n}\n"
L1, L2 = "    int a{};\n", "    std::cout << \"First: \";\n"
L3, L4 = "    std::cin >> a;\n", "    std::cout << \"You typed \" << a << '\\n';\n"
V1 = SKEL.replace("}\n", L1 + L2 + L3 + L4 + "}\n")
V2 = (V1.replace(L1, L1 + "    int b{};\n").replace('"First: "', '"Two numbers: "').replace(">> a;", ">> a >> b;")
      .replace("\"You typed \" << a", "\"Sum: \" << a + b"))
assert V2 == FINAL
CC = "g++ -std=c++20 -Wall -Wextra add.cpp -o add"

(c1, r1, clr, c2, r2, r3, r4, r5, cch, rch) = cpp.session({"add.cpp": V1}, [
    CC, Input("./add", ["42"]),
    Write("add.cpp", V2), "clear", CC,
    Input("./add", ["3 4"]), Input("./add", ["3", "4"]), Input("./add", ["   10      20"]), Input("./add", ["abc"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["1 2 3"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "First: 42\nYou typed 42\n", r1.output
assert r2.output.endswith("Sum: 7\n") and r3.output.endswith("Sum: 7\n") and r4.output.endswith("Sum: 30\n")
assert r5.output.endswith("Sum: 0\n"), r5.output
assert c1.code == c2.code == cch.code == 0 and rch.output.endswith("Sum: 6\n")

SAY = {">>": "兩個大過號", "std::cin >> a": "S T D see in 兩個大過號 a", "cin >> a >> b": "see in 兩個大過號 a 兩個大過號 b",
       ">> a >> b": "兩個大過號 a 兩個大過號 b", "std::cin": "S T D see in", "cin": "see in", "Sum: 7": "Sum 七",
       "abc": "A B C", "Enter": "Enter"}

s = Stage({"add.cpp": SKEL}, title="用 cin 讀輸入")

scenes = [
    Scene("intro",
          "歡迎返嚟！到目前為止，我哋嘅程式每次運行，結果都一樣。今集學 cin，等使用者可以輸入資料，程式就有互動。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::cin · >> · 輸入")),
    Scene("goal",
          "今集會講：[[b1]]用 cin 讀取鍵盤輸入；[[b2]]一句讀幾個值；[[b3]]輸入嘅時候，空格同 Enter 點樣處理。",
          BulletCard("今集學識", [("用 std::cin 讀輸入", "b1"), ("一句讀幾個值", "b2"), ("空格同 Enter 點處理", "b3")])),
    Scene("type1",
          "[[t1]]先宣告一個變數 a。[[t2]]印一句提示，話俾使用者知要輸入乜。[[t3]]然後 std::cin >> a，"
          "即係由鍵盤讀一個數，放入 a。[[t4]]最後將 a 印返出嚟，睇吓佢讀到啲乜。",
          s.scene(Open("add.cpp", mode="instant"),
                  Type("add.cpp", L1, before="}", last=True, at="t1"),
                  Type("add.cpp", L2, before="}", last=True, at="t2"),
                  Type("add.cpp", L3, before="}", last=True, at="t3"),
                  Type("add.cpp", L4, before="}", last=True, at="t4"), Expect("add.cpp", V1))),
    Scene("anatomy",
          "[[cin]]std::cin 代表鍵盤輸入。[[arrow]]兩個大過號就好似箭咀，指住資料流動嘅方向：由 cin 流入 a。"
          "[[a]]a 就係用嚟裝住輸入嘅變數。[[cmp]]cout 用細過號，資料流出去；cin 用大過號，資料流入嚟。",
          AnatomyCard("std::cin >> a;", [
              Part("std::cin", "鍵盤輸入", BLUE, "cin"),
              Part(" >>", "流入去", AMBER, "arrow"),
              Part(" a", "裝住輸入嘅變數", GREEN, "a"),
              Part(";", "", MUTED, "a"),
          ], size=96, note=("cout <<：資料流出去　　cin >>：資料流入嚟", "cmp"))),
    Scene("run1",
          "[[cc]]編譯運行。[[wait]]程式印咗提示之後，就停喺度等。[[type]]我哋打四十二，撳 Enter，[[out]]佢就將四十二印返出嚟。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("type",)),
                  Note("cin 會停低，等你輸入", at="wait", where="editor"))),
    Scene("two",
          "而家改成讀兩個數。[[t1]]加多個變數 b；[[t2]]改吓提示；[[t3]]cin 後面可以一路接落去：>> a >> b，"
          "一句讀兩個值。[[t4]]最後印出兩個數嘅和。",
          s.scene(Note(None), Type("add.cpp", "    int b{};\n", after=L1, at="t1"),
                  Replace("add.cpp", '"First: "', '"Two numbers: "', at="t2"),
                  Type("add.cpp", " >> b", after=">> a", at="t3"),
                  Replace("add.cpp", "\"You typed \" << a", "\"Sum: \" << a + b", at="t4"), Expect("add.cpp", V2))),
    Scene("run2",
          "[[cc]]編譯運行。今次個程式會等你輸入兩個數。[[type]]我哋打三，空格，四，再撳 Enter。[[out]]Sum: 7，答案啱晒。",
          s.scene(Run(clr), Run(c2, at="cc"), Run(r2, keys=("type",)))),
    Scene("spaces",
          "[[run1]]如果打三，撳 Enter，再打四，[[out1]]結果都一樣。[[run2]]就算中間有好多個空格，[[out2]]都冇問題。"
          "[[why]]因為 cin 讀數字嘅時候，會跳過空格同 Enter，佢哋只係用嚟分隔每個值。",
          s.scene(Run(r3, at="run1", recall=True, keys=(("run1", 1.2), "out1")), Run(r4, at="run2", recall=True),
                  Note("空格、Enter：\n只係用嚟分隔每個值", at="why", where="editor"))),
    Scene("mistake",
          "但係如果打嘅唔係數字呢？[[type]]打 abc。[[out]]結果係零！因為 cin 讀唔到整數，就會失敗，"
          "a 變咗零，後面嘅 b 亦都唔會再讀。[[later]]點樣檢查輸入啱唔啱，我哋喺 2.8 會再講。",
          s.scene(Note(None), Run(r5, at="type", recall=True, keys=(("type", 1.0),)),
                  Note("cin 讀唔到整數：失敗\na 變 0，b 都唔再讀", at="out", where="editor"))),
    Scene("recap",
          "總結：[[r1]]std::cin >> a，由鍵盤讀一個值，放入 a；[[r2]]一句可以讀幾個值：cin >> a >> b；"
          "[[r3]]空格同 Enter 只係分隔；[[r4]]輸入唔係數字，cin 就會失敗。",
          BulletCard("今集重點", [("std::cin >> a：讀一個值放入 a", "r1"), ("一句讀幾個：cin >> a >> b", "r2"),
                                ("空格、Enter 只係分隔", "r3"), ("唔係數字：cin 會失敗", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]改吓個程式，一次過讀三個數，印出佢哋嘅總和。"
          "[[next]]下一集，我哋會學加減乘除，同埋除數嘅一個大陷阱。多謝收睇，下次見！",
          EndCard("改吓個程式，一次過讀三個數，印出佢哋嘅總和。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

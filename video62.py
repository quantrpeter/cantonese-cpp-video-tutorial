#!/usr/bin/env python3
"""Video 62 (syllabus 5.11): 未定義行為

Three bugs in one program, picked by input: reading a[3], int overflow, an uninitialised int.
Built normally they all "work" (real output: a plausible number, -2147483648, 0) with only a
-Wuninitialized warning; built with -fsanitize=address,undefined the first two are really
reported (UBSan + ASan, UBSan) and the third is not. Run `python3 video62.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 62
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-11"
FINAL = (CODE / "ub.cpp").read_text()
CC = "g++ -std=c++20 -Wall -Wextra ub.cpp -o ub"
CS = "g++ -std=c++20 -g -fsanitize=address,undefined ub.cpp -o ub"

(c1, p1, p2, p3, clr, c2, s1, s2, s3) = cpp.session({"ub.cpp": FINAL}, [
    CC, Input("./ub", ["1"]), Input("./ub", ["2"]), Input("./ub", ["3"]),
    "clear", CS, Input("./ub", ["1"]), Input("./ub", ["2"]), Input("./ub", ["3"]),
], refresh=opts.fresh_runs, cols=58)
assert "'x' is used uninitialized" in cpp.visible(c1.output)
assert all(r.code == 0 for r in (p1, p2, p3)) and p2.output.split()[-1] == "-2147483648"
plain1, plain3 = p1.output.split()[-1], p3.output.split()[-1]
v1 = cpp.visible(s1.output)
assert "index 3 out of bounds for type 'int [3]'" in v1 and "stack-buffer-overflow" in v1 and s1.code != 0
assert "signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'" in cpp.visible(s2.output)
assert "runtime error" not in s3.output and s3.code == 0 and c2.code == 0

SAY = {"UB": "U B", "AddressSanitizer": "Address Sanitizer", "UBSan": "U B San", "ASan": "A San",
       "-fsanitize=address,undefined": "dash F sanitize address undefined", "-Wall": "dash W all", "a[3]": "a 三",
       "runtime error": "runtime error"}

s = Stage({"ub.cpp": FINAL}, title="未定義行為", split=0.45, code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第五章最後一集：未定義行為。C++ 有啲錯誤，編譯器唔理，程式又唔一定當機，但係結果完全冇保證。今集學點樣捉住佢哋。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "undefined behaviour · sanitizer")),
    Scene("goal",
          "今集會講：[[b1]]乜嘢係未定義行為；[[b2]]三個常見例子；[[b3]]用 sanitizer 同警告捉佢哋。",
          BulletCard("今集學識", [("未定義行為 UB", "b1"), ("出界、溢位、未初始化", "b2"), ("sanitizer 同 -Wall", "b3")])),
    Scene("what",
          "未定義行為，即係 C++ 標準冇講會發生乜：[[ok]]可能啱啱好冇事，[[bad]]可能答案錯，可能當機；[[worst]]最慘係今日啱，換部電腦就錯。",
          TileCard("未定義行為 = 冇保證", [
              Tile("🙂", "睇落冇事", "今日啱", "ok", GREEN), Tile("🤪", "答案錯", "或者當機", "bad", AMBER),
              Tile("💣", "時好時壞", "換部電腦、開優化就變", "worst", RED),
          ], height=330)),
    Scene("code",
          "[[open]]呢個程式有三個錯：[[a]]第一個讀 a 中括號三，陣列只有三格，出咗界；[[b]]第二個 int 最大值再加一，溢位，1.6 見過；"
          "[[c]]第三個 x 冇初始化就印。[[pick]]main 讀入一個數，揀行邊一個。",
          s.scene(Open("ub.cpp", at="open"), Mark((4, 8), at="a"), Mark((10, 14), at="b"), Mark((16, 19), at="c"), Mark((22, 28), at="pick"))),
    Scene("plain",
          "[[cc]]用平時嘅指令編譯：[[warn]]淨係第三個有警告：x 未初始化。[[t1]]揀一，[[o1]]" + f"印出{zh_int(int(plain1))}；"
          "[[t2]]揀二，[[o2]]負二十一億；[[t3]]揀三，" + f"[[o3]]印出{zh_int(int(plain3))}。[[none]]三個都冇當機，好似冇問題咁！",
          s.scene(Mark(None), Run(c1, at="cc"), Run(p1, at="t1", keys=(("t1", 1.0),)), Run(p2, at="t2", recall=True, keys=(("t2", 1.0),)),
                  Run(p3, at="t3", recall=True, keys=(("t3", 1.0),)), Note("冇當機 ≠ 冇錯！", at="none", where="editor"))),
    Scene("san",
          "[[cc]]今次加 -fsanitize=address,undefined，同埋 -g。undefined 嗰個叫 UBSan，專捉未定義行為。[[t1]]揀一：[[o1]]即刻報錯："
          "[[top]]第七行，index 三出咗 int 三格陣列嘅界，ASan 跟住話係 stack buffer overflow。",
          s.scene(Note(None), Run(clr, at="cc"), Run(c2), Run(s1, at="t1", keys=(("t1", 1.0),)), Scroll(at="top"),
                  Note("ub.cpp:7：index 3 出界", at="top", where="editor"))),
    Scene("san2",
          "[[t2]]揀二：[[o2]]UBSan 話：第十二行，有號整數溢位，二十一億幾加一，int 裝唔落。[[t3]]揀三：[[o3]]乜都冇講。"
          "[[why]]g++ 嘅 sanitizer 捉唔到未初始化，所以要靠 -Wall 嘅警告。",
          s.scene(Note(None), Scroll(top=False), Run(s2, at="t2", recall=True, keys=(("t2", 1.0),)),
                  Run(s3, at="t3", recall=True, keys=(("t3", 1.0),)), Note("未初始化：sanitizer 捉唔到\n靠 -Wall 警告", at="why", where="editor"))),
    Scene("table",
          "總結三個例子：[[a]]出界，ASan 同 UBSan 都捉到；[[b]]有號整數溢位，UBSan 捉到；[[c]]未初始化，要靠編譯器嘅 -Wall 警告。",
          TableCard("邊個捉到？", ["錯誤", "普通編譯", "捉到佢嘅"], [
              (["a[3] 出界", f"印出 {plain1}", "UBSan + ASan"], "a"),
              (["int 溢位", "-2147483648", "UBSan"], "b"),
              (["未初始化", f"印出 {plain3}", "-Wall 警告"], "c"),
          ], widths=[1, 1, 1.2], code_cols=(), size=40)),
    Scene("rules",
          "所以寫程式嘅好習慣：[[r1]]永遠開 -Wall -Wextra，警告都要理；[[r2]]測試嘅時候，加 -fsanitize=address,undefined；"
          "[[r3]]唔好因為冇當機，就以為冇錯。",
          BulletCard("防範未定義行為", [("永遠開 -Wall -Wextra", "r1"), ("測試：-fsanitize=address,undefined", "r2"),
                                     ("冇當機 ≠ 冇錯", "r3")])),
    Scene("recap",
          "第五章完成！我哋學咗：[[r1]]記憶體、地址同指標；[[r2]]nullptr、懸空指標同 const 指標；[[r3]]new、delete 同 RAII；"
          "[[r4]]unique_ptr、shared_ptr，同埋點樣用 sanitizer 捉記憶體錯誤。",
          BulletCard("第五章重點", [("地址、指標、reference", "r1"), ("nullptr、懸空指標、const", "r2"), ("new / delete、RAII", "r3"),
                                  ("智能指標、sanitizer", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 -fsanitize=address,undefined 重新編譯你之前寫過嘅程式，例如 4.10 嘅井字過三關，睇吓有冇隱藏嘅錯誤。"
          "[[next]]下一章，我哋開始學物件導向。多謝收睇，下次見！",
          EndCard("用 -fsanitize=address,undefined 重新編譯你之前寫過嘅程式（例如 4.10 井字過三關），睇吓有冇隱藏錯誤。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

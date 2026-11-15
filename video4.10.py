#!/usr/bin/env python3
"""Video 51 (syllabus 4.10): 小項目：井字過三關

Part 4's project: a two-player tic-tac-toe with Grid (a 2D vector), show(), same(), wins() and a
main loop. Without the "taken" check O really takes X's square (stopped with Ctrl+C); with it, a
real game is played to X winning on a diagonal. Run `python3 video51.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 51
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-10"
FINAL = (CODE / "ttt.cpp").read_text()
HEAD = "#include <iostream>\n#include <vector>\n\n"
USING = "using Grid = std::vector<std::vector<char>>;\n\n"
SHOW = FINAL.split(USING)[1].split("bool same")[0]
SAME = "bool same" + FINAL.split("bool same")[1].split("bool wins")[0]
WINS = "bool wins" + FINAL.split("bool wins")[1].split("int main")[0]
P1 = "    Grid g(3, std::vector<char>(3, '.'));\n    char player = 'X';\n    int moves{0};\n"
P2 = ("    while (moves < 9) {\n        int r{};\n        int c{};\n        std::cout << player << \" (row col): \";\n"
      "        std::cin >> r >> c;\n")
P3 = "        if (r < 0 || r > 2 || c < 0 || c > 2) {\n            std::cout << \"Out of range!\\n\";\n            continue;\n        }\n"
TAKEN = "        if (g[r][c] != '.') {\n            std::cout << \"Taken!\\n\";\n            continue;\n        }\n"
P4 = ("        g[r][c] = player;\n        moves++;\n        show(g);\n        if (wins(g, player)) {\n"
      "            std::cout << player << \" wins!\\n\";\n            return 0;\n        }\n"
      "        player = (player == 'X') ? 'O' : 'X';\n    }\n    std::cout << \"Draw!\\n\";\n")
assert HEAD + USING + SHOW + SAME + WINS + "int main() {\n" + P1 + P2 + P3 + TAKEN + P4 + "}\n" == FINAL
BUG = FINAL.replace(TAKEN, "")
SKEL = HEAD + "int main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra ttt.cpp -o ttt"
GAME = ["1 1", "1 1", "0 0", "3 3", "0 2", "2 2", "2 0"]

(c1, r1, clr, c2, r2) = cpp.session({"ttt.cpp": BUG}, [
    CC, Input("./ttt", ["1 1", "1 1", "^C"]), Write("ttt.cpp", FINAL), "clear", CC, Input("./ttt", GAME),
], refresh=opts.fresh_runs, cols=48)
assert ". . . \n. O . \n. . . \n" in r1.output and r1.code == 130, r1.output
assert r2.output.count("Taken!") == 1 and r2.output.count("Out of range!") == 1 and r2.output.endswith("X wins!\n")
assert c1.code == c2.code == 0

SAY = {"using Grid": "using grid", "Grid": "grid", "show": "show", "same": "same", "wins": "wins", "continue": "continue",
       "Taken": "Taken", "Ctrl+C": "control C", "return": "return"}

s = Stage({"ttt.cpp": SKEL}, title="小項目：井字過三關", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第四章嘅小項目：井字過三關。兩個人輪流落子，邊個先連成一條線就贏。我哋會用到二維 vector、函數同迴圈。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "二維 vector · 函數 · 迴圈")),
    Scene("plan",
          "程式分四個部分：[[g]]Grid，用二維 vector 做棋盤；[[s]]show，印出棋盤；[[w]]wins，判斷有冇人贏；[[m]]main，負責輪流落子。",
          BulletCard("四個部分", [("Grid：3 × 3 棋盤（二維 vector）", "g"), ("show()：印出棋盤", "s"),
                                ("wins()：判斷有冇人贏", "w"), ("main：輪流落子", "m")])),
    Scene("grid",
          "[[using]]using Grid 等於二維 vector：俾呢個好長嘅型別，改個短啲嘅名，之後寫 Grid 就得。[[show]]show 用 4.4 學過嘅巢狀迴圈印棋盤，"
          "參數用 const reference，唔使複製。",
          s.scene(Open("ttt.cpp", mode="instant"), Type("ttt.cpp", USING, before="int main", at="using", rate=34),
                  Type("ttt.cpp", SHOW, before="int main", at="show", rate=48))),
    Scene("wins",
          "[[same]]same 檢查三格係咪都係同一個玩家，用且將三個條件連埋。[[loop]]wins 用迴圈，每一次檢查一行同一列，"
          "i 由零行到二，三行三列就檢查晒；[[diag]]最後再檢查兩條斜線。一共八條線，任何一條連埋，就係贏。",
          s.scene(Type("ttt.cpp", SAME, before="int main", at="same", rate=44), Type("ttt.cpp", WINS, before="int main", at="loop", rate=60))),
    Scene("main1",
          "[[init]]main 開一個三乘三嘅棋盤，全部係點，X 先行。[[loop]]最多行九步：[[read]]讀入行同列；"
          "[[range]]超出範圍，就印句提示，用 continue 返去再問，呢一步唔計。呢個檢查好重要，唔係就會寫出界。",
          s.scene(Type("ttt.cpp", P1, before="}", last=True, at="init", rate=40), Type("ttt.cpp", P2, before="}", last=True, at="loop", rate=48),
                  Type("ttt.cpp", P3, before="}", last=True, at="range", rate=48))),
    Scene("main2",
          "[[place]]落子，步數加一，再印出棋盤；[[win]]贏咗就宣佈，用 return 結束程式；[[swap]]未贏，就用 2.5 學嘅條件運算子換人。"
          "[[draw]]九步都冇人贏，就係和局。",
          s.scene(Type("ttt.cpp", "".join(P4.splitlines(True)[:3]), before="}", last=True, at="place", rate=40),
                  Type("ttt.cpp", "".join(P4.splitlines(True)[3:7]), before="}", last=True, at="win", rate=48),
                  Type("ttt.cpp", P4.splitlines(True)[7], before="}", last=True, at="swap", rate=40),
                  Type("ttt.cpp", "".join(P4.splitlines(True)[8:]), before="}", last=True, at="draw", rate=40), Expect("ttt.cpp", BUG))),
    Scene("bug",
          "[[cc]]編譯，試玩吓。[[x]]X 落中間；[[o]]O 都揀中間……[[oops]]O 竟然搶咗 X 個位！程式完全冇檢查嗰格有冇人。[[stop]]撳 Ctrl+C 停咗佢先。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("x", "o", "stop")), Note("O 搶咗 X 嘅位！", at="oops", where="editor"))),
    Scene("fix",
          "[[fix]]落子之前，要檢查嗰格係咪仲係點；唔係嘅話，就話 Taken，再問一次。",
          s.scene(Note(None), Type("ttt.cpp", TAKEN, after=P3, at="fix", rate=40), Expect("ttt.cpp", FINAL))),
    Scene("game",
          "[[cc]]再嚟一局。[[m1]]X 落中間；[[m2]]O 想搶中間：Taken；[[m3]]O 改落左上角；[[m4]]X 打錯咗三三，超出範圍；"
          "[[m5]]X 落右上角；[[m6]]O 落右下角；[[m7]]X 落左下角：斜線三個 X，X 贏！程式即刻結束。全部規則都運作正常。",
          s.scene(Run(clr, at="cc"), Run(c2, recall=True), Run(r2, keys=("m1", "m2", "m3", "m4", "m5", "m6", "m7"), type_rate=10))),
    Scene("parts",
          "睇返成個程式：[[a]]show 負責印，[[b]]same 同 wins 負責判斷，[[c]]main 負責流程。[[why]]每個函數都短，就算成個程式有六十行，都唔難明。",
          TileCard("每個函數做一件事", [
              Tile("🖨️", "show", "印出棋盤", "a", BLUE), Tile("🏆", "same / wins", "判斷有冇人贏", "b", GREEN),
              Tile("🔁", "main", "輪流、檢查、落子", "c", PURPLE),
          ], height=330, footer=("函數短，成個程式就易明", "why"))),
    Scene("recap",
          "第四章完成！我哋學咗：[[r1]]vector 同 range-based for；[[r2]]vector 嘅常用操作，同 at 檢查出界；[[r3]]二維 vector、C 陣列同 std::array；"
          "[[r4]]字串操作、UTF-8，仲自己寫咗搜尋同排序。",
          BulletCard("第四章重點", [("vector、range-based for", "r1"), ("insert、erase、at()", "r2"),
                                  ("二維 vector、std::array", "r3"), ("字串、UTF-8、搜尋同排序", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]玩完一局之後可以再玩，同埋記住 X 同 O 各贏咗幾多局。[[next]]下一章，我哋學指標同記憶體。多謝收睇，下次見！",
          EndCard("改成玩完一局可以再玩，並記住 X 同 O 各贏咗幾多局。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 26 (syllabus 2.8): do-while、break、continue

Asking for a mark until it is 0-100 with do-while (a missing semicolon is a real error); "abc"
really slips through as 0, so the read itself becomes the check (clear, ignore), as promised
in 1.4; summing positive numbers with while (true), break and continue.
Run `python3 video2.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 26
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-08"
VALID = (CODE / "valid.cpp").read_text()
SUM = (CODE / "sum.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CHECK = ("        if (!(std::cin >> mark)) {\n            std::cin.clear();\n"
         "            std::cin.ignore(1000, '\\n');\n            mark = -1;\n        }\n")
V1 = VALID.replace(CHECK, "        std::cin >> mark;\n")
NOSEMI = V1.replace("mark > 100);", "mark > 100)")
CV = "g++ -std=c++20 -Wall -Wextra valid.cpp -o valid"
CS = "g++ -std=c++20 -Wall -Wextra sum.cpp -o sum"

(c1, r1, c2, c3, r3, clr, c4, r4, clr2, c5, r5, cch, rch) = cpp.session({"valid.cpp": V1, "sum.cpp": SUM}, [
    CV, Input("./valid", ["150", "-5", "80"]),
    Write("valid.cpp", NOSEMI), CV,
    Write("valid.cpp", V1), CV, Input("./valid", ["abc"]),
    Write("valid.cpp", VALID), "clear", CV, Input("./valid", ["abc", "150", "80"]),
    "clear", CS, Input("./sum", ["5", "-3", "10", "0"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["3", "9", "7"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.count("Mark (0-100): ") == 3 and r1.output.endswith("OK: 80\n")
assert "expected ';'" in cpp.visible(c2.output) and c2.code != 0, c2.output
assert r3.output.endswith("abc\nOK: 0\n"), r3.output
assert r4.output.count("Mark (0-100): ") == 3 and r4.output.endswith("OK: 80\n"), r4.output
assert r5.output.endswith("Total: 15\n") and rch.output.endswith("Correct!\n")
assert c1.code == c3.code == c4.code == c5.code == cch.code == 0

SAY = {"do-while": "do while", "do": "do", "break": "break", "continue": "continue", "while (true)": "while true",
       "std::cin >> mark": "S T D see in 兩個大過號 mark", "clear": "clear", "ignore": "ignore", "abc": "A B C"}

s = Stage({"valid.cpp": V1, "sum.cpp": SUM}, title="do-while、break、continue", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！今集學三樣同迴圈有關嘅嘢：do-while、break 同 continue。仲會講返 1.4 留低嘅問題：點樣檢查輸入啱唔啱。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "do-while · 檢查輸入 · break · continue")),
    Scene("goal",
          "今集會講：[[b1]]do-while：至少行一次；[[b2]]檢查使用者嘅輸入；[[b3]]break：提早離開迴圈；[[b4]]continue：跳過今次。",
          BulletCard("今集學識", [("do-while：至少行一次", "b1"), ("檢查輸入", "b2"), ("break：提早離開", "b3"),
                                ("continue：跳過今次", "b4")])),
    Scene("dowhile",
          "[[open]]呢個程式要使用者輸入零至一百嘅分數。[[do]]do 後面嘅大括號，會先行一次；[[while]]行完先檢查 while 嘅條件："
          "分數唔喺範圍內，就返去再問。[[semi]]留意 do-while 最尾，要有一個分號。",
          s.scene(Open("valid.cpp", at="open"), Mark((5, 8), at="do"), Mark(8, at="while"), Mark(8, at="semi"))),
    Scene("run1",
          "[[cc]]編譯運行。[[t1]]輸入一百五十，[[o1]]太大，再問一次；[[t2]]輸入負五，[[o2]]太細，又再問；[[t3]]輸入八十，[[o3]]終於 OK。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("t1", "t2", "t3")))),
    Scene("semi",
          "[[del]]如果唔記得最尾嗰個分號，[[cc]]編譯就會出錯，[[err]]話 while 後面應該要有分號。[[fix]]加返就得。",
          s.scene(Replace("valid.cpp", "mark > 100);", "mark > 100)", at="del"), Expect("valid.cpp", NOSEMI),
                  Run(c2, at="cc", recall=True), Type("valid.cpp", ";", after="mark > 100)", at="fix"), Expect("valid.cpp", V1))),
    Scene("compare",
          "while 同 do-while 嘅分別：[[w]]while 先檢查條件，一開始唔成立，就一次都唔行；"
          "[[d]]do-while 先行一次，之後先檢查，所以至少行一次。[[use]]好似問問題、問到答啱為止，就最啱用 do-while。",
          TileCard("while 定 do-while？", [
              Tile("🔍", "while", "先檢查，後行\n可能一次都唔行", "w", BLUE),
              Tile("🔁", "do-while", "先行，後檢查\n至少行一次", "d", PURPLE),
          ], cols=2, height=330, footer=("問到答啱為止：do-while", "use"))),
    Scene("abc",
          "不過仲有個漏洞。[[cc]]再運行，[[t]]今次輸入 abc。[[o]]佢話 OK: 0！記得 1.4 講過：cin 讀唔到數字就會失敗，"
          "mark 變咗零，啱啱喺範圍入面，就咁過咗關。",
          s.scene(Run(c3, at="cc", recall=True), Run(r3, recall=True, keys=("t",)),
                  Note("abc 都過關？\n讀唔到數字：mark 變 0", at="o", where="editor"))),
    Scene("check",
          "[[if]]std::cin >> mark 本身就可以用嚟做條件：讀到數字就係 true，讀唔到就係 false。"
          "[[clear]]失敗嘅話，先用 clear 清除 cin 嘅錯誤狀態，[[ignore]]再用 ignore 掉走打錯嗰行，[[neg]]最後將 mark 設做負一，等迴圈再問。",
          s.scene(Note(None), Replace("valid.cpp", "        std::cin >> mark;\n", CHECK.splitlines(True)[0] + "        }\n", at="if"),
                  Type("valid.cpp", CHECK.splitlines(True)[1], before="        }\n    } while", at="clear"),
                  Type("valid.cpp", CHECK.splitlines(True)[2], before="        }\n    } while", at="ignore"),
                  Type("valid.cpp", CHECK.splitlines(True)[3], before="        }\n    } while", at="neg"), Expect("valid.cpp", VALID))),
    Scene("run2",
          "[[cc]]編譯運行。[[t1]]輸入 abc，[[o1]]今次佢會再問；[[t2]]輸入一百五十，[[o2]]太大，再問；[[t3]]輸入八十，[[o3]]先至 OK。",
          s.scene(Run(clr, at="cc"), Run(c4, recall=True), Run(r4, recall=True, keys=("t1", "t2", "t3")))),
    Scene("brk",
          "跟住講 break 同 continue。[[open]]呢個程式加埋所有正數，輸入零就停。[[true]]while (true) 本身係死循環，"
          "[[brk]]靠 break 離開：輸入零，就即刻跳出迴圈；[[cont]]continue 就係跳過今次：負數唔加，直接返去讀下一個。",
          s.scene(Run(clr2), Open("sum.cpp", at="open"), Mark(5, at="true"), Mark((9, 11), at="brk"), Mark((12, 14), at="cont"))),
    Scene("run3",
          "[[cc]]編譯運行。[[t1]]五，[[t2]]負三，[[t3]]十，[[t4]]最後零。[[out]]總數係十五：負三被 continue 跳過咗，零就 break 咗出嚟。",
          s.scene(Mark(None), Run(c5, at="cc"), Run(r5, keys=("t1", "t2", "t3", "t4")))),
    Scene("recap",
          "總結：[[r1]]do-while 先行後檢查，至少行一次，最尾要有分號；[[r2]]用 std::cin >> x 做條件，檢查有冇讀到數字，"
          "失敗就 clear 同 ignore；[[r3]]break 即刻離開迴圈；[[r4]]continue 跳過今次，繼續下一次。",
          BulletCard("今集重點", [("do-while：至少行一次（尾有 ;）", "r1"), ("if (!(std::cin >> x))：clear + ignore", "r2"),
                                ("break：即刻離開迴圈", "r3"), ("continue：跳過今次", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 do-while 寫一個估數字遊戲：答案係七，不停叫使用者估，直到估中為止。"
          "[[next]]下一集，我哋學迴圈入面再有迴圈。多謝收睇，下次見！",
          EndCard("用 do-while 寫一個估數字：答案係 7，不停叫使用者估，直到估中為止，印出 Correct!",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

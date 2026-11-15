#!/usr/bin/env python3
"""Video 41 (syllabus 3.12): 小項目：計數機

Part 3's project: calculate(a, op, b) with a switch, a loop that reads "3 + 4" until q. The
first version really prints "= inf" for 8 / 0 and "= 0" for 5 x 3; validOp() (grouped cases)
and an else-if chain fix both. Run `python3 video3.12.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 41
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-12"
FINAL = (CODE / "calc.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CALC = ("double calculate(double a, char op, double b) {\n    switch (op) {\n    case '+': return a + b;\n"
        "    case '-': return a - b;\n    case '*': return a * b;\n    case '/': return a / b;\n    }\n    return 0;\n}\n\n")
VALID = ("bool validOp(char op) {\n    switch (op) {\n    case '+': case '-': case '*': case '/':\n        return true;\n"
         "    default:\n        return false;\n    }\n}\n\n")
PRINT = "        std::cout << \"= \" << calculate(a, op, b) << '\\n';\n"
MAINBODY = ("    double a{};\n    double b{};\n    char op{};\n    std::cout << \"a op b (q to quit)\\n\";\n"
            "    while (std::cin >> a >> op >> b) {\n" + PRINT + "    }\n")
CHAIN = ("        if (!validOp(op)) {\n            std::cout << \"Unknown operator\\n\";\n"
         "        } else if (op == '/' && b == 0) {\n            std::cout << \"Cannot divide by 0\\n\";\n"
         "        } else {\n    " + PRINT + "        }\n")
SKEL = "#include <iostream>\n\nint main() {\n}\n"
V1 = "#include <iostream>\n\n" + CALC + "int main() {\n" + MAINBODY + "}\n"
assert "#include <iostream>\n\n" + VALID + CALC + "int main() {\n" + MAINBODY.replace(PRINT, CHAIN) + "}\n" == FINAL
CC = "g++ -std=c++20 -Wall -Wextra calc.cpp -o calc"
TRY = ["3 + 4", "10 / 4", "6 * 7", "8 / 0", "5 x 3", "q"]

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"calc.cpp": V1}, [
    CC, Input("./calc", TRY), Write("calc.cpp", FINAL), "clear", CC, Input("./calc", TRY),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["7 % 3", "2 ^ 10", "q"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split("\n")[1:12] == ["3 + 4", "= 7", "10 / 4", "= 2.5", "6 * 7", "= 42", "8 / 0", "= inf", "5 x 3", "= 0", "q"], r1.output
assert "Cannot divide by 0" in r2.output and "Unknown operator" in r2.output and "= inf" not in r2.output
assert c1.code == c2.code == cch.code == 0 and "= 1" in rch.output and "= 1024" in rch.output

SAY = {"calculate": "calculate", "validOp": "valid op", "inf": "inf", "q": "Q", "switch": "switch", "else if": "else if",
       "Unknown operator": "Unknown operator"}

s = Stage({"calc.cpp": SKEL}, title="小項目：計數機", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第三章嘅小項目：計數機。輸入好似三加四咁嘅算式，佢就計出答案，一直計到你輸入 q 為止。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "函數 · switch · 迴圈")),
    Scene("plan",
          "步驟係：[[read]]讀入一個數、一個運算符號、再一個數；[[check]]檢查啱唔啱；[[calc]]計數；[[out]]印出答案；[[loop]]再讀下一條，直到輸入 q。",
          FlowCard("計數機：步驟", [Row("每一條", "算式", BLUE, [
              Node("讀入", "a op b", "read"), Node("檢查", "符號、除零", "check"),
              Node("計", "calculate", "calc"), Node("印出", "= 答案", "out"),
          ], note="重複，直到輸入 q", note_at="loop")])),
    Scene("calc_fn",
          "[[sig]]calculate 收三個參數：兩個數，同一個運算符號。[[sw]]入面用 switch 揀做邊種運算，[[ret]]每個 case 直接 return 結果；"
          "return 咗就即刻離開函數，所以唔使寫 break。",
          s.scene(Open("calc.cpp", mode="instant"), Type("calc.cpp", CALC.splitlines(True)[0], before="int main", at="sig", rate=24),
                  Type("calc.cpp", "".join(CALC.splitlines(True)[1:]), after="double b) {\n", at="sw", rate=30))),
    Scene("main_loop",
          "[[vars]]main 入面準備兩個數同一個字元。[[loop]]while 嘅條件就係讀入：讀到三樣嘢就繼續；讀唔到，例如打 q，就離開，2.8 學過。"
          "[[print]]每一條都印出答案。",
          s.scene(Type("calc.cpp", "".join(MAINBODY.splitlines(True)[:4]), before="}", last=True, at="vars", rate=30),
                  Type("calc.cpp", "".join(MAINBODY.splitlines(True)[4:]), before="}", last=True, at="loop", rate=30),
                  Expect("calc.cpp", V1), Mark(V1[:V1.index(PRINT)].count("\n") + 1, at="print"))),
    Scene("run1",
          "[[cc]]編譯運行。第一條，[[t1]]三加四，得七；[[t2]]十除四，二點五；[[t3]]六乘七，四十二，全部都啱。"
          "但係，[[t4]]八除零，出咗個 inf？[[t5]]五 x 三，答案係零？[[t6]]最後打 q，離開程式。頭三條冇問題，後面兩條就要處理。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("t1", "t2", "t3", "t4", "t5", "t6"), type_rate=12))),
    Scene("bugs",
          "有兩個問題：[[inf]]除以零，double 會得出 inf，即係無限大，唔係我哋想要嘅答案；"
          "[[zero]]打錯符號，calculate 冇對應嘅 case，就回傳咗零，仲扮係答案咁。",
          s.scene(Note("8 / 0 → inf（無限大）", at="inf", where="editor"), Note("5 x 3 → 0？\n冇呢個符號都照計", at="zero", where="editor"))),
    Scene("valid",
          "[[type]]加一個 validOp 函數，檢查運算符號。[[group]]四個 case 疊埋一齊，2.4 講過：佢哋全部都行同一段，回傳 true；"
          "[[def]]其他符號，就回傳 false。",
          s.scene(Note(None), Type("calc.cpp", VALID, before="double calculate", at="type", rate=30), Mark(5, at="group"), Mark((7, 8), at="def"))),
    Scene("chain",
          "[[chain]]main 入面改用 else if：符號唔識，就話 Unknown operator；[[div]]除以零，就話唔可以；[[ok]]其他情況，先至計數。三種情況，一次只會行其中一種。",
          s.scene(Mark(None), Replace("calc.cpp", PRINT, CHAIN, at="chain", rate=32), Expect("calc.cpp", FINAL))),
    Scene("run2",
          "[[cc]]再編譯，輸入同樣嘅算式。[[o]]三條正常嘅照計；八除零，今次話唔可以除以零；五 x 三，話唔識呢個符號；"
          "最後打 q 離開。全部情況都處理好晒。呢個就係 else if 嘅用處。",
          s.scene(Run(clr, at="cc"), Run(c2, recall=True), Run(r2, recall=True, type_rate=12))),
    Scene("parts",
          "睇返成個程式，每個函數做一件事：[[v]]validOp 檢查；[[c]]calculate 計數；[[m]]main 負責讀入、決定同輸出。"
          "[[why]]咁樣分工，每部分都短，易明，亦易改。",
          TileCard("每個函數做一件事", [
              Tile("✅", "validOp", "檢查運算符號", "v", GREEN),
              Tile("🧮", "calculate", "計數", "c", BLUE),
              Tile("🔁", "main", "讀入、決定、輸出", "m", PURPLE),
          ], height=330, footer=("分工：短、易明、易改", "why"))),
    Scene("recap",
          "第三章完成！我哋學咗：[[r1]]定義同呼叫函數，參數同 return；[[r2]]傳值、reference 同 const reference；"
          "[[r3]]宣告、多個檔案同 namespace；[[r4]]仲有遞迴。",
          BulletCard("第三章重點", [("函數：參數、return", "r1"), ("傳值、int&、const&", "r2"),
                                  ("宣告、.h / .cpp、namespace", "r3"), ("遞迴", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]為計數機加兩個運算：百分號計餘數，同埋 ^ 計次方。提示：cmath 入面有 fmod 同 pow。"
          "[[next]]下一章，我哋學 vector 同字串。多謝收睇，下次見！",
          EndCard("為計數機加兩個運算：% 計餘數，^ 計次方。提示：<cmath> 有 std::fmod 同 std::pow。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

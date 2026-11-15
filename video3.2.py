#!/usr/bin/env python3
"""Video 31 (syllabus 3.2): 參數同回傳值

square(x) with a parameter and return; using the result directly or in a variable; max3(a, b, c)
typed without its return: g++'s -Wreturn-type warning, and the program really crashes (GCC traps
at the missing return); adding `return best;` gives 42. Run `python3 video3.2.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 31
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-02"
FINAL = (CODE / "func.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SKEL = "#include <iostream>\n\nint main() {\n}\n"
SQUARE = "int square(int x) {\n    return x * x;\n}\n\n"
MAX3 = ("int max3(int a, int b, int c) {\n    int best = a;\n    if (b > best) {\n        best = b;\n    }\n"
        "    if (c > best) {\n        best = c;\n    }\n    return best;\n}\n\n")
MAIN1 = "    std::cout << square(5) << '\\n';\n    int area = square(12);\n    std::cout << area << '\\n';\n"
MAIN2 = "    std::cout << max3(7, 42, 19) << '\\n';\n"
RET = "    return best;\n"
V1 = "#include <iostream>\n\n" + SQUARE + "int main() {\n" + MAIN1 + "}\n"
NORET = "#include <iostream>\n\n" + SQUARE + MAX3.replace(RET, "") + "int main() {\n" + MAIN1 + MAIN2 + "}\n"
assert NORET.replace("        best = c;\n    }\n}", "        best = c;\n    }\n" + RET + "}") == FINAL
CC = "g++ -std=c++20 -Wall -Wextra func.cpp -o func"

(c1, r1, c2, r2, c3, r3, cch, rch) = cpp.session({"func.cpp": V1}, [
    CC, "./func", Write("func.cpp", NORET), CC, "./func", Write("func.cpp", FINAL), CC, "./func",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["25", "144"] and r3.output.split() == ["25", "144", "42"]
assert "no return statement in function returning non-void" in cpp.visible(c2.output)
assert r2.code != 0 and r2.output.split("\n")[:2] == ["25", "144"] and "42" not in r2.output, r2.output
crash = r2.output.strip().split("\n")[-1]
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.split() == ["27", "1", "0"]

SAY = {"square(5)": "square 五", "square(12)": "square 十二", "max3": "max 三", "max3(7, 42, 19)": "max 三，七、四十二、十九",
       "return": "return", "return best": "return best", "int x": "int x"}

s = Stage({"func.cpp": SKEL}, title="參數同回傳值", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅 printLine，每次都做一模一樣嘅嘢。今集學參數同回傳值：將資料傳入函數，再攞返個結果出嚟。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "parameter · return")),
    Scene("goal",
          "今集會講：[[b1]]參數：傳入函數嘅資料；[[b2]]return：交返出嚟嘅結果；[[b3]]點樣用個結果；[[b4]]唔記得 return 會點。",
          BulletCard("今集學識", [("參數 parameter", "b1"), ("回傳值 return", "b2"), ("用返個結果", "b3"),
                                ("唔記得 return 會點", "b4")])),
    Scene("square",
          "寫一個計平方嘅函數。[[sig]]名前面嘅 int，係回傳型別：佢會交返一個整數出嚟；[[param]]括號入面嘅 int x 係參數，"
          "即係呼叫嗰陣傳入嚟嘅值；[[ret]]return x 乘 x，就係將結果交返出去。",
          s.scene(Open("func.cpp", mode="instant"), Type("func.cpp", SQUARE.splitlines(True)[0], after="#include <iostream>\n\n", at="sig"),
                  Type("func.cpp", "".join(SQUARE.splitlines(True)[1:]), after="int square(int x) {\n", at="ret"))),
    Scene("anatomy",
          "[[rt]]回傳型別寫喺最前面；[[name]]跟住係函數名；[[par]]括號入面係參數，有型別亦有名；[[body]]大括號入面用 return 交返結果。",
          AnatomyCard("有參數、有回傳值", [
              Part("int", "回傳型別", PURPLE, "rt"),
              Part(" square", "函數名", BLUE, "name"),
              Part("(int x)", "參數", AMBER, "par"),
              Part(" { return x * x; }", "交返結果", GREEN, "body"),
          ], size=70)),
    Scene("call",
          "[[c1]]喺 main 入面，square(5)：五會傳入 x，計出二十五，直接印出嚟。[[c2]]結果亦可以放入變數：area 等於 square(12)。"
          "[[cc]]編譯運行，[[o]]二十五同一百四十四。",
          s.scene(Type("func.cpp", MAIN1.splitlines(True)[0], before="}", last=True, at="c1", rate=20),
                  Type("func.cpp", "".join(MAIN1.splitlines(True)[1:]), before="}", last=True, at="c2", rate=24),
                  Expect("func.cpp", V1), Run(c1, at="cc"), Run(r1))),
    Scene("flow",
          "[[call]]呼叫 square(5) 嘅時候，[[copy]]五會放入參數 x；[[ret]]函數計出二十五，用 return 交返出嚟；"
          "[[sub]]結果就好似代替咗 square(5) 呢個位，所以印出二十五。",
          FlowCard("square(5) 點樣變成 25？", [Row("呼叫", "交返", GREEN, [
              Node("square(5)", "呼叫", "call"), Node("x = 5", "五傳入 x", "copy"),
              Node("return 25", "交返結果", "ret"), Node("25", "代替咗呼叫", "sub"),
          ])])),
    Scene("max3",
          "函數可以有幾個參數，用逗號隔開。[[sig]]max3 揀出三個數入面最大嗰個：[[best]]先當 a 最大，[[cmp]]再同 b 同 c 比較，"
          "大啲就換。[[call]]喺 main 試吓 max3(7, 42, 19)。",
          s.scene(Type("func.cpp", MAX3.splitlines(True)[0], before="int main", at="sig", rate=22),
                  Type("func.cpp", MAX3.splitlines(True)[1], after="int max3(int a, int b, int c) {\n", at="best", rate=24),
                  Type("func.cpp", "".join(MAX3.splitlines(True)[2:8]) + "}\n\n", after="    int best = a;\n", at="cmp", rate=36),
                  Type("func.cpp", MAIN2, before="}", last=True, at="call", rate=24), Expect("func.cpp", NORET))),
    Scene("noret",
          "[[cc]]編譯，[[warn]]g++ 警告：一個要回傳 int 嘅函數，冇 return。[[run]]照運行，[[o]]頭兩行冇問題，但係去到 max3，程式當咗！",
          s.scene(Run(c2, at="cc", recall=True), Run(r2, at="run"), Note(f"{crash}：\n程式當咗！", at="o", where="editor"))),
    Scene("fix",
          "我哋計好咗 best，但係冇交返出去。[[ub]]冇 return 係未定義行為，今次 g++ 令程式即刻停低。[[fix]]加返 return best。"
          "[[cc]]再編譯運行，[[o]]四十二，啱晒。",
          s.scene(Note(None), Type("func.cpp", RET, after="        best = c;\n    }\n", at="fix"), Expect("func.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("rules",
          "記住幾條規則：[[r1]]回傳型別寫喺函數名前面；[[r2]]void 函數唔使 return；[[r3]]其他函數，每條路都一定要 return；"
          "[[r4]]一行到 return，函數就即刻結束。",
          BulletCard("回傳值嘅規則", [("回傳型別寫喺名前面", "r1"), ("void：唔使 return", "r2"),
                                    ("非 void：每條路都要 return", "r3"), ("return 之後即刻結束", "r4")])),
    Scene("recap",
          "總結：[[r1]]參數將資料傳入函數；[[r2]]return 將結果交返出嚟；[[r3]]結果可以直接用，或者放入變數；[[r4]]開住 -Wall，唔記得 return 會有警告。",
          BulletCard("今集重點", [("參數：傳入嘅資料", "r1"), ("return：交返嘅結果", "r2"), ("結果可以直接用或者存起", "r3"),
                                ("-Wall 會提你唔記得 return", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫兩個函數：cube 回傳一個數嘅立方，isEven 回傳 bool，話你知係咪雙數。"
          "[[next]]下一集，我哋講函數嘅宣告同定義。多謝收睇，下次見！",
          EndCard("寫兩個函數：cube(x) 回傳 x 嘅立方；isEven(n) 回傳 bool，話你知 n 係咪雙數。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

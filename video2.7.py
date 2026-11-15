#!/usr/bin/env python3
"""Video 25 (syllabus 2.7): for 迴圈

The while loop from 2.6's challenge next to the same for loop; the three parts and their order;
sum of 1 to n typed with `i < n`, which really stops at 9 and gives 45 (off-by-one); `<=` fixes
it; four loop forms with their real output. Run `python3 video25.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 25
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-07"
FINAL = (CODE / "sum.cpp").read_text()
FORMS = (CODE / "forms.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
WHILE = (ROOT / "code" / "02-06" / "challenge.cpp").read_text()     # 2.6's challenge answer
BUG = FINAL.replace("i <= n", "i < n")
BODY = ("    int total{0};\n    for (int i = 1; i < n; i++) {\n        std::cout << i << ' ';\n        total += i;\n    }\n"
        "    std::cout << \"\\nSum: \" << total << '\\n';\n")
SKEL = BUG.replace(BODY, "")
assert SKEL.replace("}\n", BODY + "}\n") == BUG
CC = "g++ -std=c++20 -Wall -Wextra sum.cpp -o sum"

(c1, r1, c2, r2, r3, cf, rf, cch, rch) = cpp.session({"sum.cpp": BUG, "forms.cpp": FORMS}, [
    CC, Input("./sum", ["10"]),
    Write("sum.cpp", FINAL), CC, Input("./sum", ["10"]), Input("./sum", ["100"]),
    "g++ -std=c++20 forms.cpp -o forms", "./forms",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("1 2 3 4 5 6 7 8 9 \nSum: 45\n"), r1.output
assert r2.output.endswith("9 10 \nSum: 55\n") and r3.output.endswith("Sum: 5050\n")
forms = [l.strip() for l in rf.output.strip().split("\n")]
assert forms == ["0 1 2 3 4", "1 2 3 4 5", "5 4 3 2 1", "0 2 4 6 8"], forms
assert c1.code == c2.code == cf.code == cch.code == 0 and rch.output.split()[-1] == "99"

SAY = {"for": "for", "i++": "i plus plus", "i--": "i minus minus", "off-by-one": "off by one", "i <= n": "i 細過或等於 n",
       "i < n": "i 細過 n"}

s = Stage({"sum.cpp": SKEL}, title="for 迴圈")

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅小挑戰，用 while 由一加到一百，要喺三個唔同地方寫：開始值、條件，同埋加一。"
          "今集學 for 迴圈，將三樣嘢放埋喺同一行。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "初始化 ; 條件 ; 更新")),
    Scene("goal",
          "今集會講：[[b1]]for 迴圈嘅三個部分；[[b2]]佢哋執行嘅次序；[[b3]]迴圈最常見嘅錯誤：差一。",
          BulletCard("今集學識", [("for 嘅三個部分", "b1"), ("執行次序", "b2"), ("差一錯誤 off-by-one", "b3")])),
    Scene("compare",
          "[[w]]左邊係 while：i 喺迴圈前面開始，條件喺 while 度，i++ 喺迴圈最尾。"
          "[[f]]右邊係 for：三樣嘢擺埋喺第一行，一眼就睇晒，亦唔會唔記得加一。",
          CodeCompareCard("while 同 for", [
              Pane("while", WHILE.split("int main() {\n")[1].rsplit("    std::cout", 1)[0].replace("\n    ", "\n").strip(),
                   True, "w", "while.cpp"),
              Pane("for", "int total{0};\nfor (int i = 1; i <= 100; i++) {\n    total += i;\n}", True, "f", "for.cpp"),
          ], size=30)),
    Scene("anatomy",
          "for 括號入面有三個部分，用分號隔開：[[init]]第一個係初始化，迴圈開始前行一次；[[cond]]第二個係條件，每次行之前都檢查；"
          "[[upd]]第三個係更新，每次行完之後做。",
          AnatomyCard("for 嘅三個部分", [
              Part("for (", "", MUTED, "init"),
              Part("int i = 1", "初始化：行一次", BLUE, "init"),
              Part(";", "", MUTED, "cond"),
              Part(" i <= n", "條件：每次之前檢查", GREEN, "cond"),
              Part(";", "", MUTED, "upd"),
              Part(" i++", "更新：每次之後", AMBER, "upd"),
              Part(")", "", MUTED, "upd"),
          ], size=64)),
    Scene("order",
          "次序係咁：[[s1]]先初始化，[[s2]]然後檢查條件，[[s3]]成立就行大括號入面嘅嘢，[[s4]]跟住更新，再返去檢查條件。"
          "[[end]]條件唔成立，迴圈就完。",
          FlowCard("for 嘅執行次序", [Row("for", "迴圈", BLUE, [
              Node("① 初始化", "int i = 1", "s1"), Node("② 檢查條件", "i <= n？", "s2"),
              Node("③ 行一次", "{ … }", "s3"), Node("④ 更新", "i++", "s4"),
          ], note="④ 之後返去 ②；條件唔成立就離開", note_at="end")])),
    Scene("type",
          "[[open]]程式先讀入 n。[[t1]]總數由零開始。[[t2]]for 迴圈：i 由一開始，i 細過 n 就繼續，每次加一。"
          "[[t3]]入面印出 i，再加入總數。[[t4]]最後喺迴圈外面，印出總數。",
          s.scene(Open("sum.cpp", mode="instant", at="open"),
                  Type("sum.cpp", BODY.splitlines(True)[0], before="}", last=True, at="t1"),
                  Type("sum.cpp", BODY.splitlines(True)[1], before="}", last=True, at="t2", rate=18),
                  Type("sum.cpp", "".join(BODY.splitlines(True)[2:5]), before="}", last=True, at="t3", rate=20),
                  Type("sum.cpp", BODY.splitlines(True)[5], before="}", last=True, at="t4", rate=20), Expect("sum.cpp", BUG))),
    Scene("run1",
          "[[cc]]編譯運行，[[t]]輸入十。[[out]]總數係四十五？由一加到十，應該係五十五先啱。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("t",)), Note("1 加到 10 = 55？", at="out", where="editor"))),
    Scene("bug",
          "睇吓印出嚟嘅數字：[[look]]去到九就停咗，冇十。[[why]]因為條件係 i 細過 n：i 等於十嘅時候，條件唔成立，十就冇加到。"
          "[[name]]呢種差一個嘅錯誤，叫 off-by-one，係迴圈最常見嘅錯誤。[[fix]]改做細過或等於。",
          s.scene(Note(None), Mark(8, at="why"), Note("i < n：i 去到 9 就停\n10 冇加到", at="why", where="editor"),
                  Note(None, at="fix"), Replace("sum.cpp", "i < n", "i <= n", at="fix"), Expect("sum.cpp", FINAL))),
    Scene("run2",
          "[[cc]]再編譯運行。[[t1]]輸入十，[[o1]]今次一直印到十，總數五十五，啱晒。[[t2]]再試一百，[[o2]]五千零五十。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("t1",)),
                  Run(r3, at="t2", recall=True, keys=(("t2", 1.0),)))),
    Scene("forms",
          "for 有唔同寫法：[[a]]由零開始、細過五，就係零到四，一共五次，之後會成日見到；[[b]]由一到五，用細過或等於；"
          "[[c]]倒數就用 i--；[[d]]每次加二，就係雙數。",
          TableCard("唔同嘅 for", ["寫法", "i 嘅值"], [
              (["for (int i = 0; i < 5; i++)", forms[0]], "a"),
              (["for (int i = 1; i <= 5; i++)", forms[1]], "b"),
              (["for (int i = 5; i > 0; i--)", forms[2]], "c"),
              (["for (int i = 0; i < 10; i += 2)", forms[3]], "d"),
          ], widths=[1.7, 1], code_cols=(0, 1), size=40)),
    Scene("recap",
          "總結：[[r1]]for 括號入面有三部分：初始化、條件、更新；[[r2]]次序係初始化，然後檢查、行、更新，不停重複；"
          "[[r3]]小心差一錯誤：細過同細過或等於，差一次；[[r4]]知道要行幾多次，就用 for。",
          BulletCard("今集重點", [("for (初始化; 條件; 更新)", "r1"), ("次序：初始化 → 檢查 → 行 → 更新", "r2"),
                                ("小心 off-by-one：< 同 <=", "r3"), ("知道次數：用 for", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 for 印出一百以內，所有三嘅倍數。提示：更新部分唔一定係加一。"
          "[[next]]下一集，我哋學 do-while、break 同 continue。多謝收睇，下次見！",
          EndCard("用 for 印出 100 以內所有 3 嘅倍數。提示：更新部分唔一定係 i++。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

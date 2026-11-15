#!/usr/bin/env python3
"""Video 16 (syllabus 1.10): auto

1.8's average rewritten with auto; what auto deduces (checked by static_assert in a hidden
compile); the trap `auto total = 0;` that turns 19.5 + 9.8 into 28, for real; and the real
error for auto without an initialiser. Run `python3 video16.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 16
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-10"
AVG = (CODE / "avg.cpp").read_text()
BILL = (CODE / "bill.cpp").read_text()
TYPES = (CODE / "types.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
OLD = (ROOT / "code" / "01-08" / "avg.cpp").read_text()          # 1.8's program, before auto
assert OLD.replace("int a{80}", "auto a = 80").replace("int b{95}", "auto b = 95").replace("double avg", "auto avg") == AVG
BAD = BILL.replace("auto total = 0.0;", "auto total = 0;")
NOINIT = BILL.replace("    total += 19.5;\n", "    auto count;\n    total += 19.5;\n")
CA = "g++ -std=c++20 -Wall -Wextra avg.cpp -o avg"
CB = "g++ -std=c++20 -Wall -Wextra bill.cpp -o bill"

(ct, a1, ra1, clr, b1, rb1, b2, rb2, b3, cch, rch) = cpp.session({"avg.cpp": AVG, "bill.cpp": BAD, "types.cpp": TYPES}, [
    "g++ -std=c++20 -c types.cpp -o /dev/null",
    CA, "./avg", "clear",
    CB, "./bill", Write("bill.cpp", BILL), CB, "./bill",
    Write("bill.cpp", NOINIT), CB,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert ct.code == 0, "auto deduced a type the video does not claim:\n" + ct.output
assert ra1.output.strip() == "Average: 87.5" and rb1.output.strip() == "Total: 28" and rb2.output.strip() == "Total: 29.3"
assert "declaration of 'auto count' has no initializer" in cpp.visible(b3.output), b3.output
assert a1.code == b1.code == b2.code == cch.code == 0 and rch.output.strip() == "1.68 A 1"

SAY = {"auto": "auto", "static_cast": "static cast", "auto total = 0": "auto total 等如零"}

s = Stage({"avg.cpp": OLD, "bill.cpp": BAD}, title="auto：自動推斷型別")

scenes = [
    Scene("intro",
          "歡迎返嚟！每次宣告變數都要寫型別。C++ 有個關鍵字 auto，可以叫編譯器自己推斷型別。今集睇吓佢幾時好用，幾時會出事。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "auto · 型別推斷")),
    Scene("goal",
          "今集會講：[[b1]]auto 點樣推斷型別；[[b2]]auto 幾時好用；[[b3]]auto 會收埋型別嘅陷阱。",
          BulletCard("今集學識", [("auto 點樣推斷型別", "b1"), ("幾時好用", "b2"), ("收埋型別嘅陷阱", "b3")])),
    Scene("rewrite",
          "我哋用 auto 改寫 1.8 嘅平均分程式。[[a]]a 等如八十，八十係整數，所以 auto 推斷做 int；[[b]]b 都一樣。"
          "[[avg]]avg 右邊用 static_cast 轉咗做 double，所以 avg 係 double，型別唔使寫兩次。[[cc]]編譯運行，[[out]]一樣係八十七點五，而且個程式短咗。",
          s.scene(Open("avg.cpp", mode="instant"), Replace("avg.cpp", "int a{80}", "auto a = 80", at="a"),
                  Replace("avg.cpp", "int b{95}", "auto b = 95", at="b"),
                  Replace("avg.cpp", "double avg", "auto avg", at="avg"), Expect("avg.cpp", AVG),
                  Run(a1, at="cc"), Run(ra1))),
    Scene("deduce",
          "auto 睇右邊嘅值，決定型別：[[i]]整數，就係 int；[[d]]有小數點，就係 double；[[c]]單引號，就係 char；"
          "[[bo]]true 同 false，就係 bool。",
          TableCard("auto 推斷出乜型別？", ["寫法", "型別"], [
              (["auto a = 80;", "int"], "i"),
              (["auto x = 80.0;", "double"], "d"),
              (["auto c = 'A';", "char"], "c"),
              (["auto ok = true;", "bool"], "bo"),
          ], widths=[1.4, 1], code_cols=(0, 1), size=46)),
    Scene("trap1",
          "但係 auto 會收埋型別。[[open]]呢個程式由零開始，加埋兩個價錢：十九點五同九點八。[[cc]]編譯運行，"
          "[[out]]答案竟然係二十八？計數機都知道係二十九點三。",
          s.scene(Run(clr), Open("bill.cpp", at="open"), Run(b1, at="cc"), Run(rb1),
                  Note("19.5 + 9.8 = 28？", at="out", where="editor"))),
    Scene("trap_why",
          "因為 total 等如零，零係整數，[[int]]所以 total 係 int！[[cut]]加十九點五，小數切走，變十九；再加九點八，變二十八，"
          "連警告都冇。[[fix]]改做零點零，total 就係 double。[[cc]]運行，[[out]]二十九點三，啱晒。",
          s.scene(Note(None), Mark(4, at="int"), Note("0 係整數 → total 係 int", at="int", where="editor"),
                  Note(None, at="fix"), Mark(None, at="fix"), Replace("bill.cpp", "auto total = 0;", "auto total = 0.0;", at="fix"),
                  Expect("bill.cpp", BILL), Run(b2, at="cc", recall=True), Run(rb2))),
    Scene("noinit",
          "仲有一樣：[[type]]auto 一定要有初始值，[[cc]]冇值俾佢睇，編譯器就推斷唔到，[[err]]會出錯：auto count 冇初始值。"
          "[[undo]]刪走就得。",
          s.scene(Type("bill.cpp", "    auto count;\n", before="    total += 19.5;", at="type"), Expect("bill.cpp", NOINIT),
                  Run(b3, at="cc", recall=True), Replace("bill.cpp", "    auto count;\n", "", at="undo"), Expect("bill.cpp", BILL))),
    Scene("when",
          "所以：[[good]]右邊已經清楚寫明型別，或者型別名好長，就用 auto，之後學 STL 嘅時候會成日用到；"
          "[[bad]]右邊只係一個數字，或者 auto 會令人睇唔明，就寫返清楚型別。",
          TileCard("幾時用 auto？", [
              Tile("✅", "好用", "右邊已經寫明型別\n（例如 static_cast<double>）\n型別名好長（STL 會見到）", "good", GREEN),
              Tile("⚠️", "小心", "右邊只係一個數字：0 係 int\n睇唔清楚型別：寫返出嚟", "bad", AMBER),
          ], cols=2, height=400)),
    Scene("recap",
          "總結：[[r1]]auto 睇右邊嘅值推斷型別；[[r2]]型別已經好清楚、或者好長，就用 auto；[[r3]]小心數字：零係 int，零點零先係 double；"
          "[[r4]]auto 一定要有初始值。",
          BulletCard("今集重點", [("auto 睇右邊嘅值推斷型別", "r1"), ("型別清楚或者好長：用 auto", "r2"),
                                ("小心：0 係 int，0.0 先係 double", "r3"), ("auto 一定要有初始值", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 auto 宣告三個變數：身高一點六八、等級 A、合格 true，確保佢哋分別係 double、char 同 bool。"
          "[[next]]下一集，我哋開始用 std::string 處理文字。多謝收睇，下次見！",
          EndCard("用 auto 宣告三個變數：身高 1.68、等級 'A'、合格 true，確保佢哋分別係 double、char 同 bool。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 13 (syllabus 1.7): 浮點數同精度

0.1 + 0.2 prints 0.3 but is not == 0.3; setprecision(17) shows the tail; comparing with a
tolerance; a 茶餐廳 bill where setprecision(2) alone prints 38 and std::fixed gives 37.90.
Run `python3 video13.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 13
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-07"
SUM = (CODE / "sum.cpp").read_text()
BILL = (CODE / "bill.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
INC_IOM, INC_CMATH = "#include <iomanip>\n", "#include <cmath>\n"
L_PREC = "    std::cout << std::setprecision(17);\n    std::cout << sum << '\\n';\n"
L_DIFF = "    double diff = std::abs(sum - 0.3);\n    std::cout << (diff < 1e-9) << '\\n';\n"
S2 = SUM.replace(INC_CMATH, "").replace(L_DIFF, "")
S1 = S2.replace(INC_IOM, "").replace(L_PREC, "")
L_FIX, L_SP = "    std::cout << std::fixed;\n", "    std::cout << std::setprecision(2);\n"
L_P = "    std::cout << \"Total: $\" << total << '\\n';\n"
B2 = BILL.replace(L_FIX, "")
B1 = B2.replace(L_SP + L_P, "")
CS = "g++ -std=c++20 -Wall -Wextra sum.cpp -o sum"
CB = "g++ -std=c++20 -Wall -Wextra bill.cpp -o bill"

(c1, r1, c2, r2, c3, r3, clr, b1, rb1, b2, rb2, b3, rb3, cch, rch) = cpp.session({"sum.cpp": S1, "bill.cpp": B1}, [
    CS, "./sum", Write("sum.cpp", S2), CS, "./sum", Write("sum.cpp", SUM), CS, "./sum",
    "clear", CB, "./bill", Write("bill.cpp", B2), CB, "./bill", Write("bill.cpp", BILL), CB, "./bill",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["0.3", "0"] and r2.output.split() == ["0.3", "0", "0.30000000000000004"]
assert r3.output.split()[-1] == "1"
p_def, p_two, p_fix = rb1.output.split("$")[1].strip(), rb2.output.split("$")[2].strip(), rb3.output.split("$")[2].strip()
assert (p_def, p_two, p_fix) == ("37.9", "38", "37.90"), (p_def, p_two, p_fix)
assert all(r.code == 0 for r in (c1, c2, c3, b1, b2, b3, cch)) and rch.output.strip() == "Each: $33.33"

SAY = {"setprecision(17)": "set precision 十七", "setprecision(2)": "set precision 二", "setprecision": "set precision",
       "std::fixed": "S T D fixed", "fixed": "fixed", "iomanip": "I O manip", "cmath": "C math", "std::abs": "S T D abs"}

s = Stage({"sum.cpp": S1, "bill.cpp": B1}, title="浮點數同精度")

scenes = [
    Scene("intro",
          "歡迎返嚟！零點一加零點二，等於幾多？今集你會發現，電腦嘅答案，同你諗嘅唔一樣。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "double · fixed · setprecision")),
    Scene("goal",
          "今集會講：[[b1]]double 嘅精度問題；[[b2]]用 fixed 同 setprecision 控制小數位；[[b3]]點樣比較兩個小數。",
          BulletCard("今集學識", [("double 嘅精度問題", "b1"), ("fixed 同 setprecision", "b2"), ("點樣比較兩個小數", "b3")])),
    Scene("sum1",
          "[[open]]零點一加零點二，放入 sum。[[cc]]編譯運行，[[out1]]印出零點三，睇落冇問題。"
          "[[out2]]但係問佢 sum 係咪等於零點三，答案係零，即係 false！",
          s.scene(Open("sum.cpp", at="open"), Run(c1, at="cc"), Run(r1), Mark(6, at="out2"),
                  Note("== 係比較：一樣印 1，唔一樣印 0\n（2.1 會詳細講）", at="out2", where="editor"))),
    Scene("sum2",
          "睇清楚啲。[[inc]]加入 iomanip，[[type]]用 setprecision(17)，印出十七個位。[[cc]]運行，"
          "[[out]]原來 sum 唔係零點三，後面仲有一條好細嘅尾巴。",
          s.scene(Note(None), Mark(None), Type("sum.cpp", INC_IOM, after="#include <iostream>\n", at="inc"),
                  Type("sum.cpp", L_PREC, after="== 0.3) << '\\n';\n", at="type"), Expect("sum.cpp", S2),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("why",
          "點解會咁？[[dec]]用十進制，三分一寫唔盡，係零點三三三，冇完冇了。[[bin]]電腦用二進制，零點一喺二進制入面都寫唔盡，"
          "只可以存一個好接近嘅數。[[small]]所以小數計算，成日會有好細嘅誤差。",
          TileCard("點解唔係 0.3？", [
              Tile("🔟", "十進制", "1/3 = 0.3333…\n永遠寫唔盡", "dec", BLUE),
              Tile("💻", "二進制", "0.1 都寫唔盡\n只存到一個好接近嘅數", "bin", PURPLE),
          ], cols=2, height=330, footer=("double 計數：會有好細嘅誤差", "small"))),
    Scene("sum3",
          "所以比較兩個 double，唔好用兩個等號。[[inc]]加入 cmath，[[type]]計吓佢哋相差幾多，std::abs 係攞絕對值；"
          "[[cmp]]相差細過一個好細嘅數，例如十嘅負九次方，就當佢哋相等。[[cc]]運行，[[out]]今次係一，即係 true。",
          s.scene(Type("sum.cpp", INC_CMATH, after=INC_IOM, at="inc"), Type("sum.cpp", L_DIFF, before="}", last=True, at="type"),
                  Expect("sum.cpp", SUM), Mark(12, at="cmp"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("bill1",
          "再嚟一個實際例子：茶餐廳埋單。[[open]]奶茶十九蚊半，菠蘿包九蚊八，蛋撻八蚊六。[[cc]]編譯運行，"
          "[[out]]總數係三十七點九。不過銀碼，通常想見到兩個小數位。",
          s.scene(Mark(None), Run(clr), Open("bill.cpp", at="open"), Run(b1, at="cc"), Run(rb1))),
    Scene("bill2",
          "[[type]]試吓用 setprecision(2)，再印一次。[[cc]]編譯運行。[[out]]咦，變咗三十八？因為淨係用 setprecision，"
          "二係指成個數最多兩個有效數字，所以三十七點九變咗三十八。",
          s.scene(Type("bill.cpp", L_SP + L_P, before="}", last=True, at="type"), Expect("bill.cpp", B2),
                  Run(b2, at="cc", recall=True), Run(rb2), Note("淨係 setprecision(2)：\n兩個有效數字 → 38", at="out", where="editor"))),
    Scene("bill3",
          "[[type]]要喺前面加 std::fixed，意思係固定小數點，[[cc]]咁 setprecision 就會變成小數點後面兩個位。"
          "[[out]]三十七點九零，啱晒。",
          s.scene(Note(None), Type("bill.cpp", L_FIX, before=L_SP, at="type"), Expect("bill.cpp", BILL),
                  Run(b3, at="cc", recall=True), Run(rb3))),
    Scene("table",
          "比較一下：[[r1]]乜都唔加，最多印六個有效數字；[[r2]]淨係 setprecision(2)，係兩個有效數字；"
          "[[r3]]加埋 fixed，就係小數點後兩個位。[[tip]]另外，真正嘅收銀系統，通常用整數以仙做單位，避免誤差。",
          TableCard("37.9 點樣印？", ["寫法", "印出"], [
              (["（乜都唔加）", p_def], "r1"),
              (["setprecision(2)", p_two], "r2", RED),
              (["fixed + setprecision(2)", p_fix], "r3", GREEN),
          ], widths=[1.6, 1], code_cols=(0, 1), size=44, note=("收銀系統：用整數，以「仙」做單位", "tip"))),
    Scene("recap",
          "總結：[[r1]]double 有好細嘅誤差，零點一加零點二唔等於零點三；[[r2]]比較 double，要睇相差夠唔夠細；"
          "[[r3]]std::fixed 加 setprecision，控制小數位；[[r4]]佢哋都喺 iomanip 入面。",
          BulletCard("今集重點", [("double 有誤差：0.1 + 0.2 ≠ 0.3", "r1"), ("比較 double：睇相差夠唔夠細", "r2"),
                                ("fixed + setprecision(2)：兩個小數位", "r3"), ("要 #include <iomanip>", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]三個人夾錢食飯，總共一百蚊，每人要俾幾多？用兩個小數位印出嚟。"
          "[[next]]下一集，我哋講型別轉換。多謝收睇，下次見！",
          EndCard("三個人夾錢食飯，總共 100 蚊，每人要俾幾多？用兩個小數位印出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

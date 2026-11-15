#!/usr/bin/env python3
"""Video 86 (syllabus 7.6): Variadic templates

Two sum overloads (2 and 3 ints) really print 3 6. One variadic template with a fold
expression (args + ...) handles any count and mixed types: 3 10 / 6.5. sum() with no
arguments is a real "fold of empty expansion over operator+" error; (0 + ... + args) gives 0.
print() uses sizeof... and a comma fold: "4: Amy 72 A 3.5". Run `python3 video86.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 86
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-06"
FINAL = (CODE / "fold.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
PRINT = "template <typename... Ts>\nvoid print" + FINAL.split("void print")[1].split("int main")[0]
CALL = "    print(\"Amy\", 72, 'A', 3.5);\n"
V4 = FINAL.replace(PRINT, "").replace(CALL, "")
BAD = V4.replace("(0 + ... + args)", "(args + ...)")
V2 = BAD.replace(" << ' ' << sum() << '\\n';", " << '\\n';")
SUM = "template <typename... Ts>\nauto sum(Ts... args) {\n    return (args + ...);\n}\n"
OVER = "int sum(int a, int b) {\n    return a + b;\n}\n\nint sum(int a, int b, int c) {\n    return a + b + c;\n}\n"
MAIN2 = "int main" + V2.split("int main")[1]
MAIN1 = "int main() {\n    std::cout << sum(1, 2) << ' ' << sum(1, 2, 3) << '\\n';\n}\n"
V1 = V2.replace(SUM, OVER).replace(MAIN2, MAIN1)
CC = "g++ -std=c++20 -Wall -Wextra fold.cpp -o fold"

(c1, r1, clr, c2, r2, c3, clr2, c4, r4, clr3, c5, r5, cch, rch) = cpp.session({"fold.cpp": V1}, [
    CC, "./fold", "clear", Write("fold.cpp", V2), CC, "./fold", Write("fold.cpp", BAD), CC, "clear", Write("fold.cpp", V4), CC, "./fold",
    "clear", Write("fold.cpp", FINAL), CC, "./fold",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "3 6\n" and r2.output == "3 10\n6.5\n" and r4.output == "3 10\n6.5 0\n", (r1.output, r2.output, r4.output)
assert r5.output == "3 10\n6.5 0\n4: Amy 72 A 3.5 \n", r5.output
assert "fold of empty expansion over operator+" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == c5.code == cch.code == 0 and rch.output == "1 0\n"

SAY = {"typename...": "typename 三點", "Ts...": "Ts 三點", "Ts": "Ts", "args...": "args 三點", "args": "args",
       "(args + ...)": "args 加 三點", "(0 + ... + args)": "零 加 三點 加 args", "sizeof...": "sizeof 三點", "sum()": "sum 空括號",
       "sum": "sum", "print": "print", "fold": "fold", "variadic": "variadic", "allPositive": "all positive", "Amy": "Amy"}

s = Stage({"fold.cpp": V1}, title="Variadic templates", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！sum 想加兩個數，又想加三個、四個、十個，難道每個數量都寫一個函數？今集學 variadic templates：參數數量唔定嘅模板。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "typename... · fold expression")),
    Scene("goal",
          "今集會講：[[b1]]參數包，三點；[[b2]]fold expression，一次過加晒；[[b3]]冇參數嘅情況；[[b4]]sizeof 三點同逐個印出。",
          BulletCard("今集學識", [("參數包：typename... Ts", "b1"), ("fold：(args + ...)", "b2"), ("空嘅參數包", "b3"),
                                ("sizeof...、逐個印", "b4")])),
    Scene("over",
          "[[two]]一個 sum 加兩個數，[[three]]一個加三個數。[[cc]]編譯運行，[[o]]三同六。但係四個數呢？又要寫多一個。而且只係得 int。",
          s.scene(Open("fold.cpp", at="two"), Mark((3, 5), at="two"), Mark((7, 9), at="three"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("pack",
          "[[del]]刪走兩個，改寫一個模板：[[ts]]typename 三點 Ts，係一包類型；[[args]]Ts 三點 args，係一包參數，幾多個都得。"
          "[[fold]]args 加三點，用括號包住，叫 fold expression：將成包參數，用加號逐個連埋。",
          s.scene(Run(clr, at="del"), Replace("fold.cpp", OVER, SUM, at="del", rate=40), Mark(3, at="ts"), Mark(4, at="args"), Mark(5, at="fold"))),
    Scene("run2",
          "[[main]]main 試吓兩個數、四個數，同埋 double 同 int 混合。[[cc]]編譯運行，[[o]]三、十，同埋六點五。數量同類型都唔使理。",
          s.scene(Mark(None), Replace("fold.cpp", MAIN1.rstrip("\n"), MAIN2.rstrip("\n"), at="main", rate=50), Expect("fold.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("expand",
          "[[call]]sum 一、二、三，[[pack]]args 就係一、二、三；[[fold]]args 加三點，展開做一加二加三。",
          TableCard("fold 點樣展開？", ["寫法", "展開做"], [
              (["sum(1, 2, 3)", "args = 1, 2, 3"], "call"),
              (["(args + ...)", "1 + (2 + 3)"], "fold"),
              (["(0 + ... + args)", "((0 + 1) + 2) + 3"], ("fold", 1.5)),
          ], widths=[1.3, 1.5], code_cols=(0, 1), size=40)),
    Scene("empty",
          "[[type]]如果一個參數都冇呢？[[cc]]編譯：[[err]]錯誤：空嘅參數包，冇嘢可以加。",
          s.scene(Replace("fold.cpp", "sum(1.5, 2, 3) << '\\n';", "sum(1.5, 2, 3) << ' ' << sum() << '\\n';", at="type"), Expect("fold.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("init",
          "[[type]]解決方法：喺前面加一個初始值零：零加三點加 args。冇參數，答案就係零。[[cc]]編譯運行，[[o]]最後多咗個零。",
          s.scene(Run(clr2, at="type"), Replace("fold.cpp", "(args + ...)", "(0 + ... + args)", at="type"), Expect("fold.cpp", V4),
                  Mark(5, at="type"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("print",
          "[[type]]再寫一個 print：[[size]]sizeof 三點 args，係參數嘅數量；[[comma]]然後用逗號 fold：逐個參數印出，後面加空格。"
          "[[cc]]印一個名、一個數、一個字元、一個 double。運行：[[o]]四個參數，逐個印出嚟。",
          s.scene(Run(clr3, at="type"), Type("fold.cpp", PRINT, before="int main", at="type", rate=60), Mark(10, at="size"), Mark(11, at="comma"),
                  Type("fold.cpp", CALL, before="}", last=True, at="cc"), Expect("fold.cpp", FINAL), Mark(None, at="cc"),
                  Run(c5, recall=True), Run(r5, at="o"))),
    Scene("recap",
          "總結：[[r1]]typename 三點 Ts，收一包類型；[[r2]]args 加三點，fold expression 一次過處理晒；[[r3]]可能冇參數，就加一個初始值；"
          "[[r4]]sizeof 三點計數量，逗號 fold 逐個做嘢。",
          BulletCard("今集重點", [("template <typename... Ts>", "r1"), ("(args + ...)", "r2"), ("(0 + ... + args)：可以空", "r3"),
                                ("sizeof...、逗號 fold", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 allPositive，用 and and 嘅 fold，檢查所有參數係咪都大過零。[[next]]下一集：第七部分嘅小項目，自己寫一個 MiniVector。"
          "多謝收睇，下次見！",
          EndCard("寫 allPositive(args...)：用 ((args > 0) && ...)；allPositive(1, 2, 3) 係 1，allPositive(1, -2) 係 0。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

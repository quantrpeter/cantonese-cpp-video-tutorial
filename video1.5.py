#!/usr/bin/env python3
"""Video 11 (syllabus 1.5): 算術運算

+ - * / % on real numbers (7 / 2 really prints 3), 7.0 / 2, precedence and brackets; a
seconds -> h m s converter with a real bug (62 minutes) fixed with % 3600; += *= ++.
Run `python3 video11.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 11
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-05"
OPS = (CODE / "ops.cpp").read_text()
TIME = (CODE / "time.cpp").read_text()
PLUS = (CODE / "plus.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
DBL = "    std::cout << 7.0 / 2 << '\\n';\n"
PREC = "    std::cout << 2 + 3 * 4 << '\\n';\n    std::cout << (2 + 3) * 4 << '\\n';\n"
OPS6 = OPS.replace(PREC, "")
OPS5 = OPS6.replace(DBL, "")
BUG = TIME.replace("total % 3600 / 60;", "total / 60;")
CO = "g++ -std=c++20 -Wall -Wextra ops.cpp -o ops"
CT = "g++ -std=c++20 -Wall -Wextra time.cpp -o time"
CP = "g++ -std=c++20 -Wall -Wextra plus.cpp -o plus"

(o1, ro1, o2, ro2, o3, ro3, clr, t1, rt1, t2, rt2, rt3, p1, rp, cch, rch) = cpp.session(
    {"ops.cpp": OPS5, "time.cpp": BUG, "plus.cpp": PLUS}, [
        CO, "./ops", Write("ops.cpp", OPS6), CO, "./ops", Write("ops.cpp", OPS), CO, "./ops",
        "clear", CT, Input("./time", ["3725"]),
        Write("time.cpp", TIME), CT, Input("./time", ["3725"]), Input("./time", ["86399"]),
        CP, "./plus",
        Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["1234"]),
    ], refresh=opts.fresh_runs, cols=48)
vals = ro3.output.split()
assert vals == ["9", "5", "14", "3", "1", "3.5", "14", "20"], vals
assert rt1.output.endswith("1h 62m 5s\n") and rt2.output.endswith("1h 2m 5s\n") and rt3.output.endswith("23h 59m 59s\n")
assert rp.output.strip() == "31" and rch.output.endswith("12 dollars 34 cents\n")
assert all(r.code == 0 for r in (o1, o2, o3, t1, t2, p1, cch))

SAY = {"%": "百分號", "% 3600": "百分號三千六百", "score += 5": "score 加等如五", "score = score + 5": "score 等如 score 加五",
       "score *= 2": "score 乘等如二", "score++": "score plus plus", "+=": "加等如", "*=": "乘等如", "++": "plus plus"}

s = Stage({"ops.cpp": OPS5, "time.cpp": BUG, "plus.cpp": PLUS}, title="算術運算")

scenes = [
    Scene("intro",
          "歡迎返嚟！今集學加減乘除。睇落好簡單，但係 C++ 嘅除數有個陷阱，好多人都中過招。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "+ − * / %")),
    Scene("goal",
          "今集會講：[[b1]]五個算術運算子；[[b2]]整數除法同餘數；[[b3]]先乘除、後加減；[[b4]]仲有 += 同 ++ 呢啲簡寫。",
          BulletCard("今集學識", [("五個算術運算子", "b1"), ("整數除法同餘數 %", "b2"), ("先乘除、後加減", "b3"),
                                ("簡寫：+=、*=、++", "b4")])),
    Scene("ops1",
          "[[open]]先試吓五個算術運算子：加、減、乘、除，同埋百分號，即係計餘數。[[cc]]編譯運行。"
          "[[out]]七加二係九，七減二係五，七乘二係十四。[[div]]但係七除二，竟然係三？",
          s.scene(Open("ops.cpp", at="open"), Run(o1, at="cc"), Run(ro1), Mark(7, at="div"))),
    Scene("intdiv",
          "因為七同二都係整數。[[t1]]整數除整數，答案都係整數，小數部分會直接切走，唔係四捨五入。"
          "[[t2]]百分號就係計除完之後嘅餘數：七除二，商三餘一，所以係一。",
          TileCard("整數除法", [
              Tile("✂️", "7 / 2 → 3", "整數除整數：小數部分直接切走，唔係四捨五入", "t1", BLUE),
              Tile("🧮", "7 % 2 → 1", "餘數：7 除 2，商 3 餘 1", "t2", PURPLE),
          ], cols=2, height=360)),
    Scene("ops2",
          "想要小數答案，[[type]]就將其中一個數寫成七點零，變成 double。[[cc]]編譯運行，[[out]]今次係三點五。",
          s.scene(Mark(None), Type("ops.cpp", DBL, after="7 % 2 << '\\n';\n", at="type"), Expect("ops.cpp", OPS6),
                  Run(o2, at="cc", recall=True), Run(ro2))),
    Scene("prec",
          "[[type]]再試兩條式。[[cc]]運行，[[out1]]二加三乘四，係十四，因為 C++ 同數學一樣，先乘除、後加減。"
          "[[out2]]想先計加數，就要加括號：二加三，再乘四，等於二十。",
          s.scene(Type("ops.cpp", PREC, after=DBL, at="type", rate=20), Expect("ops.cpp", OPS),
                  Run(o3, at="cc", recall=True), Run(ro3), Mark(10, at="out1"), Mark(11, at="out2"))),
    Scene("table",
          "總結一下：[[a]]加、減、乘，同數學一樣；[[d]]整數除整數，會切走小數；[[m]]百分號計餘數；"
          "[[p]]先乘除、後加減，有括號就先計括號。",
          TableCard("算術運算子", ["運算子", "意思", "例子", "結果"], [
              (["+  -  *", "加、減、乘", "7 * 2", vals[2]], "a"),
              (["/", "除（整數會切走小數）", "7 / 2", vals[3]], "d"),
              (["/", "有 double 就有小數", "7.0 / 2", vals[5]], ("d", 0.8)),
              (["%", "餘數", "7 % 2", vals[4]], "m"),
              (["( )", "先計括號入面", "(2 + 3) * 4", vals[7]], "p"),
          ], widths=[0.7, 1.5, 1, 0.6], code_cols=(0, 2, 3), size=42)),
    Scene("time_open",
          "實際用吓。呢個程式將秒數轉做幾多個鐘、幾多分、幾多秒。[[open]]先讀入總秒數。[[h]]一個鐘有三千六百秒，"
          "所以總秒數除三千六百，就係幾多個鐘；[[m]]分鐘就用總秒數除六十；[[s]]秒數係除六十嘅餘數。",
          s.scene(Mark(None), Run(clr), Open("time.cpp", at="open"), Mark(8, at="h"), Mark(9, at="m"), Mark(10, at="s"))),
    Scene("time_run",
          f"[[cc]]編譯運行，[[type]]輸入{zh_int(3725)}秒。[[out]]一個鐘、六十二分、五秒？六十二分唔啱，分鐘最多得五十九。",
          s.scene(Mark(None), Run(t1, at="cc"), Run(rt1, keys=("type",)),
                  Note("62 分？\n分鐘最多得 59！", at="out", where="editor"))),
    Scene("time_fix",
          "問題係：總秒數除六十，連嗰個鐘嘅秒數都計埋入去。[[fix]]應該先 % 3600，攞到一個鐘以外剩低嘅秒數，再除六十。"
          f"[[cc]]再編譯，[[type]]輸入{zh_int(3725)}，[[out]]一個鐘、兩分、五秒，啱晒。",
          s.scene(Note(None), Mark(9, at="fix"), Replace("time.cpp", "total / 60;", "total % 3600 / 60;", at=("fix", 0.3)),
                  Expect("time.cpp", TIME), Run(t2, at="cc", recall=True), Run(rt2, recall=True, keys=("type",)))),
    Scene("steps",
          f"用{zh_int(3725)}逐步計：[[r1]]除三千六百，得一個鐘；[[r2]]除三千六百嘅餘數係一百二十五，即係剩低嘅秒數；"
          f"[[r3]]一百二十五除六十，係兩分鐘；[[r4]]{zh_int(3725)}除六十嘅餘數，係五秒。",
          TableCard("3725 秒 = ?", ["計算", "結果", "意思"], [
              (["3725 / 3600", str(3725 // 3600), "1 個鐘"], "r1"),
              (["3725 % 3600", str(3725 % 3600), "一個鐘以外，剩低 125 秒"], "r2"),
              (["125 / 60", str(125 // 60), "2 分鐘"], "r3"),
              (["3725 % 60", str(3725 % 60), "5 秒"], "r4"),
          ], widths=[1.1, 0.6, 1.6], code_cols=(0, 1), size=44)),
    Scene("time_run2",
          f"[[type]]再試{zh_int(86399)}秒，即係一日差一秒：[[out]]二十三個鐘、五十九分、五十九秒。",
          s.scene(Mark(None), Run(rt3, at="type", recall=True, keys=(("type", 1.0),)))),
    Scene("short",
          "最後講幾個簡寫。[[open]]score 由十開始。[[pe]]score += 5，即係 score = score + 5，變十五；"
          "[[me]]score *= 2，乘二，變三十；[[pp]]score++ 即係加一，變三十一。[[cc]]編譯運行，[[out]]真係三十一。呢啲簡寫，之後寫迴圈嘅時候會成日用到。",
          s.scene(Run(clr), Open("plus.cpp", at="open"), Mark(5, at="pe"), Mark(6, at="me"), Mark(7, at="pp"),
                  Mark(None, at="cc"), Run(p1, at="cc"), Run(rp))),
    Scene("recap",
          "總結：[[r1]]加減乘除，同百分號計餘數；[[r2]]整數除整數會切走小數，要小數就用 double；"
          "[[r3]]先乘除、後加減，有括號先計括號；[[r4]]+=、*=、++ 係簡寫。",
          BulletCard("今集重點", [("+ − * / 同 % 餘數", "r1"), ("整數除整數：切走小數", "r2"),
                                ("先乘除、後加減，括號優先", "r3"), ("簡寫：+=、*=、++", "r4")])),
    Scene("outro",
          f"小挑戰：[[ch]]讀入一個以仙做單位嘅金額，例如{zh_int(1234)}仙，印出係幾多蚊同幾多仙。"
          "[[next]]下一集，我哋會睇吓 int 裝唔落太大嘅數，會發生咩事。多謝收睇，下次見！",
          EndCard("讀入一個以「仙」做單位嘅金額，例如 1234 仙，印出係幾多蚊同幾多仙（12 蚊 34 仙）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

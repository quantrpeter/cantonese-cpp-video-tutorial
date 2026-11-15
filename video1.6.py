#!/usr/bin/env python3
"""Video 12 (syllabus 1.6): 整數溢位

INT_MAX + 1 really wraps to -2147483648; 12! fits in int but 13! comes out as 1932053504;
long long fixes it; the trap where `long long s = 100 * 365 * ...` still overflows (g++'s
-Woverflow warning) until 100LL. Run `python3 video1.6.py --help` for options.
"""

from math import factorial

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 12
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-06"
MAX = (CODE / "max.cpp").read_text()
FACT = (CODE / "fact.cpp").read_text()
SECS = (CODE / "secs.cpp").read_text()
RANGES = (CODE / "ranges.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
FACT_INT = FACT.replace("long long f", "int f")
SECS_INT = SECS.replace("100LL", "100")
W = "g++ -std=c++20 -Wall -Wextra "

(cm, rm, clr, cf, rf, cf2, rf2, cs, rs, cs2, rs2, cr, rr, cch, rch) = cpp.session(
    {"max.cpp": MAX, "fact.cpp": FACT_INT, "secs.cpp": SECS_INT, "ranges.cpp": RANGES}, [
        W + "max.cpp -o max", "./max", "clear",
        W + "fact.cpp -o fact", "./fact",
        Write("fact.cpp", FACT), W + "fact.cpp -o fact", "./fact",
        W + "secs.cpp -o secs", "./secs",
        Write("secs.cpp", SECS), W + "secs.cpp -o secs", "./secs",
        W + "ranges.cpp -o r", "./r",
        Write("challenge.cpp", CHALLENGE), W + "challenge.cpp -o ch", "./ch",
    ], refresh=opts.fresh_runs, cols=48)
assert rm.output.split() == ["2147483647", "-2147483648"]
bad13 = int(rf.output.split("13! = ")[1])
assert bad13 != factorial(13) and rf2.output.endswith(f"13! = {factorial(13)}\n")
assert "integer overflow" in cpp.visible(cs.output) and rs.output.strip() == "-1141367296"
assert rs2.output.strip() == str(100 * 365 * 24 * 3600) and cs2.output.strip() == ""
imin, imax, lmin, lmax = rr.output.split()
assert rch.output.strip() == str(80 * 365 * 24 * 60 * 70)

SAY = {"long long": "long long", "100LL": "一百 L L", "LL": "L L", "13!": "十三嘅階乘", "12!": "十二嘅階乘",
       "n!": "n 嘅階乘", "numeric_limits": "numeric limits"}

s = Stage({"max.cpp": MAX, "fact.cpp": FACT_INT, "secs.cpp": SECS_INT}, title="整數溢位")

scenes = [
    Scene("intro",
          "歡迎返嚟！int 唔係咩數都裝得落。今集睇吓數字太大，會發生咩事，同埋點樣避免。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "overflow · long long")),
    Scene("goal",
          "今集會講：[[b1]]int 最大可以去到幾多；[[b2]]超過咗會點，即係溢位；[[b3]]幾時要用 long long。",
          BulletCard("今集學識", [("int 嘅上限", "b1"), ("溢位 overflow", "b2"), ("幾時用 long long", "b3")])),
    Scene("max",
          "[[open]]numeric_limits 可以話你知 int 最大係幾多。[[cc]]編譯運行，[[out1]]第一行係 int 嘅最大值，大約二十一億。"
          "[[plus]]我哋將佢加一，[[out2]]第二行竟然變咗負二十一億！",
          s.scene(Open("max.cpp", at="open"), Mark(5, at="open"), Run(cm, at="cc"), Run(rm),
                  Mark(7, at="plus"), Note("最大值再加一\n變咗最細嘅負數！", at="out2", where="editor"))),
    Scene("wrap",
          "呢個叫做溢位，overflow。[[odo]]就好似舊式嘅里程錶，數字轉到最大，再加一，就會打圈變返最細。"
          "[[ub]]其實 C++ 標準話，int 溢位係未定義行為，結果唔一定係咁，總之一定唔啱。5.11 會再講。",
          TileCard("溢位 overflow", [
              Tile("🔄", "打圈", f"{imax} + 1\n→ {imin}", "odo", BLUE),
              Tile("⚠️", "未定義行為", "C++ 冇保證結果係乜，總之唔啱（5.11 再講）", "ub", RED),
          ], cols=2, height=360)),
    Scene("fact_table",
          "實際例子：階乘。[[f10]]十嘅階乘係三百六十二萬幾，[[f12]]十二嘅階乘大約四億八千萬，都仲裝得落 int；"
          "[[f13]]但係十三嘅階乘大約六十二億，已經超過 int 嘅上限。",
          TableCard("n! 裝唔裝得落 int？", ["n", "n!", "int 裝得落？"], [
              (["10", f"{factorial(10):,}", "裝得落"], "f10", GREEN),
              (["12", f"{factorial(12):,}", "裝得落"], "f12", GREEN),
              (["13", f"{factorial(13):,}", "超過 2,147,483,647"], "f13", RED),
          ], widths=[0.5, 1.4, 1.4], code_cols=(0, 1), size=46)),
    Scene("fact_run",
          f"[[open]]呢個程式由十二嘅階乘開始，再乘十三。[[cc]]編譯運行，[[out]]十三嘅階乘竟然係{zh_int(bad13 // 10**8)}億幾，"
          f"真正答案應該係{zh_int(factorial(13) // 10**8)}億幾。而且編譯器一句警告都冇。",
          s.scene(Note(None), Mark(None), Run(clr), Open("fact.cpp", at="open"), Run(cf, at="cc"), Run(rf),
                  Note(f"13! 應該係 {factorial(13):,}\n但係印咗 {bad13:,}", at="out", where="editor"))),
    Scene("fact_fix",
          "[[fix]]將 int 改做 long long。long long 有八個 byte，最大大約係九百二十京，即係九後面跟十八個零。"
          f"[[cc]]再編譯運行，[[out]]今次係{zh_int(factorial(13) // 10**8)}億幾，啱晒。",
          s.scene(Note(None), Replace("fact.cpp", "int f", "long long f", at="fix"), Expect("fact.cpp", FACT),
                  Run(cf2, at="cc", recall=True), Run(rf2))),
    Scene("trap",
          "但係有個陷阱。[[open]]計一百年有幾多秒：答案放入 long long，應該冇問題啩？[[cc]]編譯，[[warn]]g++ 警告：int 溢位！"
          "[[run]]運行，[[out]]真係負數。",
          s.scene(Open("secs.cpp", at="open"), Run(cs, at="cc"), Run(rs, at="run")), seed=12),
    Scene("trap_why",
          "因為右邊嘅數字全部都係 int，[[calc]]所以乘數係用 int 計，計完先放入 long long，但係計嘅時候已經溢位咗。"
          "[[fix]]解決方法：喺第一個數後面加 LL，即係 long long，咁成條式就會用 long long 計。"
          "[[cc]]再編譯運行，[[out]]三十一億幾，啱晒。",
          s.scene(Mark(4, at="calc"), Note("右邊全部係 int：\n用 int 計，計嘅時候已經溢位", at="calc", where="editor"),
                  Note(None, at="fix"), Replace("secs.cpp", "100 *", "100LL *", at="fix"), Expect("secs.cpp", SECS),
                  Run(cs2, at="cc", recall=True), Run(rs2), Mark(None))),
    Scene("ranges",
          "記住兩個型別嘅範圍：[[int]]int 大約係正負二十一億；[[ll]]long long 大約係正負九百二十京。"
          "[[rule]]有機會超過二十億嘅數，例如人口、以仙計嘅金額、秒數，就用 long long。",
          TableCard("整數嘅範圍", ["型別", "最細", "最大"], [
              (["int", imin, imax], "int"),
              (["long long", lmin, lmax], "ll"),
          ], widths=[0.7, 1.4, 1.4], code_cols=(0, 1, 2), size=40,
              note=("可能超過 20 億：人口、金額（以仙計）、秒數 → 用 long long", "rule"))),
    Scene("recap",
          "總結：[[r1]]int 最大大約二十一億；[[r2]]超過咗就會溢位，結果亂晒，仲未必有警告；[[r3]]大數用 long long；"
          "[[r4]]成條式都係 int 嘅話，要加 LL，先會用 long long 計。",
          BulletCard("今集重點", [("int 最大約 21 億", "r1"), ("溢位：結果亂晒，未必有警告", "r2"),
                                ("大數用 long long", "r3"), ("式入面要用 100LL，先會用 long long 計", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]假設心臟每分鐘跳七十下，計吓八十年總共跳幾多下，記住揀啱型別。"
          "[[next]]下一集，我哋講小數：點解零點一加零點二，唔係零點三。多謝收睇，下次見！",
          EndCard("假設心臟每分鐘跳 70 下，計吓 80 年總共跳幾多下。記住揀啱型別！",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

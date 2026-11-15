#!/usr/bin/env python3
"""Video 20 (syllabus 2.2): 邏輯運算

The leap-year rule built up in three real runs: `by4` alone gets 1900 wrong, `by4 && !by100`
gets 2000 wrong, `(by4 && !by100) || by400` gets all three right. The truth table comes from a
real run; short-circuit evaluation as a guard against dividing by zero.
Run `python3 video2.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 20
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "02-02"
FINAL = (CODE / "leap.cpp").read_text()
TRUTH = (CODE / "truth.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
S2 = FINAL.replace("if ((by4 && !by100) || by400) {", "if (by4 && !by100) {")
S1 = S2.replace("if (by4 && !by100) {", "if (by4) {")
CC = "g++ -std=c++20 -Wall -Wextra leap.cpp -o leap"
LEAP, NOT = "Leap year\n", "Not a leap year\n"

(c1, a2024, a1900, c2, b1900, b2000, clr, c3, d2000, d1900, d2024, ct, rt, cch, rch) = cpp.session(
    {"leap.cpp": S1, "truth.cpp": TRUTH}, [
        CC, Input("./leap", ["2024"]), Input("./leap", ["1900"]),
        Write("leap.cpp", S2), CC, Input("./leap", ["1900"]), Input("./leap", ["2000"]),
        "clear", Write("leap.cpp", FINAL), CC, Input("./leap", ["2000"]), Input("./leap", ["1900"]), Input("./leap", ["2024"]),
        "g++ -std=c++20 truth.cpp -o truth", "./truth",
        Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["15"]),
    ], refresh=opts.fresh_runs, cols=48)
assert a2024.output.endswith(LEAP) and a1900.output.endswith(LEAP)                  # step 1: 1900 wrong
assert b1900.output.endswith(NOT) and b2000.output.endswith(NOT)                    # step 2: 2000 wrong
assert d2000.output.endswith(LEAP) and d1900.output.endswith(NOT) and d2024.output.endswith(LEAP)
rows = [l.split() for l in rt.output.strip().split("\n")]
assert rows[:4] == [["true", "true", "true", "true"], ["true", "false", "false", "true"],
                    ["false", "true", "false", "true"], ["false", "false", "false", "false"]] and rows[4] == ["false", "true"]
assert "unused variable 'by100'" in cpp.visible(c1.output) and "unused variable" not in cpp.visible(c3.output)
assert all(r.code == 0 for r in (c1, c2, c3, ct, cch)) and rch.output.endswith("Teen\n")

SAY = {"&&": "兩個 and 號", "||": "兩條直線", "!": "感嘆號", "by4": "by 四", "by100": "by 一百", "by400": "by 四百",
       "!by100": "感嘆號 by 一百", "bool": "bool"}

s = Stage({"leap.cpp": S1}, title="邏輯運算：閏年")

scenes = [
    Scene("intro",
          "歡迎返嚟！有時一個條件唔夠用。今集學邏輯運算：且、或、非，將幾個條件組合埋一齊。例子係判斷閏年。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "&& · || · !")),
    Scene("goal",
          "今集會講三個邏輯運算子：[[b1]]且，寫做兩個 and 號；[[b2]]或，寫做兩條直線；[[b3]]非，寫做一個感嘆號；[[b4]]最後講短路求值。",
          BulletCard("今集學識", [("&&：且 and", "b1"), ("||：或 or", "b2"), ("!：非 not", "b3"), ("短路求值", "b4")]), seed=12),
    Scene("rules",
          "閏年嘅規則有三條：[[r1]]年份可以俾四整除，係閏年；[[r2]]但係可以俾一百整除嘅，就唔係；"
          "[[r3]]除非可以俾四百整除，咁又係閏年。所以二零二四年係，一九零零年唔係，二千年係。",
          BulletCard("閏年規則", [("可以俾 4 整除 → 係閏年（2024）", "r1"), ("但係俾 100 整除 → 唔係（1900）", "r2"),
                                ("除非俾 400 整除 → 又係（2000）", "r3")])),
    Scene("step1",
          "[[open]]程式先計三個 bool：可唔可以俾四、一百、四百整除。[[if]]先淨係用第一條規則：俾四整除，就係閏年。",
          s.scene(Open("leap.cpp", at="open"), Mark((7, 9), at=("open", 0.8)), Mark(10, at="if"))),
    Scene("run1",
          "[[cc]]編譯運行。g++ 警告 by100 同 by400 未用到，因為我哋仲未用佢哋，唔緊要。[[t1]]輸入二零二四，[[o1]]係閏年，啱。[[t2]]再試一九零零，[[o2]]佢都話係閏年，錯咗！"
          "一九零零年俾一百整除，唔係閏年。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(a2024, keys=("t1",)), Run(a1900, at="t2", recall=True, keys=(("t2", 0.9),)),
                  Note("1900 唔係閏年！", at="o2", where="editor"))),
    Scene("step2",
          "[[type]]加第二條規則：俾四整除，而且唔俾一百整除。[[and]]兩個 and 號係且：兩邊都要成立；[[not]]感嘆號係非，即係反轉。",
          s.scene(Note(None), Type("leap.cpp", " && !by100", after="if (by4", at="type"), Expect("leap.cpp", S2),
                  Mark(10, at="and"))),
    Scene("run2",
          "[[cc]]再編譯運行，今次淨係 by400 未用到。[[t1]]一九零零，[[o1]]今次啱咗。[[t2]]但係二千年，[[o2]]又錯咗！二千年俾四百整除，應該係閏年。",
          s.scene(Mark(None), Run(c2, at="cc", recall=True), Run(b1900, recall=True, keys=("t1",)),
                  Run(b2000, at="t2", recall=True, keys=(("t2", 0.9),)), Note("2000 係閏年！", at="o2", where="editor"))),
    Scene("step3",
          "[[type]]加第三條：或者俾四百整除。[[or]]兩條直線係或：任何一邊成立就得。前面加個括號，令次序更清楚。",
          s.scene(Note(None), Run(clr, at="type"), Type("leap.cpp", "(", after="if (", at="type"),
                  Type("leap.cpp", ") || by400", after="!by100"), Expect("leap.cpp", FINAL), Mark(10, at="or"))),
    Scene("run3",
          "[[cc]]編譯運行。[[t1]]二千年，[[o1]]係閏年；[[t2]]一九零零，[[o2]]唔係；[[t3]]二零二四，[[o3]]係。三個答案全部啱晒：閏年嘅三條規則，一個條件就寫晒。",
          s.scene(Mark(None), Run(c3, at="cc", recall=True), Run(d2000, recall=True, keys=("t1",)),
                  Run(d1900, at="t2", recall=True, keys=(("t2", 0.9),)), Run(d2024, at="t3", recall=True, keys=(("t3", 0.9),)))),
    Scene("truth",
          "總結三個運算子：[[and]]且，兩邊都係 true，先係 true；[[or]]或，有一邊係 true，就係 true；"
          "[[not]]非，true 變 false，false 變 true。",
          TableCard("真值表", ["a", "b", "a && b", "a || b"], [
              (rows[0], "and"), (rows[1], ("and", 0.4)), (rows[2], ("and", 0.8)), (rows[3], ("and", 1.2)),
          ], code_cols=(0, 1, 2, 3), size=42, note=(f"!true → {rows[4][0]}　　!false → {rows[4][1]}", "not"))),
    Scene("short",
          "仲有一個特性，叫短路求值：[[and]]且嘅左邊係 false，結果一定係 false，右邊就唔會再計；[[or]]或嘅左邊係 true，右邊都唔使計。"
          "[[use]]好處係可以先檢查安全：例如先確定人數大過零，先至做除數，就唔會除以零。",
          AnatomyCard("短路求值", [
              Part("people > 0", "先檢查", GREEN, "and"),
              Part(" &&", "且", AMBER, "and"),
              Part(" sweets / people >= 10", "左邊 false 就唔會計", RED, "use"),
          ], size=60, note=("people 係 0：左邊已經 false，右邊唔計，唔會除以零", "use"))),
    Scene("recap",
          "總結：[[r1]]且：兩邊都成立；[[r2]]或：一邊成立就得；[[r3]]非：反轉；[[r4]]短路求值：答案已經知道，就唔再計右邊。"
          "組合條件嘅時候，加括號會更清楚。",
          BulletCard("今集重點", [("&&：兩邊都要成立", "r1"), ("||：一邊成立就得", "r2"), ("!：反轉", "r3"),
                                ("短路：答案知道咗，右邊唔計", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一個年齡，判斷佢係唔係青少年，即係十三至十九歲。"
          "[[next]]下一集，我哋學 else if，處理多過兩個選擇。多謝收睇，下次見！",
          EndCard("讀入一個年齡，判斷佢係唔係青少年（13 至 19 歲），印出 Teen 或者 Not a teen。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

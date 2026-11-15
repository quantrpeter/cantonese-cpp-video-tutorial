#!/usr/bin/env python3
"""Video 129 (syllabus 11.4): Deadlock

first() locks a then b; second() locks b then a, each sleeping 100 ms in between. The real run
hangs: `timeout 3 ./dead; echo exit $?` prints nothing for 3 seconds and then "exit 124" (killed).
Locking both mutexes at once with std::scoped_lock both(a, b) really finishes: first done,
second done, all done. Run `python3 video129.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 129
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-04"
FINAL = (CODE / "dead.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SLEEP = "    std::this_thread::sleep_for(std::chrono::milliseconds(100));\n"
BAD = (FINAL.replace("    std::scoped_lock both(a, b);\n" + SLEEP, "    std::scoped_lock l1(a);\n" + SLEEP + "    std::scoped_lock l2(b);\n")
       .replace("    std::scoped_lock both(b, a);\n" + SLEEP, "    std::scoped_lock l1(b);\n" + SLEEP + "    std::scoped_lock l2(a);\n"))
CC = "g++ -std=c++20 -Wall -Wextra dead.cpp -o dead"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"dead.cpp": BAD}, [
    CC, "timeout 3 ./dead; echo exit $?", "clear", Write("dead.cpp", FINAL), CC, "./dead",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "exit 124\n" and r1.seconds > 2.5, r1.output
assert sorted(r2.output.split("\n")[:2]) == ["first done", "second done"] and r2.output.endswith("all done\n"), r2.output
assert c1.code == c2.code == cch.code == 0 and rch.output == "100 100\n"

SAY = {"deadlock": "deadlock", "std::scoped_lock": "S T D scoped lock", "scoped_lock": "scoped lock", "timeout 3": "timeout 三",
       "timeout": "timeout", "exit 124": "exit 一二四", "mutex": "mutex", "first": "first", "second": "second", "l1": "l 一", "l2": "l 二",
       "transfer": "transfer"}

s = Stage({"dead.cpp": BAD}, title="Deadlock", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！mutex 可以保護資料，但係用得唔好，兩個 thread 會互相等對方，永遠停喺度，叫 deadlock，死鎖。今集整一個出嚟，再修好佢。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "互相等 · 鎖嘅次序 · scoped_lock")),
    Scene("goal",
          "今集會講：[[b1]]deadlock 點樣發生；[[b2]]真係卡死嘅程式；[[b3]]統一鎖嘅次序；[[b4]]用 scoped_lock 一次過鎖幾個。",
          BulletCard("今集學識", [("互相等對方", "b1"), ("卡死：timeout 先停到", "b2"), ("統一次序", "b3"), ("scoped_lock(a, b)", "b4")])),
    Scene("code",
          "[[two]]兩個 mutex：a 同 b。[[first]]first 先鎖 a，等一陣，再鎖 b；[[second]]second 剛好相反，先鎖 b，再鎖 a。[[main]]main 用兩個 thread 同時行佢哋。",
          s.scene(Open("dead.cpp", at="two"), Mark(6, at="two"), Mark((8, 13), at="first"), Mark((15, 20), at="second"), Mark((22, 26), at="main"))),
    Scene("hang",
          "[[cc]]編譯，再用 timeout 三運行，即係最多等三秒。[[o]]乜都冇印，三秒之後俾 timeout 殺咗，exit 一二四。程式真係卡死咗。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, at="o"))),
    Scene("why",
          "[[a]]first 攞咗 a，等緊 b；[[b]]second 攞咗 b，等緊 a。[[cycle]]兩個都唔放手，又等緊對方手上嗰個，就永遠等落去。",
          TableCard("點解卡死", ["thread", "攞住", "等緊"], [
              (["first", "a", "b"], "a"),
              (["second", "b", "a"], "b"),
          ], widths=[1, 1, 1], code_cols=(1, 2), size=44, note=("互相等：冇人放手", "cycle"))),
    Scene("fix",
          "[[type]]解決方法：用 scoped_lock 一次過鎖兩個 mutex。佢入面有防止死鎖嘅演算法，就算兩邊寫嘅次序唔同都唔怕。[[cc]]編譯運行：[[o]]兩個都做完，all done。",
          s.scene(Run(clr, at="type"), Replace("dead.cpp", BAD.split("void first")[1].split("int main")[0], FINAL.split("void first")[1].split("int main")[0],
                                                at="type", rate=50),
                  Expect("dead.cpp", FINAL), Mark(9, at="type"), Mark(15, at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("rules",
          "避免死鎖嘅規則：[[order]]要鎖幾個 mutex，所有地方都用同一個次序；[[scoped]]或者用 scoped_lock 一次過鎖晒；[[short]]鎖住嘅時間越短越好，唔好喺鎖住嘅時候做慢嘢。",
          BulletCard("避免 deadlock", [("統一鎖嘅次序", "order"), ("std::scoped_lock(a, b) 一次過鎖", "scoped"), ("鎖住嘅時間越短越好", "short")])),
    Scene("recap",
          "總結：[[r1]]兩個 thread 互相等對方手上嘅鎖，就係 deadlock；[[r2]]程式唔會當機，只係永遠卡住；[[r3]]統一次序可以避免；[[r4]]scoped_lock 一次過鎖幾個最穩陣。",
          BulletCard("今集重點", [("互相等：deadlock", "r1"), ("唔當機，只係卡住", "r2"), ("統一次序", "r3"), ("scoped_lock(a, b)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]兩個戶口，兩個 thread 互相轉帳一千次，用 scoped_lock 鎖住兩個戶口嘅 mutex，最後兩邊都應該係一百。[[next]]下一集：condition_variable。多謝收睇，下次見！",
          EndCard("transfer(from, to, amount) 用 std::scoped_lock 鎖 from.m 同 to.m；x→y、y→x 各轉 1000 次，最後 100 100。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 107 (syllabus 8.20): chrono

Durations with units: seconds{90} prints 90s, converts silently to 90000ms, and needs
duration_cast to become minutes (1min, truncated). Going the lossy way implicitly
(seconds back = ms;) is a real "conversion from 'duration<...1000>>' ... requested" error.
A steady_clock stopwatch around sleep_for(250ms) really prints 250ms (between 250 and 300).
Run `python3 video8.20.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 107
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-20"
FINAL = (CODE / "clock.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
WATCH = "    auto start" + FINAL.split("    auto start")[1].rsplit("}\n", 1)[0]
V1 = FINAL.replace(WATCH, "").replace("#include <thread>\n", "")
BACK = "    seconds back = ms;\n"
BAD = V1.replace("    auto m = duration_cast", BACK + "    auto m = duration_cast")
CC = "g++ -std=c++20 -Wall -Wextra clock.cpp -o clk"

(c1, r1, c2, clr, c3, r3, cch, rch) = cpp.session({"clock.cpp": V1}, [
    CC, "./clk", Write("clock.cpp", BAD), CC, "clear", Write("clock.cpp", FINAL), CC, "./clk",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "90s 90000ms 1min\n" and r3.output.startswith("90s 90000ms 1min\n"), r3.output
took = int(re.fullmatch(r"(\d+)ms\n", r3.output.split("\n", 1)[1]).group(1))
assert 250 <= took < 300 and "conversion from 'duration<[...],ratio<[...],1000>>'" in cpp.visible(c2.output)
assert c1.code == c3.code == cch.code == 0 and rch.output == "50000005000000 1\n"
D = "零一二三四五六七八九"
say_took = "二百" + D[took // 10 % 10] + "十" + (D[took % 10] if took % 10 else "")

SAY = {"std::chrono": "S T D chrono", "chrono": "chrono", "seconds": "seconds", "milliseconds": "milliseconds", "minutes": "minutes",
       "duration_cast": "duration cast", "steady_clock": "steady clock", "steady_clock::now()": "steady clock now", "sleep_for": "sleep for",
       "250ms": "二百五十 m s", "90s": "九十 s", "90000ms": "九萬 m s", "1min": "一 min", "std::this_thread": "this thread",
       "using namespace std::chrono": "using namespace chrono", "count()": "count"}

s = Stage({"clock.cpp": V1}, title="chrono", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！時間如果只係一個 int，九十係秒定毫秒？好易搞錯。std::chrono 將單位放入類型入面；仲可以用嚟計一段 code 行咗幾耐。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "duration · duration_cast · 計時")),
    Scene("goal",
          "今集會講：[[b1]]有單位嘅時間；[[b2]]單位轉換；[[b3]]會蝕嘅轉換要講明；[[b4]]用 steady_clock 做秒錶。",
          BulletCard("今集學識", [("seconds、milliseconds", "b1"), ("自動轉細單位", "b2"), ("duration_cast", "b3"), ("steady_clock 秒錶", "b4")])),
    Scene("units",
          "[[using]]喺 main 入面 using namespace std::chrono，寫法短啲。[[s]]九十秒。[[ms]]轉做毫秒，自動轉，因為唔會蝕。[[m]]轉做分鐘要用 duration_cast，"
          "因為九十秒唔係整數分鐘。[[cc]]編譯運行，[[o]]九十 s、九萬 m s、一 min：小數直接截走咗。單位一齊印出嚟，一睇就知。",
          s.scene(Open("clock.cpp", at="using"), Mark(5, at="using"), Mark(6, at="s"), Mark(7, at="ms"), Mark(8, at="m"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("lossy",
          "[[type]]如果反過嚟，將毫秒直接變秒呢？[[cc]]編譯：[[err]]錯誤！毫秒變秒可能會蝕，chrono 唔俾你靜靜雞咁做，一定要用 duration_cast 講明。",
          s.scene(Type("clock.cpp", BACK, before="    auto m = duration_cast", at="type"), Expect("clock.cpp", BAD),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("rule",
          "規則：[[fine]]大單位變細單位，例如秒變毫秒，自動；[[coarse]]細變大，例如毫秒變秒，可能有小數，要 duration_cast，而且會截走小數。",
          TableCard("單位轉換", ["方向", "寫法"], [
              (["秒 → 毫秒（唔會蝕）", "milliseconds ms = s;"], "fine", GREEN),
              (["毫秒 → 秒（可能蝕）", "duration_cast<seconds>(ms)"], "coarse", AMBER),
          ], widths=[1.3, 1.6], code_cols=(1,), size=38)),
    Scene("watch",
          "[[del]]刪走嗰句。[[type]]做一個秒錶：steady_clock now 記低開始，[[sleep]]訓二百五十毫秒，[[end]]再記低結束，相減就係用咗幾耐，再轉做毫秒。",
          s.scene(Run(clr, at="del"), Replace("clock.cpp", BACK, "", at="del"),
                  Replace("clock.cpp", "#include <iostream>\n", "#include <iostream>\n#include <thread>\n", at="type", rate=40),
                  Type("clock.cpp", WATCH, before="}", last=True, rate=60), Expect("clock.cpp", FINAL), Mark(11, at="type"), Mark(12, at="sleep"),
                  Mark((13, 14), at="end"))),
    Scene("watchrun",
          f"[[cc]]編譯運行，[[o]]{say_took} m s：比二百五十多少少，因為叫醒都要時間。",
          s.scene(Mark(None), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("clocks",
          "[[steady]]計時用 steady_clock，佢只會向前行；[[system]]system_clock 係牆上嘅時鐘，可能俾人調較，唔啱用嚟計時間差。",
          TableCard("用邊個 clock？", ["clock", "用途"], [
              (["steady_clock", "計時：只會向前"], "steady", GREEN),
              (["system_clock", "而家幾點：可能被調整"], "system"),
          ], widths=[1.2, 1.6], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]chrono 嘅時間有單位，唔會撈亂；[[r2]]變細單位自動，變大單位要 duration_cast；[[r3]]steady_clock 兩次相減就係秒錶；[[r4]]C++20 可以直接印出 duration。",
          BulletCard("今集重點", [("seconds、milliseconds…", "r1"), ("duration_cast：細 → 大", "r2"), ("steady_clock::now() 相減", "r3"),
                                ("cout << took", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 steady_clock 計吓由一加到一千萬要幾耐，印出總和，同埋有冇少過五秒。[[next]]下一集：第八部分嘅小項目，單字頻率統計。多謝收睇，下次見！",
          EndCard("用 steady_clock 計時：加 1 到 10,000,000，印出總和同 (took < 5s)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 131 (syllabus 11.6): async 同 future

std::async runs half of a 10,000,000-element sum on another thread while main sums the other half;
left.get() + right really prints 10000000. An exception thrown inside an async task is re-thrown
by get(): the run prints "caught oops". A std::promise set from a jthread delivers 42 through
its std::future. Run `python3 video131.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 131
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-06"
FINAL = (CODE / "future.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
EXC = "    auto bad" + FINAL.split("    auto bad")[1].split("    std::promise")[0]
PROM = "    std::promise" + FINAL.split("    std::promise")[1].rsplit("}\n", 1)[0]
V2 = FINAL.replace(PROM, "")
V1 = V2.replace(EXC, "")
CC = "g++ -std=c++20 -Wall -Wextra future.cpp -o fut"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"future.cpp": V1}, [
    CC, "./fut", "clear", Write("future.cpp", V2), CC, "./fut", "clear", Write("future.cpp", FINAL), CC, "./fut",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "10000000\n" and r2.output == "10000000\ncaught oops\n" and r3.output == "10000000\ncaught oops\n42\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "2000000\n"

SAY = {"std::async": "S T D async", "async": "async", "std::launch::async": "launch async", "std::future": "S T D future", "future": "future",
       "std::promise": "S T D promise", "promise": "promise", "get()": "get", "left.get()": "left 點 get", "set_value": "set value",
       "get_future": "get future", "sumRange": "sum range", "accumulate": "accumulate", "oops": "oops", "jthread": "j thread"}

s = Stage({"future.cpp": V1}, title="async 同 future", code_px=21)

scenes = [
    Scene("intro",
          "歡迎返嚟！用 thread 做嘢，點樣攞返結果？自己開變數、自己鎖好麻煩。std::async 會回傳一個 future：一張「將來會有結果」嘅收據。今集用佢做平行加總。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::async · future · promise")),
    Scene("goal",
          "今集會講：[[b1]]async 喺另一個 thread 行；[[b2]]future 點 get 攞結果；[[b3]]exception 都會傳返嚟；[[b4]]promise 自己交結果。",
          BulletCard("今集學識", [("std::async(std::launch::async, f)", "b1"), ("future.get()", "b2"), ("get() 會重新 throw", "b3"), ("std::promise", "b4")])),
    Scene("sum",
          "[[fn]]sumRange 加一段範圍。[[async]]一千萬個一，左半交俾 async，喺另一個 thread 計；launch async 即係一定要開新 thread。[[right]]同一時間，main 自己計右半。"
          "[[get]]left 點 get 會等佢計完，攞結果。[[cc]]編譯運行：[[o]]一千萬。兩邊同時計，唔使自己開 thread，亦唔使自己鎖，好簡潔。",
          s.scene(Open("future.cpp", mode="instant"), Mark((8, 11), at="fn"), Mark((16, 18), at="async"), Mark(19, at="right"), Mark(20, at="get"),
                  Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("receipt",
          "[[ticket]]future 好似取餐嘅收據：[[work]]廚房喺後面做緊；[[wait]]你攞住收據去 get，未整好就等，整好就攞到。get 只可以攞一次。",
          TableCard("future 好似取餐收據", ["", "程式"], [
              (["落單", "auto f = std::async(…);"], "ticket"),
              (["廚房做緊", "另一個 thread 行緊"], "work"),
              (["攞餐", "f.get()：未好就等"], "wait", GREEN),
          ], widths=[0.8, 1.8], code_cols=(), size=40)),
    Scene("exc",
          "[[type]]如果 async 入面 throw 呢？[[get]]exception 會儲起，等你 get 嘅時候喺呢邊重新 throw，所以用 try catch 包住 get 就接到。[[cc]]運行：[[o]]caught oops。exception 由另一個 thread 安全咁傳返嚟。",
          s.scene(Run(clr, at="type"), Type("future.cpp", EXC, before="}", last=True, at="type", rate=70), Expect("future.cpp", V2),
                  Mark((24, 28), at="get"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("promise",
          "[[type]]promise 係自己控制嘅版本：future 由 promise 攞；[[set]]另一個 thread 喺任何時候 set_value，[[get]]呢邊 get 就收到。[[cc]]運行：[[o]]四十二。get 會等到 set_value 為止。",
          s.scene(Mark(None), Run(clr2, at="type"), Type("future.cpp", PROM, before="}", last=True, at="type", rate=60), Expect("future.cpp", FINAL),
                  Mark(31, at="set"), Mark(32, at="get"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]std::async 喺另一個 thread 行函數，回傳 future；[[r2]]get 等結果，只可以 get 一次；[[r3]]入面嘅 exception 會喺 get 重新 throw；[[r4]]promise 可以自己交結果俾 future。",
          BulletCard("今集重點", [("async → future", "r1"), ("get()：等，只一次", "r2"), ("exception 經 get 傳返", "r3"), ("promise.set_value", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將一百萬個二分做四份，每份用一個 async 加，最後將四個 future 嘅結果加埋。[[next]]下一集：第十一部分嘅小項目，平行搵質數。多謝收睇，下次見！",
          EndCard("std::vector<std::future<long long>>：四個 async 各加四分一，再逐個 get 加埋（答案 2000000）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

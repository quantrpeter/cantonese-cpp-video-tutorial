#!/usr/bin/env python3
"""Video 126 (syllabus 11.1): thread 同 jthread

Two counters run as two std::threads. Without join() the real run prints "done" and then
"terminate called without an active exception" / Aborted. With join() both count to 3; their
output really interleaves and can even mix inside one item (the real run's text is shown as it
came). std::jthread joins by itself at the end of its block. Run `python3 video126.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 126
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "11-01"
FINAL = (CODE / "threads.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = FINAL.split("int main")[0]
MAIN_J = ("int main() {\n    std::thread a(count, \"A\", 3);\n    std::thread b(count, \"B\", 3);\n    a.join();\n    b.join();\n"
          "    std::cout << \"\\ndone\\n\";\n}\n")
JOINS = "    a.join();\n    b.join();\n"
V2 = HEAD + MAIN_J
BAD = V2.replace(JOINS, "")
CC = "g++ -std=c++20 -Wall -Wextra threads.cpp -o th"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"threads.cpp": BAD}, [
    CC, "./th", "clear", Write("threads.cpp", V2), CC, "./th", "clear", Write("threads.cpp", FINAL), CC, "./th",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert "terminate called without an active exception" in r1.output and r1.code != 0, r1.output
for r in (r2, r3):
    body = r.output.split("\n")[0]
    assert sorted(body.replace(" ", "")) == sorted("A1B1A2B2A3B3") and r.output.endswith("\ndone\n"), r.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "0 1 4 9 \n"

SAY = {"std::thread": "S T D thread", "std::jthread": "S T D j thread", "jthread": "j thread", "thread": "thread", "join()": "join",
       "join": "join", "terminate": "terminate", "std::flush": "flush", "sleep_for": "sleep for", "count": "count", "done": "done",
       "lambda": "lambda", "C++20": "C++ 二十"}

s = Stage({"threads.cpp": BAD}, title="thread 同 jthread", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！第十一部分講並行：同一時間做幾樣嘢。而家部電腦有好多個核心，用 thread 就可以分工。今集由最基本嘅 std::thread 同 C++20 嘅 jthread 開始。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::thread · join · jthread")),
    Scene("goal",
          "今集會講：[[b1]]開一個 thread；[[b2]]唔 join 會點；[[b3]]兩個 thread 嘅輸出會撈埋；[[b4]]jthread 自動 join。",
          BulletCard("今集學識", [("std::thread t(函數, 參數…)", "b1"), ("冇 join：terminate", "b2"), ("輸出交錯", "b3"), ("std::jthread", "b4")])),
    Scene("start",
          "[[fn]]count 由一數到 n，每次印名同數字，再訓一百毫秒。[[two]]main 開兩個 thread：a 數 A，b 數 B；std::thread 後面先寫函數，再寫參數。[[cc]]編譯運行：[[o]]印咗 done，"
          "跟住 terminate，當機！A 同 B 都未數完。點解？",
          s.scene(Open("threads.cpp", at="fn"), Mark((5, 10), at="fn"), Mark((13, 14), at="two"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("why",
          "[[main]]因為 main 冇等兩個 thread 做完，就行到尾；[[dtor]]thread 物件解構嗰陣，如果仲未 join，就會叫 terminate。[[join]]join 即係：喺度等，等佢做完先繼續。",
          BulletCard("點解當機", [("main 冇等，直接行到尾", "main"), ("std::thread 解構：未 join → terminate", "dtor"), ("join()：等佢做完", "join")])),
    Scene("join",
          "[[type]]加返兩句 join。[[cc]]運行：[[o]]A 同 B 交替出現，因為兩個真係同時行緊；而且次序唔固定，有時仲會撈埋喺同一格。最後先印 done。",
          s.scene(Run(clr, at="type"), Type("threads.cpp", JOINS, after="    std::thread b(count, \"B\", 3);\n", at="type", rate=30), Expect("threads.cpp", V2),
                  Mark((15, 16), at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("jthread",
          "[[type]]C++20 嘅 jthread 更安全：佢解構嘅時候會自動 join。[[block]]用一對大括號包住，離開大括號，兩個 jthread 就會等埋對方做完。[[cc]]運行：[[o]]一樣，唔使自己 join。",
          s.scene(Run(clr2, at="type"), Replace("threads.cpp", "int main" + V2.split("int main")[1].rstrip("\n"), "int main" + FINAL.split("int main")[1].rstrip("\n"),
                                                 at="type", rate=60),
                  Expect("threads.cpp", FINAL), Mark((13, 16), at="block"), Mark(None, at="cc"), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("rules",
          "記住：[[j]]std::thread 一定要 join，或者 detach；[[jt]]新 code 優先用 jthread；[[out]]幾個 thread 同時用 cout，輸出會撈亂，下一集會講更嚴重嘅問題：data race。",
          TableCard("thread vs jthread", ["", "std::thread", "std::jthread"], [
              (["完結時", "自己 join，唔係就 terminate", "自動 join"], "j"),
              (["C++ 版本", "C++11", "C++20"], "jt", GREEN),
          ], widths=[0.8, 1.7, 1.2], code_cols=(), size=38, note=("多個 thread 用 cout：輸出會撈亂", "out"))),
    Scene("recap",
          "總結：[[r1]]std::thread 開一個新 thread，後面跟函數同參數；[[r2]]一定要 join，唔係就 terminate；[[r3]]幾個 thread 同時行，次序唔固定；[[r4]]jthread 自動 join。",
          BulletCard("今集重點", [("std::thread t(f, args…)", "r1"), ("一定要 join", "r2"), ("次序唔固定", "r3"), ("jthread：自動 join", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 vector 裝四個 jthread，每個將自己嘅編號平方，寫入結果 vector 對應嘅格，最後印出嚟。[[next]]下一集：data race 同 mutex。多謝收睇，下次見！",
          EndCard("std::vector<std::jthread> 開 4 個，第 i 個寫 results[i] = i * i；離開大括號後印出 0 1 4 9。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

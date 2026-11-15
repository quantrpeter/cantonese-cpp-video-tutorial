#!/usr/bin/env python3
"""Video 109 (syllabus 9.1): Exception 入門

divide() throws std::runtime_error when b is 0. Uncaught, the real run prints 3.5 then
"terminate called after throwing an instance of 'std::runtime_error' / what(): divide by zero"
and Aborted. With try/catch: 3.5, caught: divide by zero, still running ("never" skipped).
With Guard objects printing in their destructors the real run shows stack unwinding:
~divide, 3.5, ~divide, ~main, caught. Run `python3 video109.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 109
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "09-01"
FINAL = (CODE / "throw.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
GUARD = "struct Guard" + FINAL.split("struct Guard")[1].split("double divide")[0]
V2 = FINAL.replace(GUARD, "").replace("    Guard g{\"divide\"};\n", "").replace("        Guard g{\"main\"};\n", "")
MAIN2 = "int main" + V2.split("int main")[1]
MAIN1 = ("int main() {\n    std::cout << divide(7, 2) << '\\n';\n    std::cout << divide(1, 0) << '\\n';\n"
         "    std::cout << \"never\\n\";\n    std::cout << \"still running\\n\";\n}\n")
V1 = V2.replace(MAIN2, MAIN1)
CC = "g++ -std=c++20 -Wall -Wextra throw.cpp -o th"

(c1, r1, clr, c2, r2, clr2, c3, r3, cch, rch) = cpp.session({"throw.cpp": V1}, [
    CC, "./th", "clear", Write("throw.cpp", V2), CC, "./th", "clear", Write("throw.cpp", FINAL), CC, "./th",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.startswith("3.5\nterminate called after throwing an instance of 'std::runtime_error'") and "never" not in r1.output
assert r1.output.rstrip().endswith("Aborted") and r1.code != 0, r1.output
assert r2.output == "3.5\ncaught: divide by zero\nstill running\n", r2.output
assert r3.output == "~divide\n3.5\n~divide\n~main\ncaught: divide by zero\nstill running\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output == "20\ncaught: negative age\n"

SAY = {"throw": "throw", "try": "try", "catch": "catch", "std::runtime_error": "S T D runtime error", "runtime_error": "runtime error",
       "e.what()": "e 點 what", "what()": "what", "Guard": "Guard", "~divide": "divide 解構", "~main": "main 解構", "terminate": "terminate",
       "stack unwinding": "stack unwinding", "<stdexcept>": "std except", "never": "never", "still running": "still running", "divide": "divide"}

s = Stage({"throw.cpp": V1}, title="Exception 入門", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！第九部分講錯誤處理。一個函數遇到做唔到嘅情況，例如除以零，點樣通知叫佢嘅人？今集學 exception：throw、try 同 catch。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "throw · try · catch · unwinding")),
    Scene("goal",
          "今集會講：[[b1]]throw 拋出 exception；[[b2]]冇人接會點；[[b3]]try 同 catch 接住；[[b4]]stack unwinding。",
          BulletCard("今集學識", [("throw std::runtime_error(…)", "b1"), ("冇人接：terminate", "b2"), ("try { } catch { }", "b3"), ("stack unwinding", "b4")])),
    Scene("throw",
          "[[fn]]divide 見到 b 係零，就 throw 一個 runtime_error，帶住一句說明。[[main]]main 先除七同二，再除一同零。[[cc]]編譯運行：[[o]]三點五；跟住 terminate，"
          "程式當機。never 同 still running 都冇印。",
          s.scene(Open("throw.cpp", at="fn"), Mark((5, 10), at="fn"), Mark((13, 16), at="main"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("what",
          "[[jump]]throw 之後，函數即刻停，唔會 return；exception 會一直向外飛，搵有冇人接。[[none]]一路去到 main 都冇人接，就會叫 terminate，成個程式結束。",
          BulletCard("throw 之後", [("即刻離開，唔會 return", "jump"), ("一層層向外搵 catch", "jump"), ("冇人接 → std::terminate → 當機", "none")])),
    Scene("catch",
          "[[type]]用 try 包住可能出事嘅 code，[[c]]後面 catch 一個 runtime_error 嘅 const reference；what 攞返嗰句說明。[[cc]]運行：[[o]]三點五；caught，divide by zero；"
          "never 冇印，因為已經跳咗去 catch；之後 still running，程式繼續。",
          s.scene(Run(clr, at="type"), Replace("throw.cpp", MAIN1.rstrip("\n"), MAIN2.rstrip("\n"), at="type", rate=60), Expect("throw.cpp", V2),
                  Mark((13, 17), at="type"), Mark((17, 19), at="c"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("unwind",
          "跳走嘅時候，啲局部變數點算？[[type]]寫一個 Guard，解構嗰陣印個名；[[put]]divide 同 main 嘅 try 入面各放一個。[[cc]]運行：[[o]]第一次 divide 正常完，印 divide 解構；"
          "第二次 throw 之後，divide 嘅 Guard 解構，跟住 main 嘅 Guard 都解構，最後先到 catch。",
          s.scene(Run(clr2, at="type"), Type("throw.cpp", GUARD, before="double divide", at="type", rate=60),
                  Type("throw.cpp", "    Guard g{\"divide\"};\n", after="double divide(int a, int b) {\n", at="put"),
                  Type("throw.cpp", "        Guard g{\"main\"};\n", after="    try {\n"), Expect("throw.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("raii",
          "呢個就叫 stack unwinding：[[up]]exception 一層層向外飛，[[dtor]]沿途每個局部物件都會正常解構。[[raii]]所以 5.8 嘅 RAII 好重要：資源由解構子還，就算出錯都唔會漏。",
          TableCard("stack unwinding", ["次序", "發生咩事"], [
              (["① throw", "divide 即刻停"], "up"),
              (["② ~divide", "divide 嘅 Guard 解構"], "dtor"),
              (["③ ~main", "try 入面嘅 Guard 解構"], "dtor"),
              (["④ catch", "處理錯誤"], "raii", GREEN),
          ], widths=[0.8, 1.8], code_cols=(), size=40, note=("RAII：出錯都會清理", "raii"))),
    Scene("recap",
          "總結：[[r1]]throw 拋出 exception，函數即刻停；[[r2]]冇人 catch 就 terminate；[[r3]]try 包住，catch const reference，用 what 攞說明；[[r4]]飛出去嘅途中，局部物件會解構。",
          BulletCard("今集重點", [("throw：即刻停", "r1"), ("冇 catch：terminate", "r2"), ("catch (const E& e)、e.what()", "r3"), ("stack unwinding", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 checkAge，年齡係負數就 throw；main 用迴圈試二十同負五，每次都 try catch。[[next]]下一集：標準同自訂 exception。多謝收睇，下次見！",
          EndCard("寫 int checkAge(int age)：負數就 throw std::runtime_error(\"negative age\")；試 20 同 -5，各自 try / catch。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

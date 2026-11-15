#!/usr/bin/env python3
"""Video 48 (syllabus 4.7): 字串操作

Parsing "08:30": find(':'), substr, std::stoi, std::to_string and replace; typing "0830" really
gives npos, a nonsense 50630 minutes and an out_of_range abort from replace; checking for
std::string::npos fixes it. Run `python3 video4.7.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 48
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-07"
FINAL = (CODE / "time.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CHECK = "    if (colon == std::string::npos) {\n        std::cout << \"No colon!\\n\";\n        return 1;\n    }\n"
REPL = "    text.replace(colon, 1, \"h\");\n    std::cout << text << '\\n';\n"
V2 = FINAL.replace(CHECK, "")
V1 = V2.replace(REPL, "")
SKEL = "#include <iostream>\n#include <string>\n\nint main() {\n}\n"
PARSE = V1.split("int main() {\n")[1].rsplit("}", 1)[0]
CC = "g++ -std=c++20 -Wall -Wextra time.cpp -o time"

(c1, r1, c2, r2, r3, clr, c4, r4, r5, cch, rch) = cpp.session({"time.cpp": V1}, [
    CC, Input("./time", ["08:30"]), Write("time.cpp", V2), CC, Input("./time", ["08:30"]), Input("./time", ["0830"]),
    Write("time.cpp", FINAL), "clear", CC, Input("./time", ["0830"]), Input("./time", ["23:59"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["2026-11-14"]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("510 minutes\n") and r2.output.endswith("510 minutes\n08h30\n")
assert "50630 minutes" in r3.output and "out_of_range" in r3.output and r3.code != 0, r3.output
assert r4.output.endswith("No colon!\n") and r4.code == 1 and r5.output.endswith("1439 minutes\n23h59\n")
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output.endswith("2026 11 14\n")

SAY = {"find": "find", "substr": "sub str", "std::stoi": "S T D S to I", "stoi": "S to I", "std::to_string": "S T D to string",
       "to_string": "to string", "replace": "replace", "npos": "N pos", "std::string::npos": "S T D string N pos",
       "08:30": "零八冒號三零", "0830": "零八三零"}

s = Stage({"time.cpp": SKEL}, title="字串操作：拆時間", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！用家輸入嘅資料，好多時係一串文字，例如八點半打成零八冒號三零。今集學點樣拆開同轉換字串。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "find · substr · stoi · to_string · replace")),
    Scene("goal",
          "今集會講：[[b1]]find 搵位置；[[b2]]substr 切出一段；[[b3]]stoi 同 to_string：字串同數字互換；[[b4]]replace 替換。",
          BulletCard("今集學識", [("find：搵位置", "b1"), ("substr：切一段", "b2"), ("stoi / to_string：互換", "b3"),
                                ("replace：替換", "b4")])),
    Scene("parse",
          "[[read]]讀入一個時間字串。[[find]]find 搵冒號喺第幾個位，回傳嘅係 std::size_t。[[sub]]substr 由零開始切，切到冒號之前，就係鐘數；"
          "由冒號後面一直切到尾，就係分鐘。[[stoi]]stoi 將字串變做 int。[[ts]]最後計總分鐘，用 to_string 變返字串，接埋文字。四個工具，一齊用。",
          s.scene(Open("time.cpp", mode="instant"),
                  Type("time.cpp", "".join(PARSE.splitlines(True)[:3]), before="}", last=True, at="read", rate=34),
                  Type("time.cpp", PARSE.splitlines(True)[3], before="}", last=True, at="find", rate=30),
                  Type("time.cpp", "".join(PARSE.splitlines(True)[4:6]), before="}", last=True, at="sub", rate=34),
                  Type("time.cpp", "".join(PARSE.splitlines(True)[6:]), before="}", last=True, at="ts", rate=34),
                  Expect("time.cpp", V1))),
    Scene("table",
          "用零八冒號三零做例子：[[f]]find 搵到冒號喺位置二；[[s1]]substr(0, 2)，由零開始切兩個字元，得零八；[[s2]]substr(3)，由三切到尾，得三零；"
          "[[n]]stoi 變做數字八同三十；[[t]]八乘六十加三十，係五百一十分鐘。",
          TableCard("text = \"08:30\"", ["寫法", "結果"], [
              (["text.find(':')", "2"], "f"),
              (["text.substr(0, 2)", "\"08\""], "s1"),
              (["text.substr(3)", "\"30\""], "s2"),
              (["std::stoi(\"08\")", "8"], "n"),
              (["std::to_string(510)", "\"510\""], "t"),
          ], widths=[1.6, 1], code_cols=(0, 1), size=40)),
    Scene("run1",
          "[[cc]]編譯運行，[[t]]輸入零八冒號三零，[[o]]五百一十分鐘：即係八乘六十，再加三十。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("t",)))),
    Scene("replace",
          "[[type]]再試 replace：喺冒號嘅位置，替換一個字元，換做 h。[[cc]]運行，[[t]]零八冒號三零，[[o]]變咗零八 h 三零。",
          s.scene(Type("time.cpp", REPL, before="}", last=True, at="type", rate=26), Expect("time.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=("t",)))),
    Scene("bug",
          "如果用家唔打冒號呢？[[t]]輸入零八三零。[[o]]五萬零六百三十分鐘？仲要即刻當機：out of range。",
          s.scene(Run(r3, at="t", recall=True, keys=(("t", 0.9),)), Note("50630 分鐘？\n仲要當機！", at="o", where="editor"))),
    Scene("npos",
          "[[npos]]find 搵唔到嘅時候，會回傳一個特別嘅值：std::string::npos，係一個好大好大嘅數，代表搵唔到。"
          "[[wrong]]我哋冇檢查，就拎咗佢嚟切字串，結果亂晒。[[fix]]所以 find 之後，一定要檢查係咪 npos。搵唔到，就唔好再切。",
          s.scene(Note("搵唔到：find 回傳 npos\n＝ 一個超大嘅數", at="npos", where="editor"), Note(None, at="fix"),
                  Type("time.cpp", CHECK, after="std::size_t colon = text.find(':');\n", at="fix", rate=30), Expect("time.cpp", FINAL))),
    Scene("run2",
          "[[cc]]再編譯。[[t1]]零八三零，[[o1]]今次話冇冒號。[[t2]]二十三冒號五十九，[[o2]]一千四百三十九分鐘，正常。",
          s.scene(Run(clr, at="cc"), Run(c4, recall=True), Run(r4, recall=True, keys=("t1",)),
                  Run(r5, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("recap",
          "總結：[[r1]]find 搵位置，搵唔到就係 npos，一定要檢查；[[r2]]substr 由某個位置切出一段；[[r3]]stoi 字串變數字，to_string 數字變字串；"
          "[[r4]]replace 替換其中一段。",
          BulletCard("今集重點", [("find：搵唔到 → npos，要檢查", "r1"), ("substr(位置, 長度)", "r2"),
                                ("stoi / to_string", "r3"), ("replace(位置, 長度, 新字串)", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一個年月日格式嘅日期，例如二零二六減十一減十四，拆出年、月、日，變做數字印出嚟。"
          "[[next]]下一集，我哋講字元同中文字。多謝收睇，下次見！",
          EndCard("讀入 YYYY-MM-DD 格式嘅日期（例如 2026-11-14），拆出年、月、日，變做數字印出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 77 (syllabus 6.15): virtual destructor 同 final

A FileLog (with a 1000-int vector) owned through std::unique_ptr<Log>. With a plain ~Log() the
real run prints only "~Log": ~FileLog never runs, so its vector is never freed; AddressSanitizer
really reports new-delete-type-mismatch (32 bytes allocated, 8 deleted). virtual ~Log() fixes
it (~FileLog then ~Log). `final` on FileLog makes deriving from it a real error.
Run `python3 video77.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 77
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-15"
FINAL = (CODE / "log.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
V2 = FINAL.replace("final ", "")
V1 = V2.replace("    virtual ~Log()", "    ~Log()").replace("~FileLog() override", "~FileLog()")
SPECIAL = "class Special : public FileLog {};\n\n"
V3 = FINAL.replace("int main", SPECIAL + "int main")
CC = "g++ -std=c++20 -Wall -Wextra log.cpp -o lg"
ASAN = "g++ -g -fsanitize=address log.cpp -o lg"

(c1, r1, ca, ra, clr, c2, r2, clr2, c3, cch, rch) = cpp.session({"log.cpp": V1}, [
    CC, "./lg", ASAN, "./lg", "clear", Write("log.cpp", V2), CC, "./lg", "clear", Write("log.cpp", V3), CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "file\n~Log\n" and c1.code == ca.code == 0, r1.output
assert "new-delete-type-mismatch" in ra.output and "32 bytes" in ra.output and ra.code != 0, ra.output[:500]
assert r2.output == "file\n~FileLog\n~Log\n" and c2.code == 0
assert "cannot derive from 'final' base 'FileLog'" in cpp.visible(c3.output), c3.output[:300]
assert cch.code == 0 and rch.output == "9\n"

SAY = {"virtual": "virtual", "final": "final", "override": "override", "~Log": "Log 解構子", "~FileLog": "FileLog 解構子",
       "FileLog": "File Log", "Log": "Log", "unique_ptr": "unique pointer", "std::unique_ptr<Log>": "unique pointer Log",
       "new-delete-type-mismatch": "new delete type mismatch", "AddressSanitizer": "Address Sanitizer", "ASan": "A San",
       "Special": "Special", "vector": "vector"}

s = Stage({"log.cpp": V1}, title="virtual destructor 同 final", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！用基底類別嘅指標去管一個子類別物件，好常見。但係如果基底嘅解構子唔係 virtual，刪佢嘅時候就會出事。今集講 virtual destructor 同 final。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "virtual ~Log() · final")),
    Scene("goal",
          "今集會講：[[b1]]經基底指標刪除物件；[[b2]]冇 virtual 解構子會點；[[b3]]virtual destructor；[[b4]]final：唔俾再繼承。",
          BulletCard("今集學識", [("經基底指標刪除", "b1"), ("冇 virtual：子類別解構子唔會行", "b2"), ("virtual ~Log()", "b3"),
                                ("final", "b4")])),
    Scene("code",
          "[[log]]Log 有一個 virtual 嘅 write，解構嗰陣印 Log 解構子。[[file]]FileLog 繼承佢，入面有一個一千個 int 嘅 vector。"
          "[[main]]main 用 unique_ptr Log 管住一個 FileLog，離開嗰陣自動 delete。",
          s.scene(Open("log.cpp", at="log"), Mark((5, 13), at="log"), Mark((15, 27), at="file"), Mark(30, at="main"))),
    Scene("run1",
          "[[cc]]編譯運行。[[o]]file 冇問題，但係最後只印咗 Log 解構子！FileLog 嘅解構子冇行過，佢嘅 vector 亦都冇釋放。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1), Note("~FileLog 冇行過！", at="o", where="editor"))),
    Scene("asan",
          "[[cc]]用 address sanitizer 再試。[[o]]佢即刻捉到：new delete type mismatch：[[size]]new 嘅時候係三十二 byte 嘅 FileLog，"
          "delete 嘅時候當咗佢係八 byte 嘅 Log。",
          s.scene(Note(None), Run(ca, at="cc"), Run(ra, at="o"), Scroll(at="o"), Note("new：32 byte 嘅 FileLog\ndelete：當咗係 8 byte 嘅 Log", at="size"))),
    Scene("why",
          "因為 delete 一個 Log 指標，[[plain]]如果解構子唔係 virtual，就同普通函數一樣，只睇指標嘅類型，只叫 Log 嘅解構子。"
          "[[virt]]加 virtual，先會睇真正嘅物件，由 FileLog 開始拆。",
          TableCard("delete 一個 Log*", ["~Log() 係", "會行嘅解構子"], [
              (["普通", "~Log()"], "plain", RED),
              (["virtual", "~FileLog() → ~Log()"], "virt", GREEN),
          ], widths=[1, 1.6], code_cols=(1,), size=42)),
    Scene("fix",
          "[[type]]喺 Log 嘅解構子前面加 virtual，[[ov]]FileLog 嘅解構子加 override。[[cc]]編譯運行：[[o]]先 FileLog 解構子，再 Log 解構子，"
          "同建構嘅次序啱啱相反。",
          s.scene(Note(None), Run(clr, at="type"), Replace("log.cpp", "    ~Log()", "    virtual ~Log()", at="type"),
                  Replace("log.cpp", "~FileLog() {", "~FileLog() override {", at="ov"), Expect("log.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("rule",
          "規則好簡單：[[r]]一個 class 只要有 virtual 函數，即係打算俾人繼承，[[d]]佢嘅解構子就一定要係 virtual。",
          BulletCard("記住", [("有 virtual 函數 → 會俾人繼承", "r"), ("解構子一定要 virtual", "d")])),
    Scene("final",
          "反過嚟，[[type]]如果 FileLog 唔想再俾人繼承，就喺名後面加 final。[[sp]]試吓寫一個 Special 繼承佢。[[cc]]編譯：[[err]]錯誤，"
          "唔可以由一個 final 嘅類別衍生。",
          s.scene(Run(clr2, at="type"), Replace("log.cpp", "class FileLog : public", "class FileLog final : public", at="type"),
                  Type("log.cpp", SPECIAL, before="int main", at="sp"), Expect("log.cpp", V3),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("recap",
          "總結：[[r1]]經基底指標刪除子類別物件，好常見；[[r2]]基底解構子唔係 virtual，子類別嘅解構子就唔會行，資源會漏；"
          "[[r3]]有 virtual 函數，解構子就要 virtual；[[r4]]final 禁止再繼承。",
          BulletCard("今集重點", [("經 Log* 刪除 FileLog", "r1"), ("冇 virtual：~FileLog 唔行", "r2"), ("virtual ~Log()", "r3"),
                                ("final：唔俾再繼承", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 6.14 嘅 Shape 加 virtual destructor，等如 default；將 Square 設為 final；用 new 同 delete 經 Shape 指標試一次。"
          "[[next]]下一集：組合同繼承。多謝收睇，下次見！",
          EndCard("幫 Shape 加 virtual ~Shape() = default;，Square 加 final；Shape* s = new Square{3.0}; 印面積再 delete。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 59 (syllabus 5.8): RAII

work() with new[] and delete[] leaks on its early return (a real LeakSanitizer report for the
n = 5 call); a Buffer struct gets the memory in its constructor and gives it back in its
destructor, which runs on every way out of the function: the run prints "give back" twice and
LeakSanitizer is silent. Run `python3 video5.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 59
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-08"
LEAK = (CODE / "leak.cpp").read_text()
RAII = (CODE / "raii.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
STRUCT = RAII.split("#include <iostream>\n\n")[1].split("void work")[0]
WORK = "void work" + RAII.split("void work")[1].split("int main")[0]
MAIN = "int main" + RAII.split("int main")[1]
SKEL = "#include <iostream>\n\n"
CL = "g++ -std=c++20 -g -fsanitize=address leak.cpp -o leak"
CR = "g++ -std=c++20 -g -fsanitize=address raii.cpp -o raii"

(c1, r1, clr, c2, r2, cch, rch) = cpp.session({"leak.cpp": LEAK, "raii.cpp": RAII}, [
    CL, "./leak", "clear", CR, "./raii",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
leak = cpp.visible(r1.output)
assert "LeakSanitizer: detected memory leaks" in leak and "20 byte(s) leaked" in leak and "leak.cpp:4" in leak, leak[-500:]
assert r2.output == ("work(2):\n  get 2\n  working\n  give back\nwork(5):\n  get 5\n  too big, return early\n  give back\n"), r2.output
assert r2.code == 0 and c1.code == c2.code == cch.code == 0 and rch.output.split() == ["before", "start", "inside", "stop", "after"]

SAY = {"RAII": "R A I I", "delete[]": "delete 中括號", "new": "new", "Buffer": "buffer", "~Buffer": "波浪號 buffer",
       "struct": "struct", "LeakSanitizer": "Leak Sanitizer", "return": "return"}

s = Stage({"leak.cpp": LEAK, "raii.cpp": RAII}, title="RAII：自動還返", split=0.45, code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集發現：new 咗，就一定要記得 delete，好容易漏。今集學 C++ 最重要嘅概念之一：RAII，令資源自動還返。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "建構子攞 · 解構子還")),
    Scene("goal",
          "今集會講：[[b1]]點解提早 return 會漏；[[b2]]struct 嘅建構子同解構子；[[b3]]離開範圍，自動清理。",
          BulletCard("今集學識", [("提早 return：漏咗 delete", "b1"), ("建構子 constructor / 解構子 destructor", "b2"),
                                ("離開範圍：自動清理", "b3")])),
    Scene("leak",
          "[[open]]work 用 new 攞記憶體，最尾 delete。[[early]]但係中間有一個提早 return：n 大過三，就即刻離開。"
          "[[cc]]用 LeakSanitizer 編譯運行：[[o1]]work 二冇問題；[[o2]]work 五，提早返咗，[[rep]]結果漏咗二十個 byte。",
          s.scene(Open("leak.cpp", at="open"), Mark(4, at="open"), Mark((6, 9), at="early"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note("work(5)：return 咗\ndelete[] 冇行到", at="rep", where="editor"))),
    Scene("why",
          "問題係：[[paths]]一個函數有幾多個出口，就要喺每個出口都記住 delete。[[more]]出口一多，或者之後有人加多個 return，就好容易漏。"
          "[[idea]]如果離開嗰陣，會自動還返，就唔使記。",
          TileCard("兩條路，一個 delete", [
              Tile("✅", "n ≤ 3", "行到最尾：有 delete[]", "paths", GREEN),
              Tile("❌", "n > 3", "提早 return：冇 delete[]", "paths", RED),
          ], cols=2, height=330, footer=("離開嗰陣自動還返：就唔使記", "idea"))),
    Scene("struct",
          "[[open]]寫一個 struct 叫 Buffer。[[ctor]]同 struct 同名嘅函數，叫建構子：建立物件嗰陣自動行，喺度 new。"
          "[[dtor]]前面有波浪號嘅，叫解構子：物件消失嗰陣自動行，喺度 delete。6.4 同 6.5 會再詳細講。",
          s.scene(Note(None), Mark(None), Run(clr, at="open"), Open("raii.cpp", mode="empty", at="open"),
                  Type("raii.cpp", SKEL + "".join(STRUCT.splitlines(True)[:2]), at="open", rate=30),
                  Type("raii.cpp", "".join(STRUCT.splitlines(True)[2:6]), at="ctor", rate=34),
                  Type("raii.cpp", "".join(STRUCT.splitlines(True)[6:]), at="dtor", rate=34))),
    Scene("use",
          "[[use]]work 入面，只係開一個 Buffer，再冇 new，亦冇 delete。[[scope]]buf 係局部變數，函數一離開，無論係邊個出口，"
          "佢都會消失，解構子就自動 delete。",
          s.scene(Type("raii.cpp", WORK, at="use", rate=40), Type("raii.cpp", MAIN.rstrip("\n"), rate=50), Expect("raii.cpp", RAII), Mark(16, at="use"))),
    Scene("run",
          "[[cc]]用 LeakSanitizer 編譯運行。[[o1]]work 二：攞、做嘢、還；[[o2]]work 五：攞，提早 return，但係都有還！"
          "[[ok]]LeakSanitizer 冇出聲，一個 byte 都冇漏。",
          s.scene(Mark(None), Run(c2, at="cc"), Run(r2), Note("提早 return：都有 give back", at="o2", where="editor"))),
    Scene("concept",
          "呢個做法叫 RAII：[[get]]攞資源，喺建構子做；[[back]]還資源，喺解構子做；[[auto]]物件一離開範圍，就自動還。"
          "[[every]]其實 vector、string、之後學嘅檔案同 unique_ptr，全部都係用呢個方法。",
          BulletCard("RAII", [("攞資源：建構子", "get"), ("還資源：解構子", "back"), ("離開範圍：自動還", "auto"),
                              ("vector、string、unique_ptr 全部係 RAII", "every")])),
    Scene("recap",
          "總結：[[r1]]手動 delete，每個出口都要記住，好易漏；[[r2]]建構子攞，解構子還；[[r3]]物件離開範圍，解構子自動行；"
          "[[r4]]所以多用 vector 呢啲 RAII 嘅工具，少寫 new 同 delete。",
          BulletCard("今集重點", [("手動 delete：好易漏", "r1"), ("建構子攞，解構子還", "r2"), ("離開範圍：自動行解構子", "r3"),
                                ("多用 RAII，少寫 new / delete", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 Timer struct：建構嗰陣印 start，解構嗰陣印 stop；放佢入一對大括號入面，睇吓幾時印。"
          "[[next]]下一集，我哋學標準庫嘅 RAII 指標：unique_ptr。多謝收睇，下次見！",
          EndCard("寫 struct Timer：建構時印 start，解構時印 stop；放入一對 { } 入面，睇吓幾時印。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 60 (syllabus 5.9): unique_ptr

std::make_unique<Robot>(1) owns a Robot that switches itself off when main ends (no delete);
a->id; copying the unique_ptr is a real "use of deleted function" error; std::move hands the
robot to b and leaves a empty. Run `python3 video5.9.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 60
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-09"
FINAL = (CODE / "uptr.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
STRUCT = "struct Robot" + FINAL.split("struct Robot")[1].split("int main")[0]
BODY = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
HEAD = "#include <iostream>\n#include <memory>\n#include <utility>\n\n"
SKEL = HEAD + "int main() {\n}\n"
S1 = HEAD + STRUCT + "int main() {\n" + "".join(BODY[:2]) + "}\n"
BAD = HEAD + STRUCT + "int main() {\n" + "".join(BODY[:2]) + "    auto b = a;\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra uptr.cpp -o uptr"

(c1, r1, c2, clr, c3, r3, cch, rch) = cpp.session({"uptr.cpp": S1}, [
    CC, "./uptr", Write("uptr.cpp", BAD), CC, "clear", Write("uptr.cpp", FINAL), CC, "./uptr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Robot 1 on\na has robot 1\nRobot 1 off\n", r1.output
assert "use of deleted function" in cpp.visible(c2.output) and c2.code != 0
assert r3.output == "Robot 1 on\na has robot 1\na empty: 1\nb has robot 1\nRobot 1 off\n", r3.output
assert c1.code == c3.code == cch.code == 0 and rch.output.count(" off") == 3

SAY = {"unique_ptr": "unique pointer", "std::make_unique": "S T D make unique", "make_unique": "make unique",
       "std::move": "S T D move", "a->id": "a 箭咀 id", "->": "箭咀", "nullptr": "null pointer", "Robot": "Robot"}

s = Stage({"uptr.cpp": SKEL}, title="unique_ptr", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集自己寫咗一個 RAII 嘅 struct。其實標準庫已經有現成嘅 RAII 指標：unique_ptr。今集學點樣用。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::make_unique · -> · std::move")),
    Scene("goal",
          "今集會講：[[b1]]用 make_unique 建立；[[b2]]用箭咀攞成員；[[b3]]唯一擁有權：唔可以複製；[[b4]]用 std::move 轉讓。",
          BulletCard("今集學識", [("std::make_unique", "b1"), ("p->成員", "b2"), ("唯一擁有：唔可以複製", "b3"), ("std::move：轉讓", "b4")])),
    Scene("robot",
          "[[st]]先寫一個 Robot：建構嗰陣印 on，解構嗰陣印 off，好似上一集嘅 Buffer。",
          s.scene(Open("uptr.cpp", mode="instant"), Type("uptr.cpp", STRUCT, before="int main", at="st", rate=50))),
    Scene("make",
          "[[make]]std::make_unique，角括號入面寫型別 Robot，括號入面係建構子要嘅參數。佢會喺 heap 建立一個 Robot，"
          "交俾 a 管。[[arrow]]用指標攞成員，要用箭咀：a 箭咀 id。[[cc]]編譯運行：[[o]]Robot on，印出 id，最後自動 off，我哋冇寫過 delete。",
          s.scene(Type("uptr.cpp", BODY[0], before="}", last=True, at="make", rate=24),
                  Type("uptr.cpp", BODY[1], before="}", last=True, at="arrow", rate=26), Expect("uptr.cpp", S1),
                  Run(c1, at="cc"), Run(r1))),
    Scene("copy",
          "unique 即係唯一：[[type]]試吓複製一份，auto b 等於 a。[[cc]]編譯：[[err]]出錯，用咗一個被刪除咗嘅函數。"
          "[[why]]因為如果有兩個 unique_ptr 管同一個 Robot，佢哋消失嗰陣就會 delete 兩次，所以複製係禁止嘅。",
          s.scene(Type("uptr.cpp", "    auto b = a;\n", before="}", last=True, at="type"), Expect("uptr.cpp", BAD),
                  Run(c2, at="cc", recall=True), Scroll(at="err"), Note("unique_ptr 唔可以複製：\n唔准兩個主人", at="why", where="editor"))),
    Scene("move",
          "[[move]]但係可以轉讓：std::move(a)，將 Robot 交俾 b，a 就變返空。[[print]]印出 a 係咪空，同埋 b 嘅 Robot。"
          "[[cc]]編譯運行：[[o]]a 係空；b 有一號 Robot；最後 Robot 只會 off 一次。",
          s.scene(Note(None), Run(clr, at="move"), Replace("uptr.cpp", "    auto b = a;\n", BODY[2], at="move"),
                  Type("uptr.cpp", "".join(BODY[3:]), before="}", last=True, at="print", rate=30), Expect("uptr.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("boxes",
          "[[before]]轉讓之前，a 管住個 Robot；[[after]]std::move 之後，b 接手，a 變成 nullptr。[[one]]任何時候，都只有一個主人。",
          BoxesCard("std::move：轉讓擁有權", [
              BoxRow([Box("a", [("Robot 1", "before"), ("nullptr", "after")], "unique_ptr", at="before", color=PURPLE, w=300, key="a"),
                      Box("b", [("", None), ("Robot 1", "after")], "unique_ptr", at="after", color=GREEN, w=300, key="b")], gap=200),
          ], top=CONTENT_TOP + 80, box_h=130, size=46, notes=[("任何時候：只有一個主人", "one")])),
    Scene("compare",
          "比較一下：[[raw]]自己 new 同 delete，要記住喺每個出口還；[[smart]]用 make_unique，就交俾 unique_ptr 管，佢消失嗰陣自動 delete。"
          "[[rule]]所以現代 C++，用 make_unique 代替 new。",
          CodeCompareCard("new 定 make_unique？", [
              Pane("自己管", "Robot* r = new Robot(1);\n// …\ndelete r;   // 唔好漏！", False, "raw"),
              Pane("交俾 unique_ptr", "auto r = std::make_unique<Robot>(1);\n// 自動 delete", True, "smart"),
          ], size=28)),
    Scene("recap",
          "總結：[[r1]]make_unique 建立物件，交俾 unique_ptr 管；[[r2]]用箭咀攞成員；[[r3]]unique_ptr 唔可以複製；"
          "[[r4]]用 std::move 轉讓，佢消失嗰陣自動 delete。",
          BulletCard("今集重點", [("std::make_unique<T>(…)", "r1"), ("p->成員", "r2"), ("唔可以複製", "r3"), ("std::move 轉讓；自動 delete", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個 vector，裝三個 unique_ptr<Robot>，用 push_back 同 make_unique 加入；睇吓程式完嗰陣，三部 Robot 有冇自動 off。"
          "[[next]]下一集，我哋學可以共享嘅 shared_ptr。多謝收睇，下次見！",
          EndCard("整一個 std::vector<std::unique_ptr<Robot>>，用 make_unique 加入三部 Robot；睇吓程式完嗰陣有冇自動 off。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

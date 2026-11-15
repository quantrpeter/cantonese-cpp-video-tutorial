#!/usr/bin/env python3
"""Video 61 (syllabus 5.10): shared_ptr 同 weak_ptr

std::make_shared and use_count really going 2 then 1; Amy and Ben pointing at each other with
shared_ptr are never destroyed (the run prints no "out" at all: a cycle leak); making buddy a
std::weak_ptr breaks the cycle and both really say "out". Run `python3 video5.10.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 61
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-10"
FINAL = (CODE / "pals.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SHARED = FINAL.replace("std::weak_ptr<Person> buddy;", "std::shared_ptr<Person> buddy;")
LINKS = "    auto ben = std::make_shared<Person>(\"Ben\");\n    amy->buddy = ben;\n    ben->buddy = amy;\n"
V1 = SHARED.replace(LINKS, "")
STRUCT = "struct Person" + V1.split("struct Person")[1].split("int main")[0]
COUNT = V1.split("int main() {\n")[1].rsplit("}", 1)[0]
HEAD = "#include <iostream>\n#include <memory>\n#include <string>\n\n"
SKEL = HEAD + "int main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra pals.cpp -o pals"

(c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"pals.cpp": V1}, [
    CC, "./pals", Write("pals.cpp", SHARED), CC, "./pals", "clear", Write("pals.cpp", FINAL), CC, "./pals",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Amy in\ncount: 2\ncount: 1\nAmy out\n", r1.output
assert r2.output == "Amy in\ncount: 2\ncount: 1\nBen in\n", r2.output
assert r3.output == "Amy in\ncount: 2\ncount: 1\nBen in\nBen out\nAmy out\n", r3.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.strip() == "Amy's buddy: Ben"

SAY = {"shared_ptr": "shared pointer", "weak_ptr": "weak pointer", "std::make_shared": "S T D make shared",
       "make_shared": "make shared", "use_count": "use count", "lock()": "lock", "unique_ptr": "unique pointer",
       "Amy": "Amy", "Ben": "Ben", "buddy": "buddy"}

s = Stage({"pals.cpp": SKEL}, title="shared_ptr 同 weak_ptr", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！unique_ptr 只可以有一個主人。如果幾個地方都要共用同一個物件呢？今集學 shared_ptr，同埋佢嘅好拍檔 weak_ptr。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "共享 · use_count · 循環")),
    Scene("goal",
          "今集會講：[[b1]]shared_ptr：幾個主人共享；[[b2]]use_count：計有幾多個主人；[[b3]]互相指住會點；[[b4]]用 weak_ptr 解決。",
          BulletCard("今集學識", [("shared_ptr：共享", "b1"), ("use_count：計主人", "b2"), ("循環引用 → 漏記憶體", "b3"),
                                ("weak_ptr 打破循環", "b4")])),
    Scene("person",
          "[[st]]Person 有個名，同埋一個 buddy，指住佢嘅朋友；建構印 in，解構印 out。[[count]]main 用 make_shared 建立 Amy；"
          "喺一對大括號入面複製一份，印出 use_count；離開之後再印一次。睇吓個數點樣變。",
          s.scene(Open("pals.cpp", mode="instant"), Type("pals.cpp", STRUCT, before="int main", at="st", rate=50),
                  Type("pals.cpp", COUNT, before="}", last=True, at="count", rate=40), Expect("pals.cpp", V1))),
    Scene("run1",
          "[[cc]]編譯運行：[[o1]]Amy in；[[o2]]複製之後，有兩個主人，count 係二；[[o3]]離開大括號，copy 冇咗，剩返一個；"
          "[[o4]]main 完咗，最後一個主人都冇咗，Amy 先至 out。",
          s.scene(Run(c1, at="cc"), Run(r1))),
    Scene("count",
          "shared_ptr 入面有一個計數器：[[a]]多一個主人，就加一；[[b]]少一個，就減一；[[c]]跌到零，即係冇人用，就自動 delete。",
          TableCard("use_count 點樣變？", ["時候", "主人", "use_count"], [
              (["make_shared", "amy", "1"], "a"), (["auto copy = amy;", "amy、copy", "2"], ("a", 0.6)),
              (["離開 { }", "amy", "1"], "b"), (["main 完", "（冇）", "0 → delete"], "c", GREEN),
          ], widths=[1.4, 1.2, 1], code_cols=(0, 2), size=40)),
    Scene("cycle",
          "而家加多個 Ben，[[link]]Amy 嘅 buddy 係 Ben，Ben 嘅 buddy 係 Amy：互相指住。[[cc]]編譯運行：[[o]]Ben in，然後……"
          "冇咗！Amy 同 Ben 都冇 out，冇人 delete 佢哋。",
          s.scene(Type("pals.cpp", LINKS, before="}", last=True, at="link", rate=30), Expect("pals.cpp", SHARED),
                  Run(c2, at="cc", recall=True), Run(r2), Note("冇 out：Amy 同 Ben\n永遠都唔會 delete", at="o", where="editor"))),
    Scene("why",
          "因為 main 完咗之後，[[gone]]amy 同 ben 呢兩個變數冇咗，但係 Amy 仲俾 Ben 嘅 buddy 指住，[[loop]]Ben 又俾 Amy 嘅 buddy 指住："
          "計數永遠跌唔到零，兩個都唔會 delete。呢個叫循環引用。",
          BoxesCard("互相指住：計數永遠係 1", [BoxRow([
              Box("Amy", "count 1", "Person", at="gone", color=RED, w=300, key="amy"),
              Box("Ben", "count 1", "Person", at="gone", color=RED, w=300, key="ben"),
          ], gap=240)], arrows=[("amy", "ben", "loop", RED), ("ben", "amy", ("loop", 0.5), RED)],
              top=CONTENT_TOP + 90, box_h=140, size=48, notes=[("冇人可以令計數變 0：漏記憶體", "loop")])),
    Scene("weak",
          "[[fix]]解決方法：buddy 改用 weak_ptr。weak_ptr 睇住個物件，但係唔算主人，唔會加計數。[[cc]]再運行：[[o]]Ben out，Amy out，兩個都還返。",
          s.scene(Note(None), Run(clr, at="fix"), Replace("pals.cpp", "std::shared_ptr<Person> buddy;", "std::weak_ptr<Person> buddy;", at="fix"),
                  Expect("pals.cpp", FINAL), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("rules",
          "記住：[[u]]一個主人，用 unique_ptr，最常用；[[sh]]真係要共享，先用 shared_ptr；[[w]]只係想睇住、唔想擁有，例如互相指住嘅朋友，就用 weak_ptr。",
          TableCard("三種智能指標", ["", "幾時用"], [
              (["unique_ptr", "一個主人（首選）"], "u"),
              (["shared_ptr", "幾個主人共享，計數到 0 先 delete"], "sh"),
              (["weak_ptr", "睇住，唔擁有，唔加計數：打破循環"], "w"),
          ], widths=[1, 2.4], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]shared_ptr 可以複製，幾個主人共享；[[r2]]use_count 跌到零先 delete；[[r3]]互相用 shared_ptr 指住，會變成循環，永遠唔 delete；"
          "[[r4]]其中一邊用 weak_ptr 就解決。",
          BulletCard("今集重點", [("shared_ptr：共享擁有", "r1"), ("計數到 0 先 delete", "r2"), ("循環引用：永遠唔 delete", "r3"),
                                ("weak_ptr 打破循環", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 weak_ptr 嘅 lock，由 Amy 攞到佢 buddy，印出朋友嘅名。[[next]]下一集係第五章最後一集：未定義行為。多謝收睇，下次見！",
          EndCard("用 amy->buddy.lock() 攞到 Amy 嘅朋友，印出佢個名。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

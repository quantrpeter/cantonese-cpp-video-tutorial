#!/usr/bin/env python3
"""Video 66 (syllabus 6.4): Constructor

A Student constructor with a member initialiser list that also fixes a negative mark (Cat -5
really becomes 0); `Student a;` is a real "no matching function for call to 'Student::Student()'"
once a constructor exists; adding a default constructor fixes it.
Run `python3 video66.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 66
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-04"
FINAL = (CODE / "ctor.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
DEFAULT = "    Student() : name_{\"Unknown\"}, mark_{0} {}\n"
HEAD = "#include <iostream>\n#include <string>\n\n"
CLASS1 = "class Student" + FINAL.replace(DEFAULT, "").split("class Student")[1].split("int main")[0]
BODY = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
MAIN1 = [BODY[1], BODY[2], BODY[4], BODY[5]]
V1 = HEAD + CLASS1 + "int main() {\n" + "".join(MAIN1) + "}\n"
BAD = HEAD + CLASS1 + "int main() {\n" + "".join(BODY) + "}\n"
assert BAD.replace("public:\n", "public:\n" + DEFAULT) == FINAL
SKEL = HEAD + "int main() {\n}\n"
CC = "g++ -std=c++20 -Wall -Wextra ctor.cpp -o ctor"

(c1, r1, c2, clr, c3, r3, cch, rch) = cpp.session({"ctor.cpp": V1}, [
    CC, "./ctor", Write("ctor.cpp", BAD), CC, "clear", Write("ctor.cpp", FINAL), CC, "./ctor",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Ben: 72\nCat: 0\n" and r3.output == "Unknown: 0\nBen: 72\nCat: 0\n"
assert "no matching function for call to 'Student::Student()'" in cpp.visible(c2.output), c2.output[:300]
assert c1.code == c3.code == cch.code == 0 and rch.output.strip() == "1 24"

SAY = {"constructor": "constructor", "Student a;": "Student a", "Student": "Student", "name_": "name 底線",
       "mark_": "mark 底線", "Unknown": "Unknown", "Ben": "Ben", "Cat": "Cat"}

s = Stage({"ctor.cpp": SKEL}, title="Constructor 建構子", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！一個物件一出世，就應該有啱嘅值。今集學 constructor，即係建構子：建立物件嗰陣自動行嘅函數。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "constructor · 初始化列表")),
    Scene("goal",
          "今集會講：[[b1]]帶參數嘅建構子；[[b2]]成員初始化列表；[[b3]]預設建構子；[[b4]]寫咗建構子之後嘅一個陷阱。",
          BulletCard("今集學識", [("帶參數嘅建構子", "b1"), ("初始化列表 : name_{name}", "b2"), ("預設建構子", "b3"),
                                ("寫咗建構子之後嘅陷阱", "b4")])),
    Scene("ctor",
          "[[name]]建構子同 class 同名，冇回傳型別。[[list]]冒號後面係初始化列表：用參數，喺物件一出世就填好每個成員。"
          "[[body]]大括號入面仲可以檢查：分數係負數，就改做零。[[main]]main 用大括號，傳名同分數入去。",
          s.scene(Open("ctor.cpp", mode="instant"), Type("ctor.cpp", CLASS1, before="int main", at="name", rate=70),
                  Mark(6, at="name"), Mark(7, at="list"), Mark((8, 10), at="body"), Mark(None, at="main"),
                  Type("ctor.cpp", "".join(MAIN1), before="}", last=True, at="main", rate=40), Expect("ctor.cpp", V1))),
    Scene("run1",
          "[[cc]]編譯運行：[[o1]]Ben，七十二；[[o2]]Cat 傳咗負五，建構子將佢改咗做零。物件一出世，就保證啱。",
          s.scene(Run(c1, at="cc"), Run(r1))),
    Scene("anatomy",
          "[[n]]名同 class 一樣；[[p]]括號入面係參數；[[l]]冒號後面係初始化列表：每個成員，用大括號填入初始值；[[b]]最後係函數本體。",
          AnatomyCard("建構子", [
              Part("Student", "同 class 同名", BLUE, "n"), Part("(std::string name, int mark)", "參數", PURPLE, "p"),
              Part(" : name_{name}, mark_{mark}", "初始化列表", GREEN, "l"), Part(" { … }", "本體", AMBER, "b"),
          ], size=46)),
    Scene("nodefault",
          "而家想建立一個乜都唔傳嘅學生：[[type]]Student a。[[cc]]編譯：[[err]]出錯！搵唔到一個唔使參數嘅建構子。"
          "[[why]]原來你自己寫咗任何建構子，編譯器就唔會再幫你整嗰個預設嘅。",
          s.scene(Type("ctor.cpp", BODY[0], after="int main() {\n", at="type"), Type("ctor.cpp", BODY[3], after=BODY[2]),
                  Expect("ctor.cpp", BAD), Run(c2, at="cc", recall=True), Scroll(at="err"),
                  Note("寫咗建構子：\n冇咗預設建構子", at="why", where="editor"))),
    Scene("default",
          "[[add]]自己加一個預設建構子：冇參數，名係 Unknown，分數係零。[[cc]]再編譯運行，[[o]]Unknown 零，Ben 七十二，Cat 零。",
          s.scene(Note(None), Run(clr, at="add"), Type("ctor.cpp", DEFAULT, after="public:\n", at="add"), Expect("ctor.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("table",
          "[[a]]Student a，冇參數，用預設建構子；[[b]]Student b 大括號 Ben 七十二，用帶參數嗰個。[[rule]]編譯器睇參數，揀啱嘅建構子，同 3.7 嘅多載一樣。",
          TableCard("用邊個建構子？", ["寫法", "用嘅建構子"], [
              (["Student a;", "Student()"], "a"), (["Student b{\"Ben\", 72};", "Student(std::string, int)"], "b"),
          ], widths=[1.3, 1.4], code_cols=(0, 1), size=42, note=("睇參數揀建構子：同多載一樣", "rule"))),
    Scene("recap",
          "總結：[[r1]]建構子同 class 同名，冇回傳型別，建立物件嗰陣自動行；[[r2]]用初始化列表填成員；[[r3]]寫咗建構子，就要自己寫預設建構子；"
          "[[r4]]建構子可以檢查，保證物件一出世就啱。",
          BulletCard("今集重點", [("同 class 同名，自動行", "r1"), ("初始化列表 : a_{a}", "r2"), ("要自己寫預設建構子", "r3"),
                                ("一出世就保證啱", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 Rectangle class：預設係一乘一，亦可以傳闊同高；加一個 area 函數計面積。"
          "[[next]]下一集：解構子 destructor。多謝收睇，下次見！",
          EndCard("寫 class Rectangle：預設 1 × 1，亦可以 Rectangle r{4, 6}；加成員函數 area()。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

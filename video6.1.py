#!/usr/bin/env python3
"""Video 63 (syllabus 6.1): struct

Two parallel vectors versus one struct Student; the missing semicolon after the struct is a real
"expected ';' after struct definition" error; aggregate initialisation, member access with a
dot, changing a member, and a vector<Student>. Run `python3 video6.1.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 63
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-01"
FINAL = (CODE / "student.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
HEAD = "#include <iostream>\n#include <string>\n#include <vector>\n\n"
STRUCT = "struct Student {\n    std::string name;\n    int mark;\n};\n\n"
BODY = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
SKEL = HEAD + "int main() {\n}\n"
NOSEMI = HEAD + STRUCT.replace("};", "}") + "int main() {\n" + "".join(BODY[:3]) + "}\n"
V1 = HEAD + STRUCT + "int main() {\n" + "".join(BODY[:3]) + "}\n"
CC = "g++ -std=c++20 -Wall -Wextra student.cpp -o stu"

(c0, c1, r1, clr, c2, r2, cch, rch) = cpp.session({"student.cpp": NOSEMI}, [
    CC, Write("student.cpp", V1), CC, "./stu", "clear", Write("student.cpp", FINAL), CC, "./stu",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "expected ';' after struct definition" in cpp.visible(c0.output), c0.output
assert r1.output == "Amy: 85\n" and r2.output == "Amy: 85\nBen: 77\nAmy 85\nBen 77\nCat 91\n", r2.output
assert c1.code == c2.code == cch.code == 0 and rch.output.strip() == "Emma (474)"

SAY = {"struct": "struct", "Student": "Student", "a.name": "a 點 name", "a.mark": "a 點 mark", "b.mark": "b 點 mark",
       "Amy": "Amy", "Ben": "Ben", "Cat": "Cat"}

s = Stage({"student.cpp": SKEL}, title="struct", code_px=24)

scenes = [
    Scene("intro",
          "歡迎嚟到第六章：物件導向！第一步係 struct：將有關係嘅資料，包埋一齊變成一個新型別。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "struct · {} 初始化 · .")),
    Scene("goal",
          "今集會講：[[b1]]定義一個 struct；[[b2]]用大括號建立；[[b3]]用點號攞成員；[[b4]]用 vector 裝好多個。",
          BulletCard("今集學識", [("定義 struct", "b1"), ("Student a{\"Amy\", 85};", "b2"), ("a.name、a.mark", "b3"),
                                ("vector<Student>", "b4")])),
    Scene("why",
          "如果學生嘅名同分數分開兩個 vector 裝，[[bad]]加加減減，好容易對唔齊，第三個名配咗第四個分數。"
          "[[good]]用 struct，一個學生嘅名同分數永遠喺埋一齊。",
          CodeCompareCard("兩個 vector 定一個 struct？", [
              Pane("分開裝", "std::vector<std::string> names;\nstd::vector<int> marks;\n// names[2] 配 marks[2]？", False, "bad"),
              Pane("struct", "struct Student {\n    std::string name;\n    int mark;\n};", True, "good"),
          ], size=30)),
    Scene("define",
          "[[type]]struct Student，大括號入面係佢嘅成員：一個名，一個分數。[[use]]main 入面建立 Amy，印出佢嘅名同分數。"
          "[[cc]]編譯：[[err]]出錯！struct 定義之後，要有分號。呢個好容易漏。",
          s.scene(Open("student.cpp", mode="instant"), Type("student.cpp", STRUCT.replace("};", "}"), before="int main", at="type", rate=30),
                  Type("student.cpp", "".join(BODY[:3]), before="}", last=True, at="use", rate=34), Expect("student.cpp", NOSEMI),
                  Run(c0, at="cc"), Note("struct 收尾：}; 要有分號", at="err", where="editor"))),
    Scene("fix",
          "[[fix]]加返分號，呢個係新手最常漏嘅地方。[[cc]]編譯運行，[[o]]Amy，八十五。",
          s.scene(Note(None), Type("student.cpp", ";", after="    int mark;\n}", at="fix"), Expect("student.cpp", V1),
                  Run(c1, at="cc", recall=True), Run(r1))),
    Scene("boxes",
          "[[init]]Student a，大括號入面嘅值，按次序放入成員：Amy 放入 name，八十五放入 mark。[[dot]]a 點 name，就係攞 a 入面嘅 name。",
          BoxesCard("Student a{\"Amy\", 85};", [BoxRow([
              Box("a.name", "\"Amy\"", "std::string", at="init", w=320), Box("a.mark", "85", "int", at=("init", 0.5), color=AMBER, w=260),
          ], label="a", gap=0, at="init")], top=CONTENT_TOP + 90, box_h=130, size=56,
              notes=[("a.name：a 入面嘅 name", "dot")])),
    Scene("more",
          "[[set]]成員可以改：Ben 加五分。[[vec]]struct 都可以放入 vector：最後一個直接用大括號建立。[[loop]]range-based for 逐個印出。"
          "[[cc]]編譯運行，[[o]]Ben 變咗七十七，三個學生都印晒出嚟。",
          s.scene(Run(clr, at="set"), Type("student.cpp", "".join(BODY[3:5]), before="}", last=True, at="set", rate=34),
                  Type("student.cpp", BODY[5], before="}", last=True, at="vec", rate=30),
                  Type("student.cpp", "".join(BODY[6:]), before="}", last=True, at="loop", rate=34), Expect("student.cpp", FINAL),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("recap",
          "總結：[[r1]]struct 將有關係嘅資料包埋一齊，變成新型別；[[r2]]定義最尾要有分號；[[r3]]用大括號按次序初始化，用點號攞成員；"
          "[[r4]]struct 可以放入 vector。下一集，我哋喺佢入面加埋函數。",
          BulletCard("今集重點", [("struct：自己嘅型別", "r1"), ("定義收尾：};", "r2"), ("{\"Amy\", 85}；a.name", "r3"),
                                ("vector<Student>", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個 struct Book，有書名、作者同頁數，用 vector 裝三本書，印出頁數最多嗰本。"
          "[[next]]下一集：class 同成員函數。多謝收睇，下次見！",
          EndCard("整一個 struct Book（書名、作者、頁數），用 vector 裝三本書，印出頁數最多嗰本。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

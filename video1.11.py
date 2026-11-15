#!/usr/bin/env python3
"""Video 17 (syllabus 1.11): std::string 入門

cin >> name stops at the space in "Chan Tai Man"; std::getline reads the whole line; + joins
strings, size() and [] (shown as boxes with indexes); reading an age with cin first makes
getline read an empty line, for real; std::cin >> std::ws fixes it.
Run `python3 video17.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 17
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-11"
FINAL = (CODE / "name.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
AGE = "    int age{};\n    std::cout << \"Age: \";\n    std::cin >> age;\n"
OPS = ("    std::string hi = \"Hello, \" + name + \"!\";\n    std::cout << hi << '\\n';\n"
       "    std::cout << name.size() << '\\n';\n    std::cout << name[0] << '\\n';\n")
OLD_PRINT = "    std::cout << \"Hello, \" << name << \"!\\n\";\n"
V4 = FINAL.replace("std::cin >> std::ws, name", "std::cin, name")
V3 = V4.replace(AGE, "")
V2 = V3.replace(OPS, OLD_PRINT)
V1 = V2.replace("std::getline(std::cin, name);", "std::cin >> name;")
CC = "g++ -std=c++20 -Wall -Wextra name.cpp -o name"
WHO = "Chan Tai Man"

(c1, r1, c2, r2, c3, r3, clr, c4, r4, c5, r5, cch, rch) = cpp.session({"name.cpp": V1}, [
    CC, Input("./name", [WHO]),
    Write("name.cpp", V2), CC, Input("./name", [WHO]),
    Write("name.cpp", V3), CC, Input("./name", [WHO]),
    Write("name.cpp", V4), "clear", CC, Input("./name", ["13", WHO]),
    Write("name.cpp", FINAL), CC, Input("./name", ["13", WHO]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", [WHO]),
], refresh=opts.fresh_runs, cols=48)
assert r1.output.endswith("Hello, Chan!\n") and r2.output.endswith(f"Hello, {WHO}!\n")
assert r3.output.endswith(f"Hello, {WHO}!\n{len(WHO)}\nC\n"), r3.output
assert "Hello, !\n0\n" in r4.output and WHO not in r4.output, r4.output
assert r5.output.endswith(f"Hello, {WHO}!\n{len(WHO)}\nC\n") and rch.output.endswith(f"{len(WHO)}\nC\nn\n")
assert all(r.code == 0 for r in (c1, c2, c3, c4, c5, cch))

SAY = {"std::string": "S T D string", "std::getline": "S T D get line", "getline": "get line",
       "std::cin >> std::ws": "S T D see in 兩個大過號 S T D W S", "std::ws": "S T D W S", "ws": "W S",
       "cin >>": "see in 兩個大過號", "size": "size", "Chan Tai Man": "Chan Tai Man"}

s = Stage({"name.cpp": V1}, title="std::string 入門")

scenes = [
    Scene("intro",
          "歡迎返嚟！之前我哋處理嘅都係數字。今集開始處理文字：std::string，即係字串。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::string · getline · size")),
    Scene("goal",
          "今集會講：[[b1]]點樣用字串；[[b2]]用 getline 讀成行；[[b3]]用加號接駁字串、size 同中括號；"
          "[[b4]]仲有 cin 同 getline 撈埋用嘅陷阱。",
          BulletCard("今集學識", [("std::string 字串", "b1"), ("getline：讀成行", "b2"),
                                ("+、size()、[]", "b3"), ("cin 同 getline 嘅陷阱", "b4")])),
    Scene("v1",
          "[[inc]]用字串，要 include string。[[decl]]std::string name 宣告一個字串，一開始係空嘅。"
          "[[cin]]同數字一樣，可以用 cin 讀入，[[pr]]再印出 Hello 同個名。",
          s.scene(Open("name.cpp", at="inc"), Mark(2, at="inc"), Mark(5, at="decl"), Mark(7, at="cin"), Mark(8, at="pr"))),
    Scene("run1",
          "[[cc]]編譯運行。[[type]]輸入全名 Chan Tai Man，撳 Enter。[[out]]但係，佢只印出 Chan！其餘嘅名去咗邊？",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1, keys=("type",)), Note("得返 Chan？", at="out", where="editor"))),
    Scene("getline",
          "記得 1.4 講過：cin >> 遇到空格就會停，空格只係用嚟分隔。[[fix]]想讀成行，就要用 std::getline："
          "佢會一直讀到 Enter 為止，包埋中間嘅空格。[[cc]]再編譯運行，同樣輸入全名，[[out]]今次讀到成個全名：Hello, Chan Tai Man!",
          s.scene(Note(None), Replace("name.cpp", "std::cin >> name;", "std::getline(std::cin, name);", at="fix"),
                  Expect("name.cpp", V2), Run(c2, at="cc", recall=True), Run(r2, recall=True, keys=(("cc", 3.0),)))),
    Scene("ops",
          "字串可以做唔少嘢。[[plus]]用加號，可以將幾個字串駁埋一齊，放入 hi，再印出嚟；[[size]]size 話你知有幾多個字元；"
          "[[idx]]中括號加位置，就攞到其中一個字元。",
          s.scene(Replace("name.cpp", OLD_PRINT, "", at="plus"),
                  Type("name.cpp", OPS.splitlines(True)[0], before="}", last=True, rate=24),
                  Type("name.cpp", OPS.splitlines(True)[1], before="}", last=True, rate=24),
                  Type("name.cpp", OPS.splitlines(True)[2], before="}", last=True, at="size", rate=24),
                  Type("name.cpp", OPS.splitlines(True)[3], before="}", last=True, at="idx", rate=24), Expect("name.cpp", V3))),
    Scene("ops_run",
          "[[cc]]編譯運行，[[type]]再輸入一次全名。[[out]]第一行係 Hello, Chan Tai Man!；第二行係十二；第三行係 C。",
          s.scene(Run(c3, at="cc", recall=True), Run(r3, recall=True, keys=("type",)))),
    Scene("boxes",
          "用盒嚟睇：[[cells]]字串就係一格一格嘅字元。[[size]]Chan Tai Man 有十二格，空格都計埋，所以 size 係十二。"
          "[[idx]]位置由零開始數，所以中括號零，就係第一個字元 C；最後一格係十一。",
          BoxesCard("name 入面", [BoxRow([Box("", ch if ch != " " else "␣", str(i), at="cells",
                                             color=AMBER if i == 0 else BLUE) for i, ch in enumerate(WHO)], gap=0)],
                    top=CONTENT_TOP + 80, box_h=110, size=50,
                    notes=[(f"name.size() 係 {len(WHO)}：空格都計", "size"), ("name[0] 係 'C'：位置由 0 開始數", "idx")])),
    Scene("trap",
          "最後一個陷阱。[[type]]喺讀名之前，先用 cin 讀年齡。[[cc]]編譯運行，[[age]]輸入十三，撳 Enter，"
          "[[out]]程式完全唔等我哋打名，就印咗 Hello 同一個空嘅名！",
          s.scene(Type("name.cpp", AGE, after="int main() {\n", at="type"), Expect("name.cpp", V4),
                  Run(clr, at="cc"), Run(c4, recall=True), Run(r4, recall=True, keys=("age",)),
                  Note("冇等我哋打名！\nname 係空嘅，size 係 0", at="out", where="editor"))),
    Scene("buffer",
          "點解？[[keys]]我哋打嘅係一、三，同埋 Enter 嘅換行字元。[[cin]]cin >> age 讀走一同三，[[left]]換行字元仲留喺度；"
          "[[gl]]getline 一嚟就見到換行，以為讀完一行，所以讀到一個空字串。",
          BoxesCard("輸入入面有乜？", [BoxRow([
              Box("", "'1'", "cin 讀走", at="keys", w=200), Box("", "'3'", "cin 讀走", at="keys", w=200),
              Box("", "'\\n'", "留低咗！", at="keys", color=RED, w=200)], gap=0)],
              top=CONTENT_TOP + 80, box_h=130, size=56,
              notes=[("cin >> age 讀走 1 同 3", "cin"), ("換行字元 '\\n' 仲留喺度", "left"),
                     ("getline 一見到 '\\n' 就停：讀到空字串", "gl")])),
    Scene("fix",
          "解決方法：[[fix]]喺 getline 入面，用 std::cin >> std::ws。ws 會先跳過所有空白，包括嗰個換行，先至開始讀。"
          "[[cc]]再編譯運行，輸入十三，再輸入全名。[[out]]今次程式有等我哋打名，結果正常晒。",
          s.scene(Note(None), Replace("name.cpp", "std::cin, name", "std::cin >> std::ws, name", at="fix"),
                  Expect("name.cpp", FINAL), Run(c5, at="cc", recall=True), Run(r5, recall=True))),
    Scene("recap",
          "總結：[[r1]]std::string 用嚟裝文字；[[r2]]cin >> 讀到空格就停，讀成行要用 getline；[[r3]]加號接駁，size 數字元，"
          "中括號由零開始；[[r4]]cin 之後用 getline，記得用 std::ws 跳過換行。",
          BulletCard("今集重點", [("std::string 裝文字", "r1"), ("讀成行：std::getline", "r2"),
                                ("+ 接駁；size()；[0] 由 0 開始", "r3"), ("cin 之後 getline：用 std::cin >> std::ws", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入你嘅全名，印出佢有幾多個字元，同埋第一個同最後一個字元。提示：最後一個嘅位置係 size 減一。"
          "[[next]]下一集係第一章嘅小項目：BMI 計算機。多謝收睇，下次見！",
          EndCard("讀入你嘅全名，印出佢有幾多個字元，同埋第一個同最後一個字元。提示：最後一個嘅位置係 size() - 1。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

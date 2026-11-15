#!/usr/bin/env python3
"""Video 78 (syllabus 6.16): 組合 vs 繼承

Car : public Engine really works ("engine starts / car drives") but also lets car.start() and
repair(car) compile: the run really prints "repairing an engine" for a whole car. A Car has an
Engine, it is not one: with an Engine member instead, both lines become real errors ("has no
member named 'start'", "invalid initialization of reference of type 'const Engine&'").
Run `python3 video78.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 78
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-16"
FINAL = (CODE / "car.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
WEIRD = "    car.start();\n    repair(car);\n"
REPAIR = "void repair" + FINAL.split("void repair")[1].split("int main")[0]
MEMBER = "\nprivate:\n    Engine engine_;\n"
E = FINAL.replace("    car.drive();\n", "    car.drive();\n" + WEIRD)
V1 = E.replace("class Car {", "class Car : public Engine {").replace("        engine_.start();", "        start();").replace(MEMBER, "")
V0 = V1.replace(WEIRD, "").replace(REPAIR, "")
CC = "g++ -std=c++20 -Wall -Wextra car.cpp -o car"

(c0, r0, clr, c1, r1, clr2, c2, clr3, c3, r3, cch, rch) = cpp.session({"car.cpp": V0}, [
    CC, "./car", "clear", Write("car.cpp", V1), CC, "./car", "clear", Write("car.cpp", E), CC, "clear", Write("car.cpp", FINAL), CC, "./car",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r0.output == "engine starts\ncar drives\n" == r3.output and r1.output == r0.output + "engine starts\nrepairing an engine\n"
err = cpp.visible(c2.output)
assert "'class Car' has no member named 'start'" in err and "invalid initialization of reference of type 'const Engine&'" in err, err
assert c0.code == c1.code == c3.code == cch.code == 0 and rch.output == "engine starts\nradio plays\ncar drives\n"

SAY = {"is a": "is a", "has a": "has a", "Engine": "Engine", "Car": "Car", "engine_": "engine 底線", "repair": "repair",
       "car.start()": "car 點 start", "start()": "start", "public Engine": "public Engine", "Radio": "Radio", "Dog": "Dog", "Animal": "Animal"}

s = Stage({"car.cpp": V0}, title="組合 vs 繼承", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！學咗繼承，好容易見到乜都想繼承。一架車要用引擎，咁 Car 係咪應該繼承 Engine？今集比較組合同繼承。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "is a · has a")),
    Scene("goal",
          "今集會講：[[b1]]用錯繼承會點；[[b2]]is a 定 has a；[[b3]]用成員嚟組合；[[b4]]幾時揀邊樣。",
          BulletCard("今集學識", [("用錯繼承", "b1"), ("is a vs has a", "b2"), ("組合：用成員", "b3"), ("幾時揀邊樣", "b4")])),
    Scene("inherit",
          "[[open]]Engine 識 start。[[car]]Car 繼承 Engine，drive 嘅時候先 start，再開車。[[cc]]main 整一架車，開車。編譯運行：[[o]]engine starts，car drives。好似冇問題，但係真係啱嗎？",
          s.scene(Open("car.cpp", at="open"), Mark((3, 8), at="open"), Mark((10, 16), at="car"), Mark(None, at="cc"), Run(c0, at="cc"), Run(r0))),
    Scene("weird",
          "[[rep]]但係加一個 repair 函數，專門修引擎。[[main]]main 入面，可以直接叫車 start，仲可以將成架車交去修引擎。[[cc]]編譯運行：[[o]]全部都得！"
          "一架車俾人當咗係引擎，攞咗去修引擎。設計上呢個係錯嘅。",
          s.scene(Run(clr, at="rep"), Type("car.cpp", REPAIR, before="int main", at="rep"),
                  Type("car.cpp", WEIRD, after="    car.drive();\n", at="main"), Expect("car.cpp", V1),
                  Run(c1, at="cc", recall=True), Run(r1), Note("成架車當咗係引擎？", at="o", where="editor"))),
    Scene("isa",
          "用一句說話測試：[[dog]]狗係一種動物？係，所以 Dog 繼承 Animal。[[car]]車係一種引擎？唔係！車係有一個引擎。[[rule]]is a 用繼承，has a 用組合。",
          TableCard("is a 定 has a？", ["句子", "啱唔啱", "用"], [
              (["狗係一種動物", "啱", "繼承"], "dog", GREEN),
              (["車係一種引擎", "唔啱", "—"], "car", RED),
              (["車有一個引擎", "啱", "組合"], "rule", GREEN),
          ], widths=[1.4, 0.8, 0.8], code_cols=(), size=42)),
    Scene("compose",
          "[[type]]改用組合：Car 唔再繼承 Engine，[[mem]]而係有一個 Engine 成員，[[call]]drive 就叫 engine 底線點 start。"
          "[[cc]]編譯：[[err]]兩個錯：車冇 start，同埋車唔可以當引擎傳俾 repair。編譯器幫我哋擋住咗。",
          s.scene(Note(None), Run(clr2, at="type"), Replace("car.cpp", "class Car : public Engine {", "class Car {", at="type"),
                  Type("car.cpp", MEMBER, after="        std::cout << \"car drives\\n\";\n    }\n", at="mem"),
                  Replace("car.cpp", "        start();", "        engine_.start();", at="call"), Expect("car.cpp", E),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("clean",
          "[[del]]刪走嗰兩句。[[cc]]再編譯運行：[[o]]engine starts，car drives，結果一樣，但係 Engine 而家收埋喺 Car 入面，外面掂唔到。",
          s.scene(Run(clr3, at="del"), Replace("car.cpp", WEIRD, "", at="del"), Expect("car.cpp", FINAL), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("parts",
          "組合嘅好處：[[car]]Car 由零件砌成：[[eng]]引擎，[[more]]第日加收音機、輪胎，都係加成員；[[hide]]零件收喺 private，外面只見到 drive。",
          BoxesCard("Car 有乜？", [
              BoxRow([Box("Car", "drive()", "外面只見到呢個", at="car", color=BLUE, w=420, key="c")]),
              BoxRow([Box("engine_", "Engine", "private", at="eng", color=PURPLE, w=260, key="e"),
                      Box("radio_", "Radio", "第日加", at="more", color=GREEN, w=260, key="r")], gap=80),
          ], arrows=[("c", "e", "eng", PURPLE), ("c", "r", "more", GREEN)], notes=[("零件收埋：private 成員", "hide")],
              top=CONTENT_TOP + 10, row_h=320, box_h=110, size=40)),
    Scene("recap",
          "總結：[[r1]]係一種，用繼承；[[r2]]有一個，用組合；[[r3]]組合就係將另一個物件做成員；[[r4]]唔肯定嘅時候，優先用組合。",
          BulletCard("今集重點", [("is a → 繼承", "r1"), ("has a → 組合", "r2"), ("組合：物件做成員", "r3"), ("唔肯定：優先組合", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 Car 加一個 Radio 成員，drive 嘅時候引擎起動之後播收音機。[[next]]下一集：enum class。多謝收睇，下次見！",
          EndCard("加 class Radio（play() 印 radio plays），做 Car 嘅成員；drive() 先 start 引擎，再 play。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

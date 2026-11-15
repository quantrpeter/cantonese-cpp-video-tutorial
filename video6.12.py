#!/usr/bin/env python3
"""Video 74 (syllabus 6.12): 繼承

Animal → Dog. Animal alone really prints "Animal Kitty / Kitty eats". Dog : public Animal reuses
eat() and adds bark(), but reading name_ while it is private is a real "is private within this
context" error; protected fixes it. The real run shows the Animal part is built before the Dog
part. Run `python3 video74.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 74
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-12"
FINAL = (CODE / "animal.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
DOG = "class Dog" + FINAL.split("class Dog")[1].split("int main")[0]
MAIN_D = "    Dog d{\"Lucky\"};\n    d.eat();\n    d.bark();\n"
MAIN_A = "    Animal a{\"Kitty\"};\n    a.eat();\n"
BAD = FINAL.replace("protected:", "private:")
V1 = BAD.replace(DOG, "").replace(MAIN_D, MAIN_A)
CC = "g++ -std=c++20 -Wall -Wextra animal.cpp -o ani"

(c1, r1, clr, c2, clr2, c3, r3, cch, rch) = cpp.session({"animal.cpp": V1}, [
    CC, "./ani", "clear", Write("animal.cpp", BAD), CC, "clear", Write("animal.cpp", FINAL), CC, "./ani",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "Animal Kitty\nKitty eats\n", r1.output
assert "is private within this context" in cpp.visible(c2.output), c2.output[:400]
assert r3.output == "Animal Lucky\nDog Lucky\nLucky eats\nLucky: Woof!\n", r3.output
assert c1.code == c3.code == cch.code == 0 and rch.output == "Animal Kitty\nCat Kitty\nKitty eats\nKitty: Meow!\n"

SAY = {"public Animal": "public Animal", "protected": "protected", "private": "private", "public": "public",
       "Animal{name}": "Animal 大括號 name", "name_": "name 底線", "Dog": "Dog", "Animal": "Animal", "bark": "bark", "eat": "eat",
       "Woof": "woof", "Lucky": "Lucky", "Kitty": "Kitty"}

s = Stage({"animal.cpp": V1}, title="繼承", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！狗係一種動物：動物識食嘢，狗都識；但係狗仲識吠。唔想將動物嘅嘢再寫一次，就要用繼承。今集由 Animal 去到 Dog。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "Animal → Dog · protected")),
    Scene("goal",
          "今集會講：[[b1]]點樣寫一個衍生類別；[[b2]]佢繼承咗乜；[[b3]]protected；[[b4]]建構嘅次序。",
          BulletCard("今集學識", [("class Dog : public Animal", "b1"), ("繼承成員函數同資料", "b2"), ("protected", "b3"),
                                ("建構次序：先基底，後衍生", "b4")])),
    Scene("animal",
          "[[open]]Animal 有個名，建構嘅時候印一句，[[eat]]仲有一個 eat 函數。[[cc]]main 整一隻叫 Kitty 嘅動物，叫佢食嘢。編譯運行：[[o]]先印 Animal Kitty，再印 Kitty eats。",
          s.scene(Open("animal.cpp", at="open"), Mark((6, 8), at="open"), Mark((9, 11), at="eat"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("dog",
          "[[type]]寫 Dog，冒號 public Animal：Dog 係一種 Animal。[[ctor]]Dog 嘅建構子，要先叫 Animal 嘅建構子，將名傳上去。"
          "[[bark]]再加一個 Animal 冇嘅 bark。",
          s.scene(Run(clr, at="type"), Type("animal.cpp", DOG, before="int main", at="type", rate=60),
                  Mark(17, at="type"), Mark(19, at="ctor"), Mark((22, 24), at="bark"))),
    Scene("main",
          "[[main]]main 改做整一隻叫 Lucky 嘅 Dog，呼叫 eat 同 bark。eat 係由 Animal 繼承落嚟嘅。[[cc]]編譯：[[err]]出錯！name 底線係 private。",
          s.scene(Mark(None), Replace("animal.cpp", MAIN_A, MAIN_D, at="main"), Expect("animal.cpp", BAD),
                  Run(c2, at="cc", recall=True), Scroll(at="err"))),
    Scene("protected",
          "[[why]]private 嘅成員，連子類別都睇唔到。[[fix]]將 private 改做 protected：外面仍然睇唔到，但係子類別睇得到。",
          s.scene(Note("private：連 Dog 都睇唔到", at="why", where="editor"), Note(None, at="fix"),
                  Replace("animal.cpp", "private:", "protected:", at="fix"), Expect("animal.cpp", FINAL), Mark(13, at="fix"))),
    Scene("run",
          "[[cc]]再編譯運行。[[o]]睇吓次序：先印 Animal Lucky，再印 Dog Lucky。即係先建好 Animal 嗰部分，再建 Dog 自己。跟住 eat 同 bark 都得。",
          s.scene(Mark(None), Run(clr2, at="cc"), Run(c3, recall=True), Run(r3))),
    Scene("layers",
          "[[base]]一隻 Dog 入面，包住一個 Animal 嘅部分：名同 eat；[[derived]]外面再加 Dog 自己嘅 bark。[[order]]建構由內到外：先 Animal，後 Dog。",
          BoxesCard("Dog 入面有乜？", [
              BoxRow([Box("Animal 部分", "name_ · eat()", "基底類別", at="base", color=BLUE, w=420, key="a")], label="① 先建"),
              BoxRow([Box("Dog 自己", "bark()", "衍生類別", at="derived", color=GREEN, w=420, key="d")], label="② 後建"),
          ], arrows=[("a", "d", "order", AMBER)], top=CONTENT_TOP + 20, row_h=250, box_h=110, size=44)),
    Scene("access",
          "三種存取：[[pub]]public 邊個都用得；[[pro]]protected 自己同子類別用得；[[pri]]private 只有自己用得。",
          TableCard("邊個睇得到？", ["存取", "class 自己", "子類別", "外面"], [
              (["public", "得", "得", "得"], "pub"),
              (["protected", "得", "得", "唔得"], "pro", AMBER),
              (["private", "得", "唔得", "唔得"], "pri"),
          ], widths=[1.2, 1, 1, 1], code_cols=(0,), size=40)),
    Scene("recap",
          "總結：[[r1]]class Dog 冒號 public Animal，Dog 就有晒 Animal 嘅成員；[[r2]]子類別嘅建構子，要先叫基底嘅建構子；"
          "[[r3]]protected 俾子類別用；[[r4]]建構先基底，後衍生。",
          BulletCard("今集重點", [("class Dog : public Animal", "r1"), ("Dog(...) : Animal{name}", "r2"), ("protected：子類別睇得到", "r3"),
                                ("先建 Animal，後建 Dog", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個 Cat 類別，識 meow，整一隻 Kitty，叫佢食嘢同 meow。[[next]]下一集：virtual 同多型。多謝收睇，下次見！",
          EndCard("加 class Cat : public Animal，有 meow()；整一隻 Kitty，呼叫 eat() 同 meow()。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 75 (syllabus 6.13): virtual 同多型

talk(const Animal&) really prints "..." for both a Dog and a Cat until Animal::speak() is
virtual. Then the Dog barks but the Cat, whose speak() forgot const, is still "..." (g++ really
warns it was hidden). Adding override turns that into a real "marked 'override', but does not
override" error; with const the run is Woof! Meow! and a base pointer works too.
Run `python3 video6.13.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 75
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-13"
FINAL = (CODE / "speak.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
PTR = "    const Animal* p = &c;\n    p->speak();\n"
CAT_OK = "class Cat : public Animal {\npublic:\n    void speak() const override"
V3 = FINAL.replace(CAT_OK, CAT_OK.replace(" const override", " override")).replace(PTR, "")
V2 = V3.replace(" override", "")
V1 = V2.replace("virtual ", "")
CC = "g++ -std=c++20 -Wall -Wextra speak.cpp -o sp"

(c1, r1, clr, c2, r2, clr2, c3, clr3, c4, r4, cch, rch) = cpp.session({"speak.cpp": V1}, [
    CC, "./sp", "clear", Write("speak.cpp", V2), CC, "./sp", "clear", Write("speak.cpp", V3), CC,
    "clear", Write("speak.cpp", FINAL), CC, "./sp",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "...\n...\n" and r2.output == "Woof!\n...\n" and r4.output == "Woof!\nMeow!\nMeow!\n"
assert "was hidden" in cpp.visible(c2.output) and "marked 'override', but does not override" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == cch.code == 0 and c3.code != 0 and rch.output == "Woof!\nMoo!\nWoof!\n"

SAY = {"virtual": "virtual", "override": "override", "speak()": "speak", "speak": "speak", "talk": "talk", "Animal&": "Animal reference",
       "const Animal&": "const Animal reference", "Animal*": "Animal 指標", "p->speak()": "p 箭咀 speak", "Woof": "woof", "Meow": "meow",
       "Dog": "Dog", "Cat": "Cat", "Animal": "Animal", "const": "const", "hidden": "hidden"}

s = Stage({"speak.cpp": V1}, title="virtual 同多型", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集 Dog 繼承咗 Animal。如果手上只係得一個 Animal reference，叫佢 speak，狗會唔會吠？今集學 virtual，同埋多型。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "virtual · override · 多型")),
    Scene("goal",
          "今集會講：[[b1]]冇 virtual 會點；[[b2]]virtual 函數；[[b3]]override 幫你捉錯；[[b4]]用基底嘅 reference 同指標。",
          BulletCard("今集學識", [("冇 virtual：睇 reference 嘅類型", "b1"), ("virtual：睇真正嘅物件", "b2"), ("override：捉錯", "b3"),
                                ("Animal& 同 Animal*", "b4")])),
    Scene("plain",
          "[[open]]Animal 嘅 speak 印三點；[[sub]]Dog 同 Cat 各自寫咗自己嘅 speak。[[talk]]talk 收一個 Animal reference，叫佢 speak。"
          "[[cc]]main 將一隻狗同一隻貓傳入去，編譯運行：[[o]]兩個都係三點！狗冇吠，貓都冇叫。",
          s.scene(Open("speak.cpp", at="open"), Mark((5, 7), at="open"), Mark((10, 22), at="sub"), Mark((24, 26), at="talk"),
                  Mark(None, at="cc"), Run(c1, at="cc"), Run(r1), Note("狗同貓都係「...」？", at="o", where="editor"))),
    Scene("why",
          "因為冇 virtual 嘅話，[[ref]]編譯器只睇 a 嘅類型：Animal reference，[[fixed]]於是編譯嗰陣就決定咗，用 Animal 嘅 speak。"
          "[[want]]我哋想要嘅，係行嘅時候先睇 a 真正係乜嘢動物。",
          TableCard("用邊個 speak？", ["", "睇乜決定", "talk(d) 印"], [
              (["冇 virtual", "a 嘅類型：Animal&", "..."], "ref"),
              (["有 virtual", "真正嘅物件：Dog", "Woof!"], "want", GREEN),
          ], widths=[1, 1.6, 1], code_cols=(2,), size=40)),
    Scene("virtual",
          "[[type]]喺 Animal 嘅 speak 前面加 virtual。[[cc]]編譯：[[warn]]有個警告，話 Animal 嘅 speak 俾 Cat 遮住咗。運行：[[o]]狗吠咗，但係貓仲係三點！",
          s.scene(Note(None), Run(clr, at="type"), Replace("speak.cpp", "    void speak() const {\n        std::cout << \"...",
                                                            "    virtual void speak() const {\n        std::cout << \"...", at="type"),
                  Expect("speak.cpp", V2), Run(c2, at="cc", recall=True), Scroll(at="warn"), Run(r2, at="o"))),
    Scene("bug",
          "[[look]]睇清楚 Cat 嘅 speak：漏咗 const！即係同 Animal 嘅唔係同一個函數，冇覆寫到，只係另外寫咗一個新嘅。"
          "呢種錯好難睇出嚟。",
          s.scene(Mark(5, at="look"), Mark(19, at=("look", 1.2)), Note("漏咗 const：唔係同一個函數", at="look"))),
    Scene("override",
          "[[type]]解決方法：喺子類別嘅 speak 後面加 override，意思係：我係要覆寫基底嘅。[[cc]]編譯：[[err]]錯誤！Cat 嘅 speak 話要 override，"
          "但係冇嘢俾佢 override。編譯器幫我哋捉到。",
          s.scene(Note(None), Mark(None), Run(clr2, at="type"), Replace("speak.cpp", "void speak() const {\n        std::cout << \"Woof",
                                                                        "void speak() const override {\n        std::cout << \"Woof", at="type"),
                  Replace("speak.cpp", "void speak() {", "void speak() override {"), Expect("speak.cpp", V3),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("fix",
          "[[type]]補返 const。[[ptr]]順手試吓指標：一個 Animal 指標指住貓，用箭咀叫 speak。[[cc]]編譯運行，[[o]]Woof、Meow，指標都係 Meow。",
          s.scene(Run(clr3, at="type"), Replace("speak.cpp", "void speak() override {", "void speak() const override {", at="type"),
                  Type("speak.cpp", PTR, before="}", last=True, at="ptr"), Expect("speak.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("poly",
          "呢個就係多型：[[one]]同一句 a 點 speak，[[many]]遇到唔同嘅物件，就有唔同嘅行為。[[how]]條件係：函數要 virtual，"
          "而且要經 reference 或者指標去呼叫。",
          BulletCard("多型", [("同一句 a.speak()", "one"), ("狗吠、貓叫：睇真正嘅物件", "many"),
                            ("virtual + 經 Animal& 或 Animal* 呼叫", "how")])),
    Scene("recap",
          "總結：[[r1]]冇 virtual，只睇 reference 嘅類型；[[r2]]有 virtual，行嘅時候睇真正嘅物件；[[r3]]子類別一律加 override，寫錯編譯器會捉；"
          "[[r4]]經基底嘅 reference 或者指標去用，就係多型。",
          BulletCard("今集重點", [("冇 virtual：睇類型", "r1"), ("virtual：睇真正物件", "r2"), ("一律加 override", "r3"),
                                ("Animal& / Animal*：多型", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一隻 Cow，識講 Moo；整一個 Animal 指標嘅陣列，放狗同牛，用迴圈逐隻 talk。[[next]]下一集：抽象類別。多謝收睇，下次見！",
          EndCard("加 class Cow（speak 印 Moo!）；用 const Animal* 陣列裝住狗同牛，迴圈逐隻 talk。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

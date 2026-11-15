#!/usr/bin/env python3
"""Video 82 (syllabus 7.2): 類別模板

An IntStack (a vector<int> inside) really prints 3 2 1. Turning it into template <typename T>
class Stack keeps that output with Stack<int>; `Stack nums;` without <int> is a real "class
template argument deduction failed" error; Stack<std::string> really prints "world 1".
Run `python3 video7.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 82
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-02"
FINAL = (CODE / "stack.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
WORDS = ("    Stack<std::string> words;\n    words.push(\"hello\");\n    words.push(\"world\");\n"
         "    std::cout << words.pop() << ' ' << words.size() << '\\n';\n")
V2 = FINAL.replace(WORDS, "").replace("#include <string>\n", "")
V1 = (V2.replace("template <typename T>\nclass Stack {", "class IntStack {").replace("void push(const T& value)", "void push(int value)")
      .replace("T pop()", "int pop()").replace("T top =", "int top =").replace("std::vector<T> items_", "std::vector<int> items_")
      .replace("Stack<int> nums", "IntStack nums"))
BAD = V2.replace("Stack<int> nums;", "Stack nums;")
CC = "g++ -std=c++20 -Wall -Wextra stack.cpp -o st"

(c1, r1, clr, c2, r2, c3, clr2, c4, r4, cch, rch) = cpp.session({"stack.cpp": V1}, [
    CC, "./st", "clear", Write("stack.cpp", V2), CC, "./st", Write("stack.cpp", BAD), CC, "clear", Write("stack.cpp", FINAL), CC, "./st",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "3 2 1 \n" == r2.output and r4.output == "3 2 1 \nworld 1\n", (r1.output, r4.output)
assert "class template argument deduction failed" in cpp.visible(c3.output) and "couldn't deduce template parameter 'T'" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "b 2\na 1\n"

SAY = {"template <typename T>": "template typename T", "Stack<int>": "Stack 角括號 int", "Stack<std::string>": "Stack 角括號 string",
       "Stack<T>": "Stack 角括號 T", "IntStack": "Int Stack", "std::vector<T>": "vector 角括號 T", "const T&": "const T reference",
       "push": "push", "pop": "pop", "top": "top", "Stack": "Stack", "T": "T", "hello": "hello", "world": "world", "items_": "items 底線"}

s = Stage({"stack.cpp": V1}, title="類別模板", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅函數模板，令一個函數用得喺唔同類型。class 都一樣：今集學類別模板，寫一個乜嘢都裝得嘅 Stack。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "template class · Stack<T>")),
    Scene("goal",
          "今集會講：[[b1]]一個只裝 int 嘅 stack；[[b2]]變成類別模板；[[b3]]用嘅時候要寫角括號；[[b4]]Stack int 同 Stack string 係兩個唔同嘅 class。",
          BulletCard("今集學識", [("IntStack：只裝 int", "b1"), ("template <typename T> class", "b2"), ("Stack<int>：要寫類型", "b3"),
                                ("每個 T 一個 class", "b4")])),
    Scene("int",
          "Stack 好似一疊碟：[[push]]push 放喺最頂，[[pop]]pop 由最頂攞走，最後放嘅最先攞。[[main]]放一、二、三，再逐個 pop。[[cc]]編譯運行，"
          "[[o]]三、二、一，倒轉咗：最後放入去嘅三，最先攞出嚟。",
          s.scene(Open("stack.cpp", at="push"), Mark((6, 8), at="push"), Mark((9, 13), at="pop"), Mark((26, 33), at="main"),
                  Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("tmpl",
          "[[t]]但係佢只裝得 int。改做模板：上面加 template typename T，名改做 Stack。[[types]]跟住將裝住嘅類型全部換做 T：push 收 const T reference，"
          "pop 回傳 T，[[vec]]入面係 vector 角括號 T。",
          s.scene(Mark(None), Run(clr, at="t"), Replace("stack.cpp", "class IntStack {", "template <typename T>\nclass Stack {", at="t", rate=20),
                  Replace("stack.cpp", "void push(int value)", "void push(const T& value)", at="types"),
                  Replace("stack.cpp", "int pop()", "T pop()"), Replace("stack.cpp", "int top =", "T top ="),
                  Replace("stack.cpp", "std::vector<int> items_", "std::vector<T> items_", at="vec"))),
    Scene("use",
          "[[main]]用嘅時候，要喺名後面講明裝乜：Stack 角括號 int。[[cc]]編譯運行，[[o]]三、二、一，同之前一樣。",
          s.scene(Replace("stack.cpp", "IntStack nums", "Stack<int> nums", at="main"), Expect("stack.cpp", V2), Mark(27, at="main"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("noarg",
          "[[type]]如果唔寫角括號呢？[[cc]]編譯：[[err]]錯誤：推導唔到 T。一個空嘅 Stack，編譯器冇線索知道你想裝乜。",
          s.scene(Replace("stack.cpp", "Stack<int> nums;", "Stack nums;", at="type"), Expect("stack.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("str",
          "[[fix]]加返 int。[[type]]再整一個裝字串嘅 Stack：push hello 同 world，pop 一個，再睇剩幾多個。[[cc]]編譯運行，[[o]]world，剩返一個。"
          "同一份 code，裝字串都得，一行都唔使改。",
          s.scene(Run(clr2, at="fix"), Replace("stack.cpp", "Stack nums;", "Stack<int> nums;", at="fix"),
                  Replace("stack.cpp", "#include <iostream>\n", "#include <iostream>\n#include <string>\n", at="type"),
                  Type("stack.cpp", WORDS, before="}", last=True, rate=40), Expect("stack.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("two",
          "[[gen]]編譯器見到 Stack int 同 Stack string，[[cls]]就用模板生成兩個 class：一個入面係 vector int，一個係 vector string。"
          "[[diff]]佢哋係兩個完全唔同嘅類型。",
          BoxesCard("一個模板，兩個 class", [
              BoxRow([Box("template", "Stack<T>", "模板：唔係 class", at="gen", color=PURPLE, w=380, key="t")]),
              BoxRow([Box("Stack<int>", "vector<int>", "class", at="cls", color=BLUE, w=320, key="i"),
                      Box("Stack<std::string>", "vector<string>", "另一個 class", at="cls", color=GREEN, w=360, key="s")], gap=80),
          ], arrows=[("t", "i", "cls", BLUE), ("t", "s", "cls", GREEN)], notes=[("兩個唔同嘅類型", "diff")],
              top=CONTENT_TOP + 10, row_h=320, box_h=110, size=38)),
    Scene("recap",
          "總結：[[r1]]template typename T 放喺 class 前面；[[r2]]入面要變嘅類型寫 T；[[r3]]用嘅時候寫 Stack 角括號 int；"
          "[[r4]]每個唔同嘅 T，都會生成一個唔同嘅 class。std::vector 本身就係咁寫出嚟嘅。",
          BulletCard("今集重點", [("template <typename T> class Stack", "r1"), ("裝住嘅類型寫 T", "r2"), ("Stack<int> nums;", "r3"),
                                ("每個 T：一個新 class", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]幫 Stack 加一個 top 函數，睇最頂嗰個但係唔攞走；用 Stack char 試吓。[[next]]下一集：模板參數推導，同埋 CTAD。"
          "多謝收睇，下次見！",
          EndCard("加 const T& top() const：睇最頂但唔攞走。用 Stack<char> 試：push 'a'、'b'，top 應該係 b。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

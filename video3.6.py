#!/usr/bin/env python3
"""Video 35 (syllabus 3.6): 傳參考同 const reference

swapInts with value parameters really leaves 1 2; with int& it gives 2 1 (the swap traced step by
step); swapInts(1, 2) is a real "cannot bind non-const lvalue reference" error; greet takes a
const std::string& so nothing is copied or changed. Run `python3 video3.6.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 35
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-06"
FINAL = (CODE / "swap.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
GREET = "void greet(const std::string& name) {\n    std::cout << \"Hello, \" << name << \"!\\n\";\n}\n\n"
CALLS = "    std::string who = \"Chan Tai Man\";\n    greet(who);\n"
V2 = FINAL.replace("#include <string>\n", "").replace(GREET, "").replace(CALLS, "")
V1 = V2.replace("int& a, int& b", "int a, int b")
VR = V2.replace("swapInts(x, y);", "swapInts(1, 2);")
CC = "g++ -std=c++20 -Wall -Wextra swap.cpp -o swap"

(c1, r1, c2, r2, c3, clr, c4, r4, cch, rch) = cpp.session({"swap.cpp": V1}, [
    CC, "./swap", Write("swap.cpp", V2), CC, "./swap", Write("swap.cpp", VR), CC,
    Write("swap.cpp", FINAL), "clear", CC, "./swap",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.strip() == "1 2" and r2.output.strip() == "2 1"
assert "cannot bind non-const lvalue reference of type 'int&'" in cpp.visible(c3.output), c3.output
assert r4.output == "2 1\nHello, Chan Tai Man!\n" and c1.code == c2.code == c4.code == cch.code == 0 and rch.output.strip() == "85"

SAY = {"swapInts": "swap ints", "swapInts(1, 2)": "swap ints 一、二", "int&": "int and", "temp": "temp",
       "const std::string&": "const S T D string and", "std::swap": "S T D swap", "greet": "greet"}

s = Stage({"swap.cpp": V1}, title="傳參考同 const reference", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集學咗 reference。今集將佢用喺函數參數，寫一個真正可以交換兩個變數嘅 swap。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int& · const std::string&")),
    Scene("goal",
          "今集會講：[[b1]]傳參考：函數改到呼叫者嘅變數；[[b2]]const reference：唔使複製，又唔會被改；[[b3]]幾時用邊一種。",
          BulletCard("今集學識", [("傳參考 int&", "b1"), ("const reference", "b2"), ("幾時用邊種", "b3")])),
    Scene("byvalue",
          "[[open]]swapInts 用一個臨時變數 temp，將 a 同 b 交換。[[cc]]編譯運行，[[o]]x 同 y 仲係一同二，冇交換到。"
          "[[why]]記得 3.4：參數只係副本。",
          s.scene(Open("swap.cpp", at="open"), Mark((3, 7), at=("open", 0.8)), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note("交換咗副本\nx、y 冇郁過", at="why", where="editor"))),
    Scene("byref",
          "[[amp]]將兩個參數都加 and 號，變成 int&。[[cc]]再編譯運行，[[o]]今次係二同一，交換成功！",
          s.scene(Note(None), Replace("swap.cpp", "int a, int b", "int& a, int& b", at="amp"), Expect("swap.cpp", V2),
                  Mark(3, at="amp"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("boxes",
          "因為而家 a 同 b，[[names]]就係 x 同 y 嘅第二個名。[[swap]]函數入面交換 a 同 b，其實就係交換緊 x 同 y。",
          BoxesCard("int& a, int& b：x 同 y 嘅第二個名", [BoxRow([
              Box("x / a", [("1", "names"), ("2", "swap")], "int", at="names", color=PURPLE, w=300),
              Box("y / b", [("2", "names"), ("1", ("swap", 0.5))], "int", at="names", color=PURPLE, w=300),
          ], gap=160)], top=CONTENT_TOP + 90, box_h=150, size=64)),
    Scene("steps",
          "交換嘅三步：[[s1]]先將 a 放入 temp 保存；[[s2]]再將 b 放入 a；[[s3]]最後將 temp 放入 b。冇咗 temp，a 原本個值就會冇咗。",
          TableCard("點樣交換？", ["步驟", "a（x）", "b（y）", "temp"], [
              (["開始", "1", "2", "–"], None),
              (["temp = a;", "1", "2", "1"], "s1"),
              (["a = b;", "2", "2", "1"], "s2"),
              (["b = temp;", "2", "1", "1"], "s3", GREEN),
          ], widths=[1.2, 0.8, 0.8, 0.8], code_cols=(0, 1, 2, 3), size=42)),
    Scene("rvalue",
          "試吓直接傳數字：[[type]]swapInts(1, 2)。[[cc]]編譯，[[err]]出錯：int& 唔可以綁住一個臨時嘅值。"
          "reference 一定要代表一個真正嘅變數。[[undo]]改返做 x 同 y。",
          s.scene(Mark(None), Replace("swap.cpp", "swapInts(x, y);", "swapInts(1, 2);", at="type"), Expect("swap.cpp", VR),
                  Run(c3, at="cc", recall=True), Replace("swap.cpp", "swapInts(1, 2);", "swapInts(x, y);", at="undo"),
                  Expect("swap.cpp", V2))),
    Scene("cref",
          "傳字串呢啲大嘅嘢，傳值要將成個字串複製一次，好浪費。[[type]]greet 用 const std::string&：[[noc]]唔複製，直接用原本嗰個；"
          "[[const]]const 保證函數唔會改佢，要改嘅話，編譯器會阻止你。",
          s.scene(Type("swap.cpp", "#include <string>\n", after="#include <iostream>\n", at="type"),
                  Type("swap.cpp", GREET, before="int main", rate=24), Type("swap.cpp", CALLS, before="}", last=True, rate=24),
                  Expect("swap.cpp", FINAL), Mark(10, at="const"))),
    Scene("cref_run",
          "[[cc]]編譯運行，[[o]]印出 Hello, Chan Tai Man!；上面嘅 x 同 y，仍然係交換咗嘅二同一。",
          s.scene(Mark(None), Run(clr, at="cc"), Run(c4, recall=True), Run(r4))),
    Scene("which",
          "三種傳法點揀？[[v]]int 呢啲細嘅型別，唔使改，就傳值；[[r]]要改呼叫者嘅變數，就傳參考；"
          "[[c]]string 呢啲大嘅嘢，唔使改，就用 const reference。",
          TableCard("三種傳法", ["寫法", "幾時用"], [
              (["int n", "細嘅型別，唔使改：傳值"], "v"),
              (["int& n", "要改呼叫者嘅變數：傳參考"], "r"),
              (["const std::string& s", "大嘅嘢，唔使改：const 參考"], "c"),
          ], widths=[1.3, 1.6], code_cols=(0,), size=42)),
    Scene("recap",
          "總結：[[r1]]參數加 and 號，函數就可以改到呼叫者嘅變數；[[r2]]reference 參數一定要傳變數，唔可以傳數字；"
          "[[r3]]大嘅嘢用 const reference，唔複製又安全；[[r4]]標準庫其實已經有 std::swap。",
          BulletCard("今集重點", [("int&：改到呼叫者嘅變數", "r1"), ("要傳變數，唔可以傳 1、2", "r2"),
                                ("大嘅嘢：const std::string&", "r3"), ("標準庫有 std::swap", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數 addBonus，用 reference 參數，將分數直接加上獎勵分。"
          "[[next]]下一集，我哋學預設參數同函數多載。多謝收睇，下次見！",
          EndCard("寫一個函數 addBonus(int& score, int bonus)，將分數直接加上獎勵分。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

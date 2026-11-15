#!/usr/bin/env python3
"""Video 46 (syllabus 4.5): C 風格陣列

int marks[5]: sizeof(marks) / sizeof(marks[0]) gives 5 in main, but inside a function the array
has decayed to a pointer and the same sum really gives 2 (with g++'s -Wsizeof-array-argument
warning); passing the size separately; why std::array or std::vector is better.
Run `python3 video4.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 46
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-05"
FINAL = (CODE / "carray.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
GOOD_FN = FINAL.split("#include <iostream>\n\n")[1].split("int main")[0]
BAD_FN = ("void printAll(int a[]) {\n    int n = sizeof(a) / sizeof(a[0]);\n"
          "    std::cout << \"In function: \" << n << '\\n';\n}\n\n")
V1 = FINAL.replace(GOOD_FN, "").replace("    printAll(marks, n);\n", "")
V2 = FINAL.replace(GOOD_FN, BAD_FN).replace("printAll(marks, n);", "printAll(marks);")
CC = "g++ -std=c++20 -Wall -Wextra carray.cpp -o arr"

(c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"carray.cpp": V1}, [
    CC, "./arr", Write("carray.cpp", V2), CC, "./arr", Write("carray.cpp", FINAL), "clear", CC, "./arr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "In main: 5\n" and r2.output == "In main: 5\nIn function: 2\n"
assert "will return size of 'int*'" in cpp.visible(c2.output), c2.output
assert r3.output == "In main: 5\n72 85 64 91 58 \n" and c1.code == c3.code == cch.code == 0 and rch.output.strip() == "370"

SAY = {"int marks[5]": "int marks 五", "sizeof": "size of", "printAll": "print all", "std::array": "S T D array",
       "int a[]": "int a 中括號", "decay": "decay"}

s = Stage({"carray.cpp": V1}, title="C 風格陣列", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！喺 vector 之前，C 語言已經有陣列。今集睇吓呢種舊式陣列有乜陷阱，同埋點解我哋通常唔用佢。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int a[5] · sizeof · decay")),
    Scene("goal",
          "今集會講：[[b1]]點樣宣告 C 風格陣列；[[b2]]佢冇 size；[[b3]]傳入函數就會退化做指標；[[b4]]應該用乜代替。",
          BulletCard("今集學識", [("int marks[5]", "b1"), ("冇 size()", "b2"), ("傳入函數：退化 decay", "b3"), ("用乜代替", "b4")])),
    Scene("declare",
          "[[decl]]int marks[5]：一個裝五個 int 嘅陣列，大小固定，唔可以 push_back。[[nosize]]佢亦冇 size，"
          "想知有幾多格，要用 sizeof：成個陣列嘅 byte 數，除以一格嘅 byte 數。[[cc]]編譯運行，[[o]]五格，即係二十個 byte 除四個 byte。比起 vector 嘅 size，麻煩好多。",
          s.scene(Open("carray.cpp", at="decl"), Mark(4, at="decl"), Mark(5, at="nosize"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("func",
          "[[type]]將陣列傳入一個函數，喺函數入面用同一條式計格數。[[cc]]編譯，[[warn]]g++ 警告：喺參數度用 sizeof，量到嘅係 int 指標嘅大小。"
          "[[run]]運行，[[o]]main 入面係五，函數入面變咗二！",
          s.scene(Type("carray.cpp", BAD_FN, before="int main", at="type", rate=26),
                  Type("carray.cpp", "    printAll(marks);\n", before="}", last=True), Expect("carray.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2, at="run"), Note("main：5\n函數入面：2？", at="o", where="editor"))),
    Scene("decay",
          "因為陣列一傳入函數，就會退化，英文叫 decay：[[ptr]]變成一個指標，只係記住第一格喺邊，[[lost]]唔再知道自己有幾多格。"
          "[[math]]sizeof 量到嘅，係指標嘅八個 byte，除以 int 嘅四個 byte，就得二。指標喺第五章會詳細講。",
          BoxesCard("傳入函數：退化做指標", [
              BoxRow([Box("", str(v), f"[{i}]", at="ptr", w=150, color=AMBER if i == 0 else BLUE)
                      for i, v in enumerate([72, 85, 64, 91, 58])], label="main：marks", gap=0, at="ptr"),
              BoxRow([Box("a", "→ 第一格", "int*（8 byte）", at="ptr", color=PURPLE, w=320, key="a")], label="printAll", at="ptr"),
          ], top=CONTENT_TOP + 20, row_h=230, box_h=110, size=44,
              notes=[("a 唔知道陣列有幾多格", "lost"), ("sizeof(a) / sizeof(a[0]) = 8 / 4 = 2", "math")])),
    Scene("fix",
          "[[fix]]所以用 C 風格陣列，就要另外傳格數入去：參數多一個 n；[[loop]]函數用 n 嚟行迴圈。[[cc]]編譯運行，[[o]]五個分數全部印出嚟。",
          s.scene(Note(None), Replace("carray.cpp", BAD_FN, GOOD_FN, at="fix", rate=30),
                  Replace("carray.cpp", "printAll(marks);", "printAll(marks, n);", at="loop"), Expect("carray.cpp", FINAL),
                  Run(clr, at="cc"), Run(c3, recall=True), Run(r3))),
    Scene("compare",
          "比較三種：[[c]]C 風格陣列，大小固定，唔知自己幾大，傳入函數就退化；[[a]]下一集嘅 std::array，大小都係固定，但係知道自己幾大；"
          "[[v]]std::vector，可以變大，又知道自己幾大。[[rule]]所以寫新程式，用 std::array 或者 std::vector。",
          TableCard("三種陣列", ["", "大小", "知道自己幾大？", "傳入函數"], [
              (["int a[5]", "固定", "唔知（要 sizeof）", "退化做指標"], "c", RED),
              (["std::array<int, 5>", "固定", "知：size()", "完整傳入"], "a", GREEN),
              (["std::vector<int>", "可以變大", "知：size()", "完整傳入"], "v", GREEN),
          ], widths=[1.4, 0.8, 1.3, 1.1], code_cols=(0,), size=36, note=("新程式：用 std::array 或 std::vector", "rule"))),
    Scene("recap",
          "總結：[[r1]]C 風格陣列大小固定，冇 size；[[r2]]傳入函數會退化做指標，sizeof 就唔準；[[r3]]要另外傳格數；"
          "[[r4]]盡量用 std::array 同 std::vector。",
          BulletCard("今集重點", [("int a[5]：固定大小，冇 size()", "r1"), ("傳入函數：退化做指標", "r2"),
                                ("要另外傳格數 n", "r3"), ("新程式：std::array / std::vector", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數 sum，收一個 C 風格陣列同埋格數，回傳總和。[[next]]下一集，我哋學 std::array。多謝收睇，下次見！",
          EndCard("寫一個函數 sum(const int a[], int n)，回傳陣列嘅總和。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

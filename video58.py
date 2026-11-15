#!/usr/bin/env python3
"""Video 58 (syllabus 5.7): new 同 delete

new int{42} and delete; new int[n] sized at run time and delete[]; without delete[] the program
runs as if nothing were wrong, but built with -fsanitize=address it ends with a real
LeakSanitizer report (bytes leaked and the line of the new[]). Run `python3 video58.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 58
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-07"
FINAL = (CODE / "heap.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
L = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
SKEL = "#include <iostream>\n\nint main() {\n}\n"
LEAK = FINAL.replace("    delete[] arr;\n", "")
CC = "g++ -std=c++20 -Wall -Wextra heap.cpp -o heap"
CA = "g++ -std=c++20 -g -fsanitize=address heap.cpp -o heap"

(c1, r1, c2, r2, clr, a1, ra1, a2, ra2, cch, rch) = cpp.session({"heap.cpp": FINAL}, [
    CC, Input("./heap", ["5"]), Write("heap.cpp", LEAK), CC, Input("./heap", ["5"]),
    "clear", CA, Input("./heap", ["5"]), Write("heap.cpp", FINAL), CA, Input("./heap", ["5"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["3", "24 26 28"]),
], refresh=opts.fresh_runs, cols=58)
assert r1.output.endswith("0 1 4 9 16 \n") and r1.output.startswith("42\n") and r2.output == r1.output and r2.code == 0
leak = cpp.visible(ra1.output)
assert "LeakSanitizer: detected memory leaks" in leak and "20 byte(s) leaked" in leak and "heap.cpp:11" in leak, leak[-600:]
assert "LeakSanitizer" not in ra2.output and ra2.code == 0 and rch.output.endswith("Average: 26\n")

SAY = {"new": "new", "delete": "delete", "delete[]": "delete 中括號", "new int[n]": "new int n", "new int{42}": "new int 四十二",
       "LeakSanitizer": "Leak Sanitizer", "memory leak": "memory leak", "-fsanitize=address": "dash F sanitize address"}

s = Stage({"heap.cpp": SKEL}, title="new 同 delete", split=0.45, code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！5.1 講過 heap。今集學點樣自己喺 heap 攞記憶體：用 new；同埋用完之後，用 delete 還返。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "new · delete · new[] · delete[]")),
    Scene("goal",
          "今集會講：[[b1]]new 攞一個；[[b2]]new 中括號攞一排；[[b3]]delete 還返；[[b4]]唔還會點：memory leak。",
          BulletCard("今集學識", [("new：攞一個", "b1"), ("new[]：攞一排", "b2"), ("delete / delete[]：還返", "b3"), ("memory leak", "b4")])),
    Scene("one",
          "[[new]]new int，喺 heap 開一格 int，放入四十二，回傳佢嘅地址，所以用指標接住。[[use]]用嘅時候一樣用星號；"
          "[[del]]用完，就用 delete 還返俾系統。",
          s.scene(Open("heap.cpp", mode="instant"), Type("heap.cpp", L[0], before="}", last=True, at="new"),
                  Type("heap.cpp", L[1], before="}", last=True, at="use"), Type("heap.cpp", "".join(L[2:4]), before="}", last=True, at="del"))),
    Scene("many",
          "[[read]]跟住讀入一個數 n。[[arr]]new int 中括號 n：喺 heap 開 n 格。n 要運行嗰陣先知，所以要用 heap。"
          "[[fill]]填入平方數，再印出嚟；[[del]]用完，用 delete 中括號還返成排，唔係淨係還第一格。new 中括號，就配 delete 中括號。",
          s.scene(Type("heap.cpp", "".join(L[4:7]), before="}", last=True, at="read", rate=30),
                  Type("heap.cpp", L[7], before="}", last=True, at="arr"),
                  Type("heap.cpp", "".join(L[8:15]), before="}", last=True, at="fill", rate=40),
                  Type("heap.cpp", L[15], before="}", last=True, at="del"), Expect("heap.cpp", FINAL))),
    Scene("run1",
          "[[cc]]編譯運行：[[o1]]四十二；[[t]]輸入五，[[o2]]零、一、四、九、十六。n 係五，所以開咗五格。",
          s.scene(Run(c1, at="cc"), Run(r1, keys=("t",)))),
    Scene("boxes",
          "[[stack]]p 同 arr 呢兩個指標，喺 stack 入面；[[heap]]佢哋指住嘅記憶體，喺 heap。[[own]]stack 嘅變數會自動收返，"
          "但係 heap 嘅記憶體唔會：要我哋自己 delete。其實 vector 入面，就係幫你做緊呢啲嘢。",
          BoxesCard("stack 上嘅指標，指住 heap", [
              BoxRow([Box("arr", "地址", "int*", at="stack", color=PURPLE, w=220, key="arr")], label="stack"),
              BoxRow([Box("", str(i * i), f"[{i}]", at="heap", color=GREEN, w=130, key=f"h{i}") for i in range(5)],
                     label="heap", gap=0, at="heap"),
          ], arrows=[("arr", "h0", "heap", PURPLE)], top=CONTENT_TOP + 10, row_h=250, box_h=110, size=48,
              notes=[("heap 嘅記憶體：要自己 delete[]", "own")])),
    Scene("leak",
          "如果唔記得還呢？[[del]]刪走 delete 中括號。[[cc]]編譯運行，[[o]]一切正常，乜錯誤都冇。[[why]]呢個就係 memory leak：記憶體借咗唔還，"
          "程式行得耐，就會越食越多。",
          s.scene(Replace("heap.cpp", "    delete[] arr;\n", "", at="del"), Expect("heap.cpp", LEAK), Run(c2, at="cc", recall=True),
                  Run(r2, recall=True, keys=(("cc", 3.5),)), Note("冇 delete[]：都冇錯誤？", at="o", where="editor"))),
    Scene("lsan",
          "[[cc]]用 -fsanitize=address 再編譯運行：[[o]]程式完咗之後，LeakSanitizer 話你知：漏咗二十個 byte，"
          "[[line]]係喺 heap.cpp 第十一行 new 出嚟嘅，即係五個 int。",
          s.scene(Note(None), Run(clr, at="cc"), Run(a1), Run(ra1, keys=(("cc", 5.0),)),
                  Note("20 byte leaked\n＝ 5 個 int（第 11 行）", at="line", where="editor"))),
    Scene("fix",
          "[[fix]]加返 delete 中括號。[[cc]]再用 LeakSanitizer 運行，[[o]]今次冇報告。[[pair]]記住：new 配 delete，new 中括號配 delete 中括號，唔可以撈亂。",
          s.scene(Note(None), Type("heap.cpp", "    delete[] arr;\n", before="}", last=True, at="fix"), Expect("heap.cpp", FINAL),
                  Run(a2, at="cc", recall=True), Run(ra2, recall=True, keys=(("cc", 3.5),)))),
    Scene("rules",
          "規則：[[r1]]每個 new，都要有一個 delete；[[r2]]new 中括號，要配 delete 中括號；[[r3]]好容易漏，所以現代 C++ 好少直接寫 new，"
          "用 vector，或者第五章後面嘅 unique_ptr，佢哋會自動幫你還。",
          BulletCard("new 同 delete 嘅規則", [("每個 new 配一個 delete", "r1"), ("new[] 配 delete[]", "r2"),
                                           ("好易漏：用 vector、unique_ptr（5.9）", "r3")])),
    Scene("recap",
          "總結：[[r1]]new 喺 heap 攞記憶體，回傳地址；[[r2]]delete 同 delete 中括號還返；[[r3]]唔還就係 memory leak；"
          "[[r4]]LeakSanitizer 幫你搵出嚟。",
          BulletCard("今集重點", [("new：喺 heap 攞記憶體", "r1"), ("delete / delete[]：還返", "r2"), ("唔還：memory leak", "r3"),
                                ("LeakSanitizer 幫你搵", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 new 中括號開一個 double 陣列，讀入 n 個溫度，計平均溫度；記得還返，再用 LeakSanitizer 檢查吓。"
          "[[next]]下一集，我哋學 RAII：令記憶體自動還返。多謝收睇，下次見！",
          EndCard("用 new double[n] 讀入 n 個溫度，計平均溫度；記得 delete[]，再用 -fsanitize=address 檢查冇 leak。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

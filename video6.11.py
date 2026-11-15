#!/usr/bin/env python3
"""Video 73 (syllabus 6.11): Rule of zero / five

6.9's Buffer needs three hand-written special members (five once moving is added). Swapping
int* for std::vector<int> lets every one of them go: the real run still prints 42 99 42, and
std::move works too (42). With std::unique_ptr<int[]> as the member instead, `Buffer b = a;`
is a real "use of deleted function" error: members decide what the class can do.
Run `python3 video6.11.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 73
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-11"
FINAL = (CODE / "buffer.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
START = (ROOT / "code" / "06-09" / "buffer.cpp").read_text()
SPECIAL = "    Buffer(const Buffer& other)" + START.split("    Buffer(const Buffer& other)")[1].split("    void set")[0]
COPYFROM = "    void copyFrom" + START.split("    void copyFrom")[1].split("    int size_;")[0]
MOVE_LINES = "    Buffer d = std::move(a);\n    std::cout << d.get(0) << '\\n';\n"
V2 = FINAL.replace(MOVE_LINES, "").replace("#include <utility>\n", "")
UPTR = (FINAL.replace("#include <utility>\n#include <vector>\n", "#include <memory>\n#include <utility>\n")
        .replace("data_(n)", "data_{std::make_unique<int[]>(n)}").replace("std::vector<int> data_;", "std::unique_ptr<int[]> data_;"))
CC = "g++ -std=c++20 -Wall -Wextra buffer.cpp -o buf"

(c1, r1, clr, c2, r2, clr2, c3, cch, rch) = cpp.session({"buffer.cpp": V2}, [
    CC, "./buf", "clear", Write("buffer.cpp", FINAL), CC, "./buf", "clear", Write("buffer.cpp", UPTR), CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "42 99 42\n" and r2.output == "42 99 42\n42\n" and c1.code == c2.code == cch.code == 0, (r1.output, r2.output)
assert "use of deleted function 'Buffer::Buffer(const Buffer&)'" in cpp.visible(c3.output), c3.output[:400]
assert rch.output == "0 1000000 1000000\n", rch.output

SAY = {"std::vector<int>": "S T D vector int", "std::unique_ptr": "S T D unique pointer", "unique_ptr": "unique pointer",
       "rule of zero": "rule of zero", "rule of five": "rule of five", "rule of three": "rule of three", "data_": "data 底線",
       "std::move": "S T D move", "use of deleted function": "use of deleted function", "= default": "等如 default",
       "operator=": "operator 等號", "Buffer&&": "Buffer 兩個 and 號"}

s = Stage({"buffer.cpp": START}, title="Rule of zero / five", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！6.9 嘅 Buffer，為咗管一個指標，寫咗三個特別成員函數；6.10 再加搬移，就變成五個。有冇辦法一個都唔使寫？今集講 rule of zero 同 rule of five。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "rule of five · rule of zero")),
    Scene("goal",
          "今集會講：[[b1]]五個特別成員函數；[[b2]]用 vector 做成員，全部唔使寫；[[b3]]用 unique_ptr 做成員，會點；[[b4]]幾時用邊條規則。",
          BulletCard("今集學識", [("五個特別成員函數", "b1"), ("成員用 vector：一個都唔寫", "b2"), ("成員用 unique_ptr：只可以搬", "b3"),
                                ("rule of zero vs rule of five", "b4")])),
    Scene("five",
          "[[d]]解構子，[[cc]]複製建構子，[[ca]]複製賦值，[[mc]]搬移建構子，[[ma]]搬移賦值。如果 class 自己管一個資源，"
          "就要諗清楚五個點做：呢個就係 rule of five。",
          TableCard("五個特別成員函數", ["名", "寫法"], [
              (["解構子", "~Buffer()"], "d"),
              (["複製建構子", "Buffer(const Buffer&)"], "cc"),
              (["複製賦值", "operator=(const Buffer&)"], "ca"),
              (["搬移建構子", "Buffer(Buffer&&)"], "mc"),
              (["搬移賦值", "operator=(Buffer&&)"], "ma"),
          ], widths=[0.8, 1.6], code_cols=(1,), size=40)),
    Scene("old",
          "[[open]]呢個係 6.9 嘅 Buffer。[[sp]]呢十幾行，全部都係為咗照顧 data 底線呢個指標：複製要自己 new，自己抄，解構要 delete。"
          "[[ptr]]問題嘅根源，就係呢個自己管嘅指標。",
          s.scene(Open("buffer.cpp", at="open"), Mark((6, 21), at="sp"), Mark(36, at="ptr"))),
    Scene("refactor",
          "[[vec]]將指標換做 std::vector<int>，vector 自己識複製，識搬，識釋放。[[del]]於是解構子、複製建構子、複製賦值，同埋 copyFrom，"
          "全部刪走。[[ctor]]建構子用小括號，開 n 格。",
          s.scene(Mark(None), Replace("buffer.cpp", "    int size_;\n    int* data_;", "    std::vector<int> data_;", at="vec", rate=30),
                  Replace("buffer.cpp", "#include <iostream>\n", "#include <iostream>\n#include <vector>\n"),
                  Replace("buffer.cpp", COPYFROM, "", at="del"),
                  Replace("buffer.cpp", SPECIAL, ""),
                  Replace("buffer.cpp", "size_{n}, data_{new int[n]{}}", "data_(n)", at="ctor"),
                  Expect("buffer.cpp", V2), Mark(6, at="ctor"))),
    Scene("run1",
          "[[main]]main 一個字都冇改：複製建構、再用等號複製。[[cc]]編譯運行，[[o]]四十二、九十九、四十二，同 6.9 一樣，冇當機，"
          "但係成個 class 短咗一大截。",
          s.scene(Mark((19, 25), at="main"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1),
                  Note("一個特別成員函數都冇寫", at="o", where="editor"))),
    Scene("move",
          "搬移呢？[[type]]加 utility，再加一句 std::move，將 a 搬去 d，跟住印 d 嘅第一格。[[cc]]編譯運行，[[o]]d 拎到四十二。"
          "vector 自己識搬，所以 Buffer 都自動識搬，一行搬移建構子都唔使寫。",
          s.scene(Note(None), Run(clr, at="type"), Replace("buffer.cpp", "#include <vector>\n", "#include <utility>\n#include <vector>\n", at="type"),
                  Type("buffer.cpp", MOVE_LINES, before="}", last=True), Expect("buffer.cpp", FINAL),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("zero",
          "呢個就係 rule of zero：[[m]]成員自己識管自己，[[c]]class 就一個特別成員函數都唔使寫，[[auto]]編譯器自動整嘅版本，會逐個成員複製同搬移，"
          "啱晒。",
          BulletCard("rule of zero", [("成員自己管資源：vector、string、unique_ptr", "m"), ("class：五個都唔寫", "c"),
                                     ("編譯器自動逐個成員複製、搬移", "auto")])),
    Scene("uptr",
          "如果成員係 unique_ptr 呢？[[type]]將 vector 換做 unique_ptr 一個 int 陣列。[[cc]]編譯：[[err]]出錯！use of deleted function："
          "unique_ptr 唔可以複製，所以 Buffer 都唔可以複製。",
          s.scene(Run(clr2, at="type"), Replace("buffer.cpp", "#include <utility>\n#include <vector>\n", "#include <memory>\n#include <utility>\n", at="type"),
                  Replace("buffer.cpp", "data_(n)", "data_{std::make_unique<int[]>(n)}", rate=30),
                  Replace("buffer.cpp", "std::vector<int> data_;", "std::unique_ptr<int[]> data_;", rate=30), Expect("buffer.cpp", UPTR),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("decide",
          "[[good]]呢個係好事：成員決定 class 可以做乜。用 unique_ptr，就係講明呢個物件只可以搬，唔可以複製，編譯器幫你守住。"
          "[[want]]想複製，就用 vector。",
          s.scene(Note("成員唔可以複製\n→ class 都唔可以複製", at="good", where="editor"),
                  Note("想複製：用 vector", at="want", where="editor"))),
    Scene("which",
          "點揀？[[z]]平時用 rule of zero，成員用標準嘅工具；[[f]]只有好少數，真係要自己管一個原始資源嘅 class，先用 rule of five，"
          "而且最好只做呢一件事。",
          TableCard("用邊條規則？", ["情況", "規則", "寫幾多個"], [
              (["成員用 vector / string / unique_ptr", "rule of zero", "0"], "z", GREEN),
              (["自己 new / delete 原始資源", "rule of five", "5"], "f", AMBER),
          ], widths=[1.8, 1.0, 0.7], code_cols=(), size=36)),
    Scene("recap",
          "總結：[[r1]]特別成員函數有五個；[[r2]]成員自己識管自己，class 就一個都唔使寫，即係 rule of zero；"
          "[[r3]]unique_ptr 成員令 class 只可以搬；[[r4]]真係要自己管資源，先寫齊五個。",
          BulletCard("今集重點", [("五個特別成員函數", "r1"), ("rule of zero：用 vector，唔寫", "r2"), ("unique_ptr 成員：只可以搬", "r3"),
                                ("rule of five：自己管就寫齊", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]將 6.10 一百萬個 int 嘅 Buffer 改用 vector，複製一次，搬移一次，印出三個嘅 size。"
          "[[next]]下一集：繼承。多謝收睇，下次見！",
          EndCard("將 6.10 嘅 Buffer 改用 std::vector<int>：Buffer b = a; Buffer c = std::move(a); 印出 a、b、c 嘅 size。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

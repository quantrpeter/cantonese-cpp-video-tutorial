#!/usr/bin/env python3
"""Video 55 (syllabus 5.4): nullptr 同懸空指標

*p on a nullptr really ends in "Segmentation fault" (After never prints); checking for nullptr
fixes it. A pointer into a vector really dangles after push_back and prints garbage; built with
-fsanitize=address the run stops with a real heap-use-after-free report pointing at the line;
re-taking the pointer fixes it. Run `python3 video55.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 55
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-04"
NUL = (CODE / "null.cpp").read_text()
GROW = (CODE / "grow.cpp").read_text()
CHECK = "    if (p != nullptr) {\n        std::cout << *p << '\\n';\n    } else {\n        std::cout << \"p is null\\n\";\n    }\n"
NBAD = NUL.replace(CHECK, "    std::cout << *p << '\\n';\n")
RETAKE = "    p = &v[0];\n"
GBAD = GROW.replace(RETAKE, "")
CN = "g++ -std=c++20 -Wall -Wextra null.cpp -o null"
CG = "g++ -std=c++20 -Wall -Wextra grow.cpp -o grow"
CA = "g++ -std=c++20 -g -fsanitize=address grow.cpp -o grow"

(n1, rn1, n2, rn2, clr, g1, rg1, a1, ra1, a2, ra2) = cpp.session({"null.cpp": NBAD, "grow.cpp": GBAD}, [
    CN, "./null", Write("null.cpp", NUL), CN, "./null",
    "clear", CG, "./grow", CA, "./grow", Write("grow.cpp", GROW), CA, "./grow",
], refresh=opts.fresh_runs, cols=58)
assert rn1.output == "Before\nSegmentation fault\n" and rn2.output == "Before\np is null\nAfter\n"
garbage = rg1.output.split()[1]
assert rg1.output.split()[0] == "1" and garbage != "1", rg1.output
asan = cpp.visible(ra1.output)
assert "AddressSanitizer: heap-use-after-free" in asan and "grow.cpp:9" in asan and ra1.code != 0
assert ra2.output.split() == ["1", "1"] and ra2.code == 0

SAY = {"nullptr": "null pointer", "*p": "星 p", "Segmentation fault": "Segmentation fault", "push_back": "push back",
       "AddressSanitizer": "Address Sanitizer", "-fsanitize=address": "dash F sanitize address", "-g": "dash G",
       "heap-use-after-free": "heap use after free", "ASan": "A San", "dangling": "dangling"}

s = Stage({"null.cpp": NBAD, "grow.cpp": GBAD}, title="nullptr 同懸空指標", split=0.45, code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！指標用錯，係 C++ 最常見、亦最難搵嘅錯誤。今集故意整兩個：空指標同懸空指標，再用一個工具捉住佢哋。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "nullptr · dangling · AddressSanitizer")),
    Scene("goal",
          "今集會講：[[b1]]跟住 nullptr 搵嘢會點；[[b2]]懸空指標：指住已經冇咗嘅記憶體；[[b3]]AddressSanitizer：幫你捉記憶體錯誤嘅工具。",
          BulletCard("今集學識", [("解參考 nullptr", "b1"), ("懸空指標 dangling", "b2"), ("AddressSanitizer", "b3")])),
    Scene("null",
          "[[open]]p 係 nullptr，乜都唔指，但係我哋照用星號 p 去攞個值。[[cc]]編譯運行：[[o]]印咗 Before，然後 Segmentation fault，"
          "After 冇機會印出嚟。",
          s.scene(Open("null.cpp", at="open"), Mark(6, at=("open", 1.2)), Mark(None, at="cc"), Run(n1, at="cc"), Run(rn1))),
    Scene("null_fix",
          "跟住一個唔存在嘅地址去搵嘢，作業系統就即刻停咗個程式。[[fix]]所以用指標之前，可能係空嘅話，就要先檢查佢係咪 nullptr。"
          "[[cc]]再運行，[[o]]程式識得處理，仲行埋 After。",
          s.scene(Replace("null.cpp", "    std::cout << *p << '\\n';\n", CHECK, at="fix", rate=30), Expect("null.cpp", NUL),
                  Run(n2, at="cc", recall=True), Run(rn2))),
    Scene("grow",
          f"第二種係懸空指標。[[open]]p 指住 vector 嘅第一個元素；[[push]]然後 push_back 加多一個。[[cc]]編譯運行：[[o]]第一次印一，"
          f"第二次印出{zh_int(int(garbage))}？",
          s.scene(Run(clr, at="open"), Open("grow.cpp", at="open"), Mark(6, at="open"), Mark(8, at="push"), Mark(None, at="cc"),
                  Run(g1, at="cc"), Run(rg1), Note(f"第二次：{garbage}？", at="o", where="editor"))),
    Scene("why",
          "因為 vector 變大嘅時候，[[move]]可能要搬去一嚿更大嘅記憶體，[[free]]舊嗰嚿就交返出去；[[dangle]]p 仲指住舊嘅地址，"
          "變咗懸空指標。讀出嚟嘅，係垃圾，有時甚至睇落冇事，所以最危險。",
          BoxesCard("push_back 之後：vector 搬咗屋", [
              BoxRow([Box("", str(x), f"舊 [{i}]", at="move", color=RED, w=150, key=f"o{i}") for i, x in enumerate([1, 2, 3])],
                     label="已交返", gap=0, at="free"),
              BoxRow([Box("p", "舊地址", "int*", at="dangle", color=PURPLE, w=260, key="p")], label=""),
              BoxRow([Box("", str(x), f"新 [{i}]", at="move", color=GREEN, w=150) for i, x in enumerate([1, 2, 3, 4])],
                     label="v 而家喺度", gap=0, at="move"),
          ], arrows=[("p", "o0", "dangle", RED)], top=CONTENT_TOP - 10, row_h=200, box_h=90, size=44)),
    Scene("asan",
          "呢種錯誤好難搵，所以有工具幫手。[[cc]]編譯嘅時候加 -fsanitize=address，同埋 -g，[[run]]再運行。"
          "[[o]]程式即刻停低，印出一大段報告。[[top]]睇返最頂：heap use after free，即係用咗已經交返嘅 heap 記憶體；"
          "[[line]]仲話你知係 grow.cpp 第九行。",
          s.scene(Note(None), Run(a1, at="cc"), Run(ra1, at="run"), Scroll(at="top"), Note("heap-use-after-free\n喺 grow.cpp:9", at="line", where="editor"))),
    Scene("fix",
          "[[fix]]push_back 之後，舊嘅指標全部唔可以再用，要重新攞過。[[cc]]用 AddressSanitizer 再編譯運行，[[o]]兩次都係一，報告冇再出現。",
          s.scene(Note(None), Scroll(top=False, at="fix"), Type("grow.cpp", RETAKE, after="v.push_back(4);\n", at="fix"), Expect("grow.cpp", GROW),
                  Run(a2, at="cc", recall=True), Run(ra2))),
    Scene("rules",
          "記住三點：[[r1]]指標可能係空，用之前就檢查 nullptr；[[r2]]vector 變大之後，舊嘅指標、reference 全部失效；"
          "[[r3]]開發同測試嘅時候，用 -fsanitize=address，等工具幫你捉錯。",
          BulletCard("避免指標錯誤", [("可能係空：先檢查 nullptr", "r1"), ("vector 變大：舊指標失效", "r2"),
                                    ("開發時用 -fsanitize=address", "r3")])),
    Scene("recap",
          "總結：[[r1]]解參考 nullptr 會令程式當機；[[r2]]懸空指標指住已經冇咗嘅記憶體，讀到垃圾；[[r3]]AddressSanitizer 會捉住佢，仲話你知邊一行。",
          BulletCard("今集重點", [("*nullptr：Segmentation fault", "r1"), ("懸空指標：讀到垃圾", "r2"),
                                ("ASan：話你知錯喺邊行", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個函數，回傳一個局部變數嘅地址，睇吓 g++ 點樣警告你，再諗吓點解唔得。"
          "[[next]]下一集，我哋睇指標同陣列嘅關係。多謝收睇，下次見！",
          EndCard("寫一個函數回傳局部變數嘅地址（return &n;），睇吓 g++ 點警告，再諗吓點解唔得。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

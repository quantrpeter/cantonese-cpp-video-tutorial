#!/usr/bin/env python3
"""Video 53 (syllabus 5.2): 指標入門

int* p = &score holds score's address (the real address is printed); *p reads it and *p = 99
changes score through the pointer; `int* p = score;` is a real "invalid conversion" error;
addOne(int* p) changes the caller's variable. Run `python3 video53.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 53
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-02"
FINAL = (CODE / "ptr.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
ADDONE = "void addOne(int* p) {\n    *p = *p + 1;\n}\n\n"
CALL = "    addOne(&score);\n    std::cout << \"score: \" << score << '\\n';\n"
SET = "    *p = 99;\n    std::cout << \"score: \" << score << '\\n';\n"
V2 = FINAL.replace(ADDONE, "").replace(CALL, "")
V1 = V2.replace(SET, "")
BAD = V1.replace("int* p = &score;", "int* p = score;")
CC = "g++ -std=c++20 -Wall -Wextra ptr.cpp -o ptr"

(c0, c1, r1, c2, r2, clr, c3, r3, cch, rch) = cpp.session({"ptr.cpp": BAD}, [
    CC, Write("ptr.cpp", V1), CC, "./ptr", Write("ptr.cpp", V2), CC, "./ptr",
    Write("ptr.cpp", FINAL), "clear", CC, "./ptr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "invalid conversion from 'int' to 'int*'" in cpp.visible(c0.output), c0.output
assert "possible fix: take the address with '&'" in cpp.visible(c0.output)
o1 = r1.output.split("\n")
address = o1[1].split()[-1]
assert o1[0] == "score: 10" and address.startswith("0x") and o1[2].split()[-1] == "10"
assert r2.output.strip().endswith("score: 99") and r3.output.strip().endswith("score: 100")
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.strip() == "2 1"

SAY = {"int*": "int pointer", "int* p = &score": "int pointer p 等如 and score", "*p": "星 p", "&score": "and score",
       "*p = 99": "星 p 等如九十九", "addOne": "add one", "pointer": "pointer", "&": "and 號"}

s = Stage({"ptr.cpp": BAD}, title="指標入門", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集學咗地址。今集學一種專門裝地址嘅變數：指標，英文叫 pointer。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int* · & · *")),
    Scene("goal",
          "今集會講：[[b1]]用 int 星號宣告指標；[[b2]]星號跟住地址，去搵返個值；[[b3]]經指標改變數；[[b4]]用指標做函數參數。",
          BulletCard("今集學識", [("int* p：指標 pointer", "b1"), ("*p：搵返個值", "b2"), ("經指標改變數", "b3"), ("指標參數", "b4")])),
    Scene("bad",
          "[[open]]score 係十。[[decl]]int 星號 p，即係一個指住 int 嘅指標。等號右邊……[[cc]]編譯：[[err]]出錯，唔可以將 int 變做 int 指標！"
          "[[why]]指標要裝地址，唔係裝個值；g++ 仲提示你：攞地址，要加 and 號。",
          s.scene(Open("ptr.cpp", at="open"), Mark(5, at="decl"), Mark(None, at="cc"), Run(c0, at="cc"),
                  Note("指標裝地址：要 &score", at="why", where="editor"))),
    Scene("fix",
          "[[fix]]加返 and 號：p 而家裝住 score 嘅地址。[[cc]]編譯運行：[[o1]]score 係十；[[o2]]p 係一個地址；"
          "[[o3]]星號 p，就係跟住呢個地址去搵，搵到嘅值都係十。",
          s.scene(Note(None), Type("ptr.cpp", "&", before="score;\n    std::cout", at="fix"), Expect("ptr.cpp", V1),
                  Run(c1, at="cc", recall=True), Run(r1), Mark(7, at="o2"), Mark(8, at="o3"))),
    Scene("boxes",
          f"用盒嚟睇：[[score]]score 喺地址尾 {address[-2:]} 嗰度，裝住十；[[p]]p 係另一個盒，入面裝嘅係 score 嘅地址，"
          "好似一張寫住門牌嘅紙條。[[arrow]]所以話 p 指住 score。",
          BoxesCard("int* p = &score;", [BoxRow([
              Box("p", address, "int*（指標）", at="p", color=PURPLE, w=440, key="p"),
              Box("score", "10", f"地址 {address}", at="score", color=AMBER, w=330, key="score"),
          ], gap=170)], arrows=[("p", "score", "arrow", PURPLE)], top=CONTENT_TOP + 80, box_h=130, size=40)),
    Scene("set",
          "[[type]]星號 p 等於九十九：即係跟住 p 嘅地址，將嗰度嘅值改做九十九。[[cc]]編譯運行，[[o]]score 變咗九十九，"
          "雖然我哋冇直接寫 score。",
          s.scene(Mark(None), Type("ptr.cpp", SET, before="}", last=True, at="type", rate=22), Expect("ptr.cpp", V2),
                  Run(c2, at="cc", recall=True), Run(r2))),
    Scene("stars",
          "星號同 and 號有兩種用法，好易撈亂：[[decl]]宣告嗰陣，int 星號，係講個型別：呢個係指標；[[deref]]用嘅時候，星號 p，"
          "係跟住地址去搵個值；[[addr]]and 號 score，就係攞 score 嘅地址。",
          TableCard("* 同 & 點樣讀？", ["寫法", "讀法"], [
              (["int* p", "p 係一個指住 int 嘅指標"], "decl"),
              (["*p", "p 指住嗰度嘅值"], "deref"),
              (["&score", "score 嘅地址"], "addr"),
          ], widths=[1, 2], code_cols=(0,), size=44)),
    Scene("func",
          "指標都可以做函數參數。[[fn]]addOne 收一個 int 指標，將佢指住嘅值加一。[[call]]呼叫嗰陣傳 score 嘅地址。"
          "[[cc]]運行，[[o]]score 變咗一百：同 3.6 嘅 reference 一樣，改到呼叫者嘅變數。",
          s.scene(Run(clr, at="fn"), Type("ptr.cpp", ADDONE, after="#include <iostream>\n\n", at="fn", rate=24),
                  Type("ptr.cpp", CALL, before="}", last=True, at="call", rate=26), Expect("ptr.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("recap",
          "總結：[[r1]]指標係裝地址嘅變數；[[r2]]and 號攞地址，星號跟住地址搵個值；[[r3]]經指標可以改原本嘅變數；"
          "[[r4]]下一集，比較指標同 reference。",
          BulletCard("今集重點", [("指標：裝地址嘅變數", "r1"), ("&x 攞地址；*p 搵個值", "r2"), ("*p = 99：改原本嘅變數", "r3"),
                                ("下集：指標 vs reference", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用指標參數寫一個 swapPtr，交換兩個 int；3.6 用 reference 寫過，比較吓有乜分別。"
          "[[next]]下一集：指標同 reference 有乜分別。多謝收睇，下次見！",
          EndCard("用指標參數寫 swapPtr(int* a, int* b)，交換兩個 int；同 3.6 嘅 reference 版本比較吓。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

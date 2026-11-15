#!/usr/bin/env python3
"""Video 52 (syllabus 5.1): 記憶體同地址

Memory as a street of numbered bytes; &a prints a real address (hexadecimal), different on every
run; the real addresses show a, b, d and c packed next to each other on the stack (4, 8 and 1
bytes apart); &c on a char really prints the letter, not an address, until it is cast to void*;
stack vs heap. Run `python3 video52.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 52
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-01"
FINAL = (CODE / "addr.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
CHAR = "    char c{'A'};\n"
CPRINT = "    std::cout << \"c: \" << static_cast<void*>(&c) << '\\n';\n"
V1 = FINAL.replace(CHAR, "").replace(CPRINT, "")
BAD = FINAL.replace("static_cast<void*>(&c)", "&c")
CC = "g++ -std=c++20 -Wall -Wextra addr.cpp -o addr"

(c1, r1, r1b, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"addr.cpp": V1}, [
    CC, "./addr", "./addr", Write("addr.cpp", BAD), "clear", CC, "./addr", Write("addr.cpp", FINAL), CC, "./addr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
addr = {k: int(v, 16) for k, v in (l.split(": ") for l in r3.output.strip().split("\n"))}
first = {k: v for k, v in (l.split(": ") for l in r1.output.strip().split("\n"))}
again = {k: v for k, v in (l.split(": ") for l in r1b.output.strip().split("\n"))}
assert first["a"] != again["a"], "the address did not change between runs"
assert int(first["a"], 16) - int(first["b"], 16) == 4 and int(first["b"], 16) - int(first["d"], 16) == 8
assert addr["a"] - addr["b"] == 4 and addr["b"] - addr["d"] == 8 and addr["d"] - addr["c"] == 1, addr
assert r2.output.strip().endswith("c: A") and c1.code == c2.code == c3.code == cch.code == 0
v = [int(x, 16) for x in rch.output.split()]
assert v[1] - v[0] == 4 and v[2] - v[1] == 4
shown = {k: int(v, 16) for k, v in first.items()}       # the addresses the viewer saw in the first run
low = lambda x: f"…{x & 0xff:02x}"                    # the last two hex digits, for the card

SAY = {"&a": "and a", "&": "and 號", "0x": "零 x", "&c": "and c", "static_cast<void*>": "static cast void pointer",
       "stack": "stack", "heap": "heap", "char": "char", "void*": "void pointer"}

s = Stage({"addr.cpp": V1}, title="記憶體同地址", code_px=24)

scenes = [
    Scene("intro",
          "歡迎嚟到第五章：指標同記憶體！第一步，要知道變數喺電腦記憶體入面，究竟住喺邊。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "byte · 地址 · & · stack · heap")),
    Scene("goal",
          "今集會講：[[b1]]記憶體係乜樣；[[b2]]用 and 號攞變數嘅地址；[[b3]]stack 同 heap 兩個區域。",
          BulletCard("今集學識", [("記憶體：一排 byte", "b1"), ("&x：x 嘅地址 address", "b2"), ("stack 同 heap", "b3")])),
    Scene("street",
          "記憶體好似一條好長好長嘅街：[[byte]]每個 byte 係一間屋，[[addr]]每間屋都有個門牌號碼，叫做地址。"
          "[[int]]一個 int 要四個 byte，就住咗連續四間屋；佢嘅地址，就係第一間嘅門牌。",
          BoxesCard("記憶體：一排 byte", [BoxRow(
              [Box("", "x" if i < 4 else "", f"100{i}", at=("byte", 0.1 * i), color=AMBER if i < 4 else BLUE, w=130)
               for i in range(8)], gap=0)], top=CONTENT_TOP + 60, box_h=110, size=48,
              notes=[("每個 byte 都有自己嘅地址（門牌）", "addr"), ("int x 佔 4 個 byte：地址係 1000", "int")])),
    Scene("print",
          "[[open]]三個變數：兩個 int，一個 double。[[amp]]喺變數前面加 and 號，就攞到佢嘅地址。[[cc]]編譯運行，"
          "[[o]]印出嚟係三個好長嘅數，零 x 開頭。零 x 即係十六進制，每次運行都可能唔同。",
          s.scene(Open("addr.cpp", at="open"), Mark((7, 9), at="amp"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("hex",
          "[[hex]]零 x 開頭，代表十六進制：除咗零至九，仲有 a 至 f，代表十至十五。地址好大，用十六進制寫短啲。"
          "[[again]]再運行多一次，[[o]]地址全部唔同咗：為咗安全，作業系統每次都會揀唔同嘅位置。",
          s.scene(Note("0x：十六進制\n0–9，再加 a–f（10–15）", at="hex", where="editor"), Note(None, at="again"),
                  Run(r1b, at="again", recall=True), Note("每次運行，地址都唔同", at="o", where="editor"))),
    Scene("layout",
          f"睇吓佢哋點排：[[a]]a 嘅地址尾係 {first['a'][-2:]}，[[b]]b 細咗四：一個 int 啱啱四個 byte；"
          "[[d]]d 再細八：double 佔八個 byte。[[stack]]函數入面嘅變數，就係咁樣一個貼一個，排喺一個叫 stack 嘅區域。",
          BoxesCard("main 入面嘅變數（真實地址）", [BoxRow([
              Box("d", "3.5", f"{low(shown['d'])} 起，8 byte", at="d", color=PURPLE, w=420),
              Box("b", "2", f"{low(shown['b'])} 起，4 byte", at="b", w=260),
              Box("a", "1", f"{low(shown['a'])} 起，4 byte", at="a", color=AMBER, w=260),
          ], gap=0)], top=CONTENT_TOP + 70, box_h=130, size=56,
              notes=[("地址由細到大：d → b → a，一個貼一個", "stack")])),
    Scene("char",
          "有個陷阱：[[type]]加一個 char，同樣印佢嘅地址。[[cc]]編譯運行，[[o]]印咗個 A 出嚟，唔係地址！"
          "[[why]]因為 char 嘅地址，cout 會當係一串文字嚟印。[[fix]]要先轉做 void 指標，[[run]]先會印出真正嘅地址。記住呢個陷阱：char 指標，cout 會當係字串。",
          s.scene(Note(None), Type("addr.cpp", CHAR, after="    double d{3.5};\n", at="type"),
                  Type("addr.cpp", CPRINT.replace("static_cast<void*>(&c)", "&c"), before="}", last=True), Expect("addr.cpp", BAD),
                  Run(c2, at="cc", recall=True), Run(r2), Note("char 嘅地址：\ncout 當佢係文字", at="why", where="editor"),
                  Note(None, at="fix"), Replace("addr.cpp", "<< &c <<", "<< static_cast<void*>(&c) <<", at="fix"),
                  Expect("addr.cpp", FINAL), Run(c3, at="run", recall=True), Run(r3))),
    Scene("heap",
          "記憶體主要有兩個區域：[[st]]stack 放函數入面嘅變數，自動分配，函數完咗就自動收返，好快，但係唔大；"
          "[[hp]]heap 就大好多，要用嘅時候先攞，5.7 會學點樣用 new 喺 heap 攞記憶體。",
          TileCard("stack 同 heap", [
              Tile("🥞", "stack", "函數入面嘅變數\n自動分配、自動收返\n快，但係細", "st", BLUE),
              Tile("🏗️", "heap", "大好多\n要用先攞（5.7 new）", "hp", PURPLE),
          ], cols=2, height=380)),
    Scene("recap",
          "總結：[[r1]]記憶體係一排 byte，每個都有地址；[[r2]]and 號攞變數嘅地址，用十六進制顯示；[[r3]]局部變數排喺 stack，一個貼一個；"
          "[[r4]]印 char 嘅地址，要先轉做 void 指標。",
          BulletCard("今集重點", [("記憶體：每個 byte 有地址", "r1"), ("&x：地址（0x 十六進制）", "r2"),
                                ("局部變數：stack，一個貼一個", "r3"), ("char 地址：static_cast<void*>", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]印出一個 vector 入面三個元素嘅地址，睇吓佢哋相差幾多。[[next]]下一集，我哋學點樣用變數記住一個地址：指標。"
          "多謝收睇，下次見！",
          EndCard("印出 vector<int> 入面 v[0]、v[1]、v[2] 嘅地址，睇吓佢哋相差幾多。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

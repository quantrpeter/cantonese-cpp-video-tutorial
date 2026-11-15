#!/usr/bin/env python3
"""Video 72 (syllabus 6.10): Move semantics

A Buffer of a million ints. Without a move constructor, std::move(a) really still copies ("copy"
printed twice): std::move only marks a as movable. A move constructor steals the pointer; one that
forgets to null the source really crashes (both destructors free it); the correct one prints "move" and
leaves a with size 0. Run `python3 video72.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 72
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-10"
FINAL = (CODE / "move.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
MOVE = "    Buffer(Buffer&& other) noexcept" + FINAL.split("    Buffer(Buffer&& other) noexcept")[1].split("    ~Buffer")[0]
NULLS = "        other.size_ = 0;\n        other.data_ = nullptr;\n"
V1 = FINAL.replace(MOVE, "")
BAD = FINAL.replace(NULLS, "")
CC = "g++ -std=c++20 -Wall -Wextra move.cpp -o mv"

(c1, r1, clr, c2, r2, c3, r3, cch, rch) = cpp.session({"move.cpp": V1}, [
    CC, "./mv", "clear", Write("move.cpp", BAD), CC, "./mv", Write("move.cpp", FINAL), CC, "./mv",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "copy 1000000 ints\ncopy 1000000 ints\n1000000 1000000\n", r1.output
assert r2.output.startswith("copy 1000000 ints\nmove\n") and r2.code != 0, r2.output
crash = r2.output.strip().split("\n")[-1]
assert r3.output == "copy 1000000 ints\nmove\n0 1000000\n" and c1.code == c2.code == c3.code == cch.code == 0
assert rch.output.strip() == "52 0", rch.output

SAY = {"std::move": "S T D move", "Buffer&&": "Buffer 兩個 and 號", "&&": "兩個 and 號", "noexcept": "no except",
       "lvalue": "L value", "rvalue": "R value", "nullptr": "null pointer", "double free": "double free", "move": "move"}

s = Stage({"move.cpp": V1}, title="Move semantics", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集嘅深複製，要將一百萬個數逐個抄一次，好慢。如果原本嗰個之後都唔再用，其實可以直接搬走佢嘅記憶體。今集學 move semantics。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "std::move · Buffer&& · 搬走")),
    Scene("goal",
          "今集會講：[[b1]]std::move 做咗乜；[[b2]]搬移建構子；[[b3]]搬完之後要做嘅一件事；[[b4]]被搬走嘅物件變成點。",
          BulletCard("今集學識", [("std::move", "b1"), ("搬移建構子 Buffer(Buffer&&)", "b2"), ("搬完：清空來源", "b3"),
                                ("被搬走：空但合法", "b4")])),
    Scene("v1",
          "[[open]]Buffer 有一百萬個 int，複製建構子會印 copy。[[main]]b 係 a 嘅副本；c 用 std::move(a) 建立。[[cc]]編譯運行，睇吓印咗乜：[[o]]兩次都係 copy！明明用咗 std::move，點解仲係複製？",
          s.scene(Open("move.cpp", at="open"), Mark((7, 13), at="open"), Mark((27, 29), at="main"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1), Note("std::move 都係 copy？", at="o", where="editor"))),
    Scene("what",
          "因為 std::move 本身乜都冇搬，[[mark]]佢只係貼一張標籤：呢個物件我唔再用，可以搬走。[[need]]要真係搬，class 要有一個搬移建構子；"
          "冇嘅話，就只可以退返去複製。",
          TileCard("std::move 做咗乜？", [
              Tile("📌", "貼標籤", "「a 我唔再用，可以搬」\n本身冇搬任何嘢", "mark", AMBER),
              Tile("🚚", "搬移建構子", "真正去搬嘅係佢\n冇就退返去複製", "need", BLUE),
          ], cols=2, height=360)),
    Scene("bad",
          "[[type]]搬移建構子，參數係 Buffer 兩個 and 號：一個可以搬嘅物件。[[steal]]佢唔 new，直接攞走對方嘅指標。[[cc]]編譯運行：[[o]]今次印 move，"
          "但係最後當機！",
          s.scene(Note(None), Run(clr, at="type"), Type("move.cpp", MOVE.replace(NULLS, ""), before="    ~Buffer", at="type", rate=50),
                  Expect("move.cpp", BAD), Mark(15, at="steal"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2), Note(f"{crash}！", at="o", where="editor"))),
    Scene("why",
          "因為 a 同 c 而家指住同一排記憶體：[[both]]兩個都會 delete，同一排記憶體還咗兩次。[[fix]]所以搬完之後，一定要將對方清空：size 變零，指標變 nullptr；"
          "delete nullptr 係安全嘅。",
          BoxesCard("搬完要清空來源", [
              BoxRow([Box("a.data_", [("地址", "both"), ("nullptr", "fix")], "被搬走", at="both", color=RED, w=280, key="a"),
                      Box("c.data_", "地址", "搬咗嚟", at="both", color=GREEN, w=280, key="c")], gap=200),
              BoxRow([Box("", "一百萬個 int", "heap", at="both", color=AMBER, w=420, key="h")]),
          ], arrows=[("c", "h", "both", GREEN)], top=CONTENT_TOP + 20, row_h=250, box_h=110, size=44,
              notes=[("a 變空：解構子 delete nullptr，安全", "fix")])),
    Scene("fixrun",
          "[[type]]加返兩句清空。[[cc]]再運行：[[o]]b 仲係 copy，但係 c 係 move：一百萬個數，一個都冇抄，只係搬咗個指標。a 嘅 size 變咗零，c 係一百萬。",
          s.scene(Note(None), Type("move.cpp", NULLS, after="data_{other.data_} {\n", at="type"), Expect("move.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("rules",
          "記住：[[m1]]std::move 只係話可以搬；[[m2]]搬移建構子攞走資源，再清空來源；[[m3]]加 noexcept，vector 先會放心用佢；"
          "[[m4]]被搬走嘅物件仲合法，但係唔好再靠佢入面嘅值，除非重新設定。",
          BulletCard("move 嘅規則", [("std::move：只係話可以搬", "m1"), ("搬移建構子：攞走，再清空來源", "m2"),
                                   ("加 noexcept", "m3"), ("被搬走：唔好再用佢嘅值", "m4")])),
    Scene("recap",
          "總結：[[r1]]複製大物件好慢；[[r2]]搬移建構子直接攞走對方嘅資源；[[r3]]一定要清空來源，唔係就 double free；"
          "[[r4]]std::move 將一個有名嘅物件標記做可以搬。",
          BulletCard("今集重點", [("複製大物件：慢", "r1"), ("Buffer(Buffer&&)：攞走資源", "r2"), ("清空來源", "r3"),
                                ("std::move：標記可以搬", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 std::move 將一個好長嘅 string，push_back 入 vector，印出 vector 入面嘅長度，同埋原本嗰個 string 嘅長度。"
          "[[next]]下一集：rule of zero，一個建構子都唔使寫。多謝收睇，下次見！",
          EndCard("用 std::move 將一個好長嘅 std::string push_back 入 vector，印出兩邊嘅長度。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

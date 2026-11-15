#!/usr/bin/env python3
"""Video 34 (syllabus 3.5): Reference 入門

`int nick = score;` is a copy (score stays 10); adding one & makes nick a second name for the
same box (both 15); changing score changes nick; `int& bad;` is a real "declared as reference
but not initialized" error. Run `python3 video3.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 34
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-05"
FINAL = (CODE / "ref.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
TAIL = "    score = 100;\n    std::cout << \"nick:  \" << nick << '\\n';\n"
V2 = FINAL.replace(TAIL, "")
V1 = V2.replace("int& nick", "int nick")
BAD = FINAL.replace("    int& nick = score;\n", "    int& nick = score;\n    int& bad;\n")
CC = "g++ -std=c++20 -Wall -Wextra ref.cpp -o ref"

(c1, r1, c2, r2, c3, r3, c4, cch, rch) = cpp.session({"ref.cpp": V1}, [
    CC, "./ref", Write("ref.cpp", V2), CC, "./ref", Write("ref.cpp", FINAL), CC, "./ref",
    Write("ref.cpp", BAD), CC,
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output.split() == ["score:", "10", "nick:", "15"] and r2.output.split() == ["score:", "15", "nick:", "15"]
assert r3.output.split()[-1] == "100"
assert "'bad' declared as reference but not initialized" in cpp.visible(c4.output), c4.output
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.split() == ["30", "30", "30"]

SAY = {"int&": "int and", "int& nick = score": "int and nick 等如 score", "int nick = score": "int nick 等如 score",
       "&": "and 號", "nick": "nick", "reference": "reference"}

s = Stage({"ref.cpp": V1}, title="Reference 入門")

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集見到，函數攞到嘅只係副本。今集學 reference：一個變數嘅第二個名。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int& · 第二個名")),
    Scene("goal",
          "今集會講：[[b1]]點樣用 int& 宣告 reference；[[b2]]佢同副本有乜分別；[[b3]]reference 一定要初始化。",
          BulletCard("今集學識", [("int&：reference 參考", "b1"), ("reference vs 副本", "b2"), ("一定要初始化", "b3")])),
    Scene("copy",
          "[[open]]先重溫副本：nick 等於 score，[[add]]然後 nick 加五。[[cc]]編譯運行，[[o]]score 仲係十，nick 係十五：兩個係唔同嘅盒。",
          s.scene(Open("ref.cpp", at="open"), Mark(5, at=("open", 0.6)), Mark(6, at="add"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("copy_boxes",
          "[[two]]int nick 等於 score，係開一個新嘅盒，將十複製入去；[[add]]之後 nick 加五，只係改佢自己個盒。",
          BoxesCard("int nick = score;：兩個盒", [BoxRow([
              Box("score", "10", "int", at="two", w=300),
              Box("nick", [("10", "two"), ("15", "add")], "int（副本）", at="two", color=AMBER, w=300),
          ], gap=160)], arrows=[("score", "nick", "two")], top=CONTENT_TOP + 90, box_h=150, size=64)),
    Scene("ref",
          "而家，[[amp]]喺 int 後面加一個 and 號，變成 int&。[[cc]]再編譯運行，[[o]]score 同 nick 都變咗十五！",
          s.scene(Type("ref.cpp", "&", before=" nick = score", at="amp"), Expect("ref.cpp", V2), Mark(5, at="amp"),
                  Run(c2, at="cc", recall=True), Run(r2), Mark(None, at="o"))),
    Scene("ref_box",
          "因為 reference 唔係新嘅盒，[[one]]只係同一個盒嘅第二個名。[[nick]]好似陳大文個花名叫阿文：叫邊個名，都係同一個人。"
          "[[add]]所以經 nick 加五，score 都會變。",
          BoxesCard("int& nick = score;：一個盒，兩個名", [BoxRow([
              Box("score / nick", [("10", "one"), ("15", "add")], "int", at="one", color=PURPLE, w=420),
          ])], top=CONTENT_TOP + 90, box_h=170, size=72, notes=[("reference：同一個盒嘅第二個名", "nick")])),
    Scene("back",
          "反過嚟都一樣：[[type]]將 score 改做一百，再印 nick。[[cc]]運行，[[o]]nick 都係一百。改邊個名，都係改同一個盒。",
          s.scene(Type("ref.cpp", TAIL, before="}", last=True, at="type", rate=20), Expect("ref.cpp", FINAL),
                  Run(c3, at="cc", recall=True), Run(r3))),
    Scene("anatomy",
          "[[t]]int& 讀做 int 嘅 reference；[[n]]nick 係新嘅名；[[s]]等號右邊，就係佢代表嘅變數。",
          AnatomyCard("int& nick = score;", [
              Part("int&", "int 嘅 reference", PURPLE, "t"),
              Part(" nick", "第二個名", BLUE, "n"),
              Part(" = score", "代表邊個變數", GREEN, "s"),
              Part(";", "", MUTED, "s"),
          ], size=84)),
    Scene("bad",
          "reference 一定要有對象。[[type]]如果淨係寫 int& bad，[[cc]]編譯就會出錯：bad 係 reference，但係冇初始化。"
          "[[fix]]刪走佢。",
          s.scene(Type("ref.cpp", "    int& bad;\n", after="    int& nick = score;\n", at="type"), Expect("ref.cpp", BAD),
                  Run(c4, at="cc", recall=True), Replace("ref.cpp", "    int& bad;\n", "", at="fix"), Expect("ref.cpp", FINAL))),
    Scene("rules",
          "記住三條規則：[[r1]]reference 宣告嗰陣一定要初始化；[[r2]]之後佢一直代表同一個變數，唔可以改做第二個嘅名；"
          "[[r3]]佢冇自己嘅盒，用佢就等於用原本個變數。",
          BulletCard("reference 嘅規則", [("宣告時一定要初始化", "r1"), ("一世代表同一個變數", "r2"), ("冇自己嘅盒", "r3")])),
    Scene("recap",
          "總結：[[r1]]int& 宣告 reference，即係第二個名；[[r2]]副本係新嘅盒，reference 係同一個盒；[[r3]]經 reference 改，原本嘅變數都會變。"
          "下一集，我哋將 reference 用喺函數參數上。",
          BulletCard("今集重點", [("int&：第二個名", "r1"), ("副本 = 新盒；reference = 同一個盒", "r2"),
                                ("經 reference 改，原本都變", "r3")])),
    Scene("outro",
          "小挑戰：[[ch]]為同一個變數整兩個 reference，經其中一個將值乘十，再印出三個名嘅值。"
          "[[next]]下一集：傳參考同 const reference。多謝收睇，下次見！",
          EndCard("為同一個變數整兩個 reference，經其中一個將值乘 10，再印出三個名嘅值。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

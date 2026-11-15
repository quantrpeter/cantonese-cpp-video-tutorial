#!/usr/bin/env python3
"""Video 57 (syllabus 5.6): const 同指標

const int* p: *p = 10 is a real "read-only location" error, but p can point elsewhere;
int* const q: *q = 10 works, but q = &b is a real "read-only variable" error; reading the type
from right to left. Run `python3 video57.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 57
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "05-06"
FINAL = (CODE / "cptr.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
L = FINAL.split("int main() {\n")[1].rsplit("}", 1)[0].splitlines(True)
SKEL = "#include <iostream>\n\nint main() {\n}\n"
B1 = SKEL.replace("}\n", "".join(L[:3]) + "    *p = 10;\n}\n")
V1 = SKEL.replace("}\n", "".join(L[:4]) + "}\n")
B2 = SKEL.replace("}\n", "".join(L[:6]) + "    q = &b;\n}\n")
CC = "g++ -std=c++20 -Wall -Wextra cptr.cpp -o cptr"

(c1, c2, clr, c3, c4, r4, cch, rch) = cpp.session({"cptr.cpp": B1}, [
    CC, Write("cptr.cpp", V1), CC, "clear", Write("cptr.cpp", B2), CC, Write("cptr.cpp", FINAL), CC, "./cptr",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "assignment of read-only location '* p'" in cpp.visible(c1.output), c1.output
assert "assignment of read-only variable 'q'" in cpp.visible(c3.output), c3.output
assert r4.output.strip() == "2 10" and c4.code == cch.code == 0 and rch.output.strip() == "72 85 64"

SAY = {"const int*": "const int pointer", "int* const": "int pointer const", "const int* p": "const int pointer p",
       "int* const q": "int pointer const q", "*p": "星 p", "*q": "星 q", "p = &b": "p 等如 and b", "q = &b": "q 等如 and b"}

s = Stage({"cptr.cpp": SKEL}, title="const 同指標", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！const 加喺指標身上，可以有兩個唔同嘅意思，視乎佢擺喺星號左邊定右邊。今集一次過搞清楚。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "const int* · int* const")),
    Scene("goal",
          "今集會講：[[b1]]const int 星號：唔可以經佢改個值；[[b2]]int 星號 const：唔可以轉對象；[[b3]]點樣由右到左讀。",
          BulletCard("今集學識", [("const int*：唔改個值", "b1"), ("int* const：唔轉對象", "b2"), ("由右到左讀", "b3")])),
    Scene("p1",
          "[[decl]]p 係 const int 星號，指住 a。[[set]]試吓經 p 改個值，星號 p 等於十。[[cc]]編譯：[[err]]出錯，p 指住嘅位置係唯讀！",
          s.scene(Open("cptr.cpp", mode="instant"), Type("cptr.cpp", "".join(L[:3]), before="}", last=True, at="decl", rate=26),
                  Type("cptr.cpp", "    *p = 10;\n", before="}", last=True, at="set"), Expect("cptr.cpp", B1), Run(c1, at="cc"),
                  Note("const int* p：\n唔可以經 p 改個值", at="err", where="editor"))),
    Scene("p2",
          "[[del]]刪走佢。[[move]]但係 p 本身可以轉對象：p 等於 and 號 b，冇問題。[[cc]]編譯，[[ok]]冇 error，只係警告 p 未用到，等陣會用。"
          "const 保護嘅係 p 指住嘅值，唔係 p 本身。",
          s.scene(Note(None), Replace("cptr.cpp", "    *p = 10;\n", "", at="del"), Type("cptr.cpp", L[3], before="}", last=True, at="move"),
                  Expect("cptr.cpp", V1), Run(c2, at="cc", recall=True))),
    Scene("q1",
          "另一種：[[decl]]q 係 int 星號 const，const 擺咗喺星號右邊。[[set]]經 q 改值，星號 q 等於十，冇問題；"
          "[[move]]但係想 q 轉去指 b，[[cc]]編譯：[[err]]出錯，q 本身係唯讀。",
          s.scene(Run(clr, at="decl"), Type("cptr.cpp", L[4], before="}", last=True, at="decl"), Type("cptr.cpp", L[5], before="}", last=True, at="set"),
                  Type("cptr.cpp", "    q = &b;\n", before="}", last=True, at="move"), Expect("cptr.cpp", B2), Run(c3, at="cc", recall=True),
                  Note("int* const q：\nq 唔可以轉對象", at="err", where="editor"))),
    Scene("run",
          "[[del]]刪走嗰句，[[print]]印出星號 p 同 a。[[cc]]運行，[[o]]p 指住 b，係二；a 經 q 改咗做十。兩個都同我哋預期一樣。",
          s.scene(Note(None), Replace("cptr.cpp", "    q = &b;\n", "", at="del"), Type("cptr.cpp", L[6], before="}", last=True, at="print"),
                  Expect("cptr.cpp", FINAL), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("read",
          "記法：由右到左讀。[[a]]const int 星號 p：p 係一個指標，指住一個 const int，所以個值唔改得；[[b]]int 星號 const q：q 係一個 const 指標，"
          "所以 q 自己唔改得；[[c]]兩樣都唔改得，就兩邊都加 const。",
          TableCard("由右到左讀", ["寫法", "讀法", "改 *p？", "改 p？"], [
              (["const int* p", "p 係指標，指住 const int", "唔得", "得"], "a"),
              (["int* const q", "q 係 const 指標，指住 int", "得", "唔得"], "b"),
              (["const int* const r", "兩樣都 const", "唔得", "唔得"], "c"),
          ], widths=[1.3, 1.8, 0.6, 0.6], code_cols=(0,), size=36)),
    Scene("use",
          "最常見嘅用法，係函數參數：[[param]]寫 const int 星號，就係承諾函數只會讀，唔會改你嘅資料，同 3.6 嘅 const reference 一樣。",
          CodeCompareCard("函數參數", [
              Pane("可能會改", "void printAll(int* a, int n);", False, "param"),
              Pane("承諾唔改", "void printAll(const int* a, int n);", True, "param"),
          ], size=30)),
    Scene("recap",
          "總結：[[r1]]const 喺星號左邊，保護指住嘅值；[[r2]]const 喺星號右邊，保護指標本身；[[r3]]由右到左讀；[[r4]]淨係讀嘅參數，用 const int 星號。",
          BulletCard("今集重點", [("const int*：值唔改得", "r1"), ("int* const：指標唔改得", "r2"), ("由右到左讀", "r3"),
                                ("唔改嘅參數：const int*", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 printAll，參數用 const int 星號，再喺入面試吓改第一個元素，睇吓 g++ 點講。"
          "[[next]]下一集，我哋學 new 同 delete：自己喺 heap 攞記憶體。多謝收睇，下次見！",
          EndCard("寫 printAll(const int* a, int n)；喺入面試吓改 a[0]，睇吓 g++ 點講。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

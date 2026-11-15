#!/usr/bin/env python3
"""Video 119 (syllabus 10.2): Preprocessor 同 macro

#define SQUARE(x) x * x really gives 5 for SQUARE(1 + 2), and `g++ -E` shows why (1 + 2 * 1 + 2);
a constexpr function gives 9. #ifdef DEBUG code only appears when built with -DDEBUG. A header
included twice without a guard is a real "redefinition of 'struct Point'" error; an #ifndef
include guard fixes it (prints 3). Run `python3 video10.2.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 119
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "10-02"
FILES = {f: (CODE / f).read_text() for f in ["macro.cpp", "point.h", "shape.h", "guard.cpp"]}
CHALLENGE = (CODE / "challenge.cpp").read_text()
POINT = FILES["point.h"]
GUARD_TOP, GUARD_END = "#ifndef POINT_H\n#define POINT_H\n\n", "\n#endif\n"
POINT0 = POINT.replace(GUARD_TOP, "").replace(GUARD_END, "")
START = dict(FILES, **{"point.h": POINT0})

(c1, r1, pre, c2, r2, clr, cg, clr2, cg2, rg, cch, rch) = cpp.session(START, [
    "g++ -std=c++20 -Wall -Wextra macro.cpp -o m", "./m", "g++ -E macro.cpp | tail -6", "g++ -std=c++20 -DDEBUG macro.cpp -o m", "./m",
    "clear", "g++ -std=c++20 -Wall -Wextra guard.cpp -o g", "clear", Write("point.h", POINT), "g++ -std=c++20 -Wall -Wextra guard.cpp -o g", "./g",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "5 9\n" and "1 + 2 * 1 + 2" in pre.output and r2.output == "5 9\ndebug build\n", (r1.output, r2.output)
assert "redefinition of 'struct Point'" in cpp.visible(cg.output) and cg.code != 0 and rg.output == "3\n"
assert c1.code == c2.code == cg2.code == cch.code == 0 and rch.output == "6 7\n"

SAY = {"#define": "define", "#ifdef": "if def", "#ifndef": "if n def", "#endif": "end if", "#include": "include", "#pragma once": "pragma once",
       "SQUARE": "大楷 square", "SQUARE(1 + 2)": "大楷 square 一加二", "square(1 + 2)": "square 一加二", "constexpr": "const expr",
       "-DDEBUG": "D DEBUG", "DEBUG": "DEBUG", "g++ -E": "g 加加 E", "POINT_H": "POINT H", "point.h": "point 點 h", "shape.h": "shape 點 h",
       "Point": "Point", "Line": "Line", "macro": "macro", "MAX": "大楷 max", "i++": "i 加加"}

s = Stage(START, title="Preprocessor 同 macro", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集見到，井號開頭嘅指令喺編譯之前已經處理咗。今集睇 preprocessor 識做乜：define、ifdef、include guard，同埋點解好多時 constexpr 會好過 macro。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "#define · #ifdef · include guard")),
    Scene("goal",
          "今集會講：[[b1]]macro 只係文字替換；[[b2]]佢嘅陷阱；[[b3]]ifdef 揀 code；[[b4]]include guard。",
          BulletCard("今集學識", [("#define：文字替換", "b1"), ("SQUARE(1 + 2) = ?", "b2"), ("#ifdef DEBUG", "b3"), ("include guard", "b4")])),
    Scene("macro",
          "[[def]]define SQUARE x，換做 x 乘 x。[[fn]]另一邊係一個 constexpr 函數 square。[[use]]兩個都計一加二嘅平方。[[cc]]編譯運行：[[o]]macro 得五！函數就係正確嘅九。點解會咁？",
          s.scene(Open("macro.cpp", at="def"), Mark(3, at="def"), Mark((5, 7), at="fn"), Mark((10, 11), at="use"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("why",
          "[[e]]用 g++ D E 睇吓預處理之後變成點：[[o]]SQUARE 一加二，變咗一加二乘一加二。macro 唔識數學，只係逐個字照抄，乘數行先，所以得五。",
          s.scene(Run(pre, at="e"), Note("macro：照抄文字\n1 + 2 * 1 + 2 = 5", at="o", where="editor"))),
    Scene("ifdef",
          "[[code]]ifdef DEBUG 到 endif 之間嘅 code，只有定義咗 DEBUG 先會保留。[[cc]]編譯時加 D DEBUG，就等於 define DEBUG。運行：[[o]]多咗一句 debug build。",
          s.scene(Note(None), Mark((12, 14), at="code"), Mark(None, at="cc"), Run(c2, at="cc"), Run(r2))),
    Scene("twice",
          "[[point]]point.h 定義 Point；[[shape]]shape.h 都 include 咗 point.h；[[main]]guard.cpp 兩個都 include。[[cc]]編譯：[[err]]錯誤，Point 重複定義：point.h 被貼咗兩次入嚟。",
          s.scene(Run(clr, at="point"), Open("point.h", at="point"), Open("shape.h", at="shape"), Mark(1, at="shape"), Open("guard.cpp", at="main"),
                  Mark((2, 3), at="main"), Mark(None, at="cc"), Run(cg, at="cc"), Scroll(at="err"))),
    Scene("guard",
          "[[type]]解決方法：include guard。ifndef POINT_H：如果未定義過，就 define 佢，再放內容；[[end]]第二次再 include，POINT_H 已經定義咗，成段就會跳過，唔會再定義多次。另一個寫法係一句 pragma once，效果一樣。",
          s.scene(Run(clr2, at="type"), Open("point.h", mode="instant"), Type("point.h", GUARD_TOP, before="struct Point", at="type", rate=60),
                  Type("point.h", "\n\n#endif", after="};", last=True, rate=30), Expect("point.h", POINT))),
    Scene("guardrun",
          "[[cc]]再編譯 guard.cpp，運行：[[o]]三。point.h 雖然 include 咗兩次，但係內容只會出現一次。",
          s.scene(Run(cg2, at="cc"), Run(rg))),
    Scene("rules",
          "建議：[[const]]常數同簡單函數，用 constexpr 代替 macro，有類型、有範圍；[[guard]]每個 header 都要有 include guard，或者用 pragma once；[[ifdef]]ifdef 留俾真係要分版本嘅地方。",
          TableCard("用 preprocessor 嘅建議", ["需要", "用"], [
              (["常數、小計算", "constexpr，唔用 #define"], "const", GREEN),
              (["header 重複 include", "#pragma once 或 #ifndef guard"], "guard"),
              (["分 debug / release", "#ifdef DEBUG"], "ifdef"),
          ], widths=[1.3, 1.7], code_cols=(), size=40)),
    Scene("recap",
          "總結：[[r1]]macro 只係文字替換，唔理運算次序；[[r2]]g++ D E 睇到展開之後嘅樣；[[r3]]ifdef 配合 D 選項揀 code；[[r4]]header 一定要有 include guard。",
          BulletCard("今集重點", [("#define：照抄文字", "r1"), ("g++ -E：睇展開", "r2"), ("#ifdef + -D", "r3"), ("include guard / #pragma once", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]有個 MAX macro，參數已經加晒括號。i 係五，m 等於 MAX i 加加同三。估吓印出 m 同 i 係幾多，再運行睇吓。[[next]]下一集：CMake 入門。多謝收睇，下次見！",
          EndCard("#define MAX(a, b) ((a) > (b) ? (a) : (b))；int i = 5; int m = MAX(i++, 3); 估 m 同 i，再運行（答案 6 7）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

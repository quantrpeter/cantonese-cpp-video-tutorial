#!/usr/bin/env python3
"""Video 81 (syllabus 7.1): 函數模板

Two copy-pasted maxOf overloads (int, double) really print 7 and 2.5. One function template
replaces both and also works for std::string (banana). maxOf(3, 2.5) is a real "deduced
conflicting types for parameter 'T' ('int' and 'double')" error; maxOf<double>(3, 2.5) prints 3.
Run `python3 video7.1.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 81
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "07-01"
FINAL = (CODE / "maxof.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BODY = " {\n    if (a > b) {\n        return a;\n    }\n    return b;\n}\n"
TEMPLATE = "template <typename T>\nT maxOf(T a, T b)" + BODY
INT_FN = "int maxOf(int a, int b)" + BODY
DBL_FN = "double maxOf(double a, double b)" + BODY
STR = "    std::string x = \"apple\", y = \"banana\";\n    std::cout << maxOf(x, y) << '\\n';\n"
LAST = "    std::cout << maxOf<double>(3, 2.5) << '\\n';\n"
V3 = FINAL.replace(LAST, "")
V1 = V3.replace("#include <string>\n", "").replace(STR, "").replace(TEMPLATE, INT_FN + "\n" + DBL_FN)
BAD = FINAL.replace("maxOf<double>(3, 2.5)", "maxOf(3, 2.5)")
CC = "g++ -std=c++20 -Wall -Wextra maxof.cpp -o mx"

(c1, r1, clr, c2, r2, c3, clr2, c4, r4, cch, rch) = cpp.session({"maxof.cpp": V1}, [
    CC, "./mx", "clear", Write("maxof.cpp", V3), CC, "./mx", Write("maxof.cpp", BAD), CC, "clear", Write("maxof.cpp", FINAL), CC, "./mx",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "7\n2.5\n" and r2.output == "7\n2.5\nbanana\n" and r4.output == "7\n2.5\nbanana\n3\n", (r1.output, r4.output)
assert "deduced conflicting types for parameter 'T' ('int' and 'double')" in cpp.visible(c3.output), c3.output[:500]
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "4\nb\n0.5\n"

SAY = {"template <typename T>": "template typename T", "template": "template", "typename": "typename", "maxOf": "max of",
       "maxOf<double>": "max of 角括號 double", "maxOf<int>": "max of 角括號 int", "maxOf<std::string>": "max of 角括號 string",
       "std::string": "S T D string", "T": "T", "minOf": "min of", "apple": "apple", "banana": "banana", "double": "double"}

s = Stage({"maxof.cpp": V1}, title="函數模板", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！第七部分講模板。如果同一個函數，要為 int、double、string 各寫一次，內容又一模一樣，好浪費。今集學函數模板：寫一次，乜嘢類型都用得。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "template <typename T> · maxOf")),
    Scene("goal",
          "今集會講：[[b1]]重複嘅多載；[[b2]]template typename T；[[b3]]編譯器點樣幫你生成函數；[[b4]]類型唔夾嘅時候點算。",
          BulletCard("今集學識", [("重複嘅多載", "b1"), ("template <typename T>", "b2"), ("實例化：編譯器生成", "b3"),
                                ("maxOf<double>(3, 2.5)", "b4")])),
    Scene("dup",
          "[[int]]一個 int 版本嘅 maxOf，[[dbl]]一個 double 版本，兩個除咗類型，一個字都冇分別。[[cc]]編譯運行，[[o]]七，二點五。"
          "想要 string 版本？又要抄多次。",
          s.scene(Open("maxof.cpp", at="int"), Mark((3, 8), at="int"), Mark((10, 15), at="dbl"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Run(r1))),
    Scene("tmpl",
          "[[del]]刪走 double 版本。[[type]]喺上面寫 template 角括號 typename T，[[t]]再將 int 全部換做 T。T 就係一個類型嘅位，用嘅時候先決定，"
          "可以係 int，可以係 double，乜都得。",
          s.scene(Run(clr, at="del"), Replace("maxof.cpp", "\n" + DBL_FN, "", at="del"),
                  Replace("maxof.cpp", "int maxOf(int a, int b)", "template <typename T>\nT maxOf(T a, T b)", at="type", rate=22),
                  Mark((3, 4), at="t"))),
    Scene("str",
          "[[str]]順手試吓 string：include string，整兩個字串，apple 同 banana，再叫 maxOf。一個 int 都冇改，只係多咗兩行。字串得唔得？",
          s.scene(Mark(None), Replace("maxof.cpp", "#include <iostream>\n", "#include <iostream>\n#include <string>\n", at="str"),
                  Type("maxof.cpp", STR, before="}", last=True, rate=24), Expect("maxof.cpp", V3))),
    Scene("run2",
          "[[cc]]編譯運行：[[o]]七，二點五，banana。同一個 maxOf，三種類型都用得。字串比較嘅係字典次序，banana 喺 apple 後面，所以大啲。",
          s.scene(Run(c2, at="cc", recall=True), Run(r2))),
    Scene("inst",
          "背後發生咩事？[[i]]編譯器見到 maxOf 三、七，[[d]]就知 T 係 int，自動生成一個 int 版本，[[s]]見到 double 同 string，又各自生成一個。"
          "呢個叫實例化。[[same]]即係話，抄嘅工夫由編譯器幫你做。",
          TableCard("實例化：編譯器幫你抄", ["呼叫", "T 係", "生成"], [
              (["maxOf(3, 7)", "int", "maxOf<int>"], "i"),
              (["maxOf(2.5, 1.5)", "double", "maxOf<double>"], "d"),
              (["maxOf(x, y)", "std::string", "maxOf<std::string>"], "s"),
          ], widths=[1.3, 1, 1.4], code_cols=(0, 1, 2), size=38, note=("寫一次，編譯器按需要生成", "same"))),
    Scene("mix",
          "[[type]]如果一個係 int，一個係 double 呢？[[cc]]編譯：[[err]]錯誤：T 推導出兩個唔同嘅類型，int 同 double，編譯器唔知揀邊個。",
          s.scene(Type("maxof.cpp", "    std::cout << maxOf(3, 2.5) << '\\n';\n", before="}", last=True, at="type"), Expect("maxof.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("explicit",
          "[[type]]解決方法：自己講明 T 係乜，喺函數名後面寫角括號 double。三會變成三點零。[[cc]]編譯運行，[[o]]三。",
          s.scene(Run(clr2, at="type"), Replace("maxof.cpp", "maxOf(3, 2.5)", "maxOf<double>(3, 2.5)", at="type"), Expect("maxof.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("need",
          "仲有一點：[[gt]]maxOf 入面用咗大過號，所以 T 一定要識比較大細。[[no]]如果傳一個唔識比較嘅類型入去，就會有錯誤，而且好長。7.4 嘅 concepts 會解決呢個問題。",
          BulletCard("T 要識做乜？", [("入面用咗 a > b：T 要識比較", "gt"), ("唔識：錯誤，好長（7.4 concepts 再講）", "no")])),
    Scene("recap",
          "總結：[[r1]]template typename T，寫一個通用嘅函數；[[r2]]編譯器睇參數推導 T，再生成對應版本；[[r3]]推導唔到，就用角括號講明；"
          "[[r4]]T 要支援函數入面用到嘅運算。",
          BulletCard("今集重點", [("template <typename T>", "r1"), ("推導 T，生成版本", "r2"), ("maxOf<double>(…)：講明", "r3"),
                                ("T 要識入面用到嘅運算", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 minOf 模板，試吓 int、char，同埋用角括號 double 比較一同零點五。[[next]]下一集：類別模板。多謝收睇，下次見！",
          EndCard("寫 template minOf：minOf(4, 9)、minOf('x', 'b')、minOf<double>(1, 0.5)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

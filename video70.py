#!/usr/bin/env python3
"""Video 70 (syllabus 6.8): 運算子多載

Vec2: `a + b` before operator+ exists is a real "no match for 'operator+'" error; operator+ as
a member function (4 6); operator<< as a free function so cout prints (4, 6); a defaulted
operator<=> (C++20) gives ==, < and friends: a == b is 0, a < b is 1. Run `python3 video70.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 70
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "06-08"
FINAL = (CODE / "vec.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
PLUS = "\n    Vec2 operator+(const Vec2& other) const {\n        return {x + other.x, y + other.y};\n    }\n"
CMP = "    auto operator<=>(const Vec2&) const = default;\n"
OUT = ("std::ostream& operator<<(std::ostream& out, const Vec2& v) {\n"
       "    return out << '(' << v.x << \", \" << v.y << ')';\n}\n\n")
PRINT_XY = "    std::cout << c.x << ' ' << c.y << '\\n';\n"
PRINT_C = "    std::cout << c << '\\n';\n"
CMPLINE = "    std::cout << (a == b) << ' ' << (a < b) << '\\n';\n"
V3 = FINAL.replace(CMP, "").replace(CMPLINE, "")
V2 = V3.replace(OUT, "").replace(PRINT_C, PRINT_XY)
V1 = V2.replace(PLUS, "")
CC = "g++ -std=c++20 -Wall -Wextra vec.cpp -o vec"

(c1, c2, r2, clr, c3, r3, c4, r4, cch, rch) = cpp.session({"vec.cpp": V1}, [
    CC, Write("vec.cpp", V2), CC, "./vec", "clear", Write("vec.cpp", V3), CC, "./vec", Write("vec.cpp", FINAL), CC, "./vec",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "no match for 'operator+'" in cpp.visible(c1.output), c1.output[:300]
assert r2.output == "4 6\n" and r3.output == "(4, 6)\n" and r4.output == "(4, 6)\n0 1\n"
assert c2.code == c3.code == c4.code == cch.code == 0 and rch.output.strip() == "(4, 5) (3, 6)"

SAY = {"operator+": "operator 加", "operator<<": "operator 兩個細過號", "operator<=>": "operator 太空船", "<=>": "太空船運算子",
       "Vec2": "Vec 二", "std::ostream": "S T D O stream", "ostream": "O stream", "default": "default", "a + b": "a 加 b"}

s = Stage({"vec.cpp": V1}, title="運算子多載", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！如果可以用加號，將兩個向量加埋，再用 cout 直接印出嚟，幾自然？今集學運算子多載。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "operator+ · operator<< · <=>")),
    Scene("goal",
          "今集會講：[[b1]]operator 加；[[b2]]operator 兩個細過號，用嚟印；[[b3]]C++20 嘅太空船運算子，一次過整晒比較。",
          BulletCard("今集學識", [("operator+", "b1"), ("operator<<：印出", "b2"), ("operator<=>：比較（C++20）", "b3")])),
    Scene("v1",
          "[[open]]Vec2 係一個二維向量，有 x 同 y。[[add]]main 想將 a 同 b 加埋。[[cc]]編譯：[[err]]出錯，冇一個加號識處理兩個 Vec2。",
          s.scene(Open("vec.cpp", at="open"), Mark((4, 7), at="open"), Mark(12, at="add"), Mark(None, at="cc"),
                  Run(c1, at="cc"), Scroll(at="err"))),
    Scene("plus",
          "[[type]]教 C++ 點樣加：寫一個成員函數，名叫 operator 加。[[other]]other 係加號右邊嗰個；左邊就係呼叫嘅物件自己。"
          "[[ret]]回傳一個新嘅 Vec2：x 加 x，y 加 y。[[cc]]編譯運行，[[o]]四同六。加號真係識加兩個 Vec2 喇。",
          s.scene(Type("vec.cpp", PLUS, after="    int y;\n", at="type", rate=40), Expect("vec.cpp", V2), Mark(8, at="other"),
                  Mark(9, at="ret"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("anatomy",
          "[[a]]a 加 b，C++ 會變成 a 點 operator 加，括號 b。所以運算子其實就係一個特別名嘅函數。",
          AnatomyCard("a + b 其實係……", [
              Part("a", "左邊：呼叫嘅物件", BLUE, "a"), Part(".operator+", "函數名", PURPLE, "a"),
              Part("(b)", "右邊：other", GREEN, "a"),
          ], size=80)),
    Scene("out",
          "想直接用 cout 印 c，[[fn]]就要寫 operator 兩個細過號。佢唔係成員函數，因為左邊係 cout，唔係 Vec2。[[ret]]印完要回傳 out，"
          "咁先可以繼續接落去印。[[cc]]編譯運行，[[o]]括號四逗號六。",
          s.scene(Run(clr, at="fn"), Type("vec.cpp", OUT, before="int main", at="fn", rate=40),
                  Replace("vec.cpp", PRINT_XY, PRINT_C, at="ret"), Expect("vec.cpp", V3), Run(c3, at="cc", recall=True), Run(r3))),
    Scene("cmp",
          "最後係比較。[[type]]C++20 有個太空船運算子，等於 default，編譯器就自動整晒等於、細過、大過呢啲比較，先比 x，再比 y。"
          "[[cc]]運行：[[o]]a 唔等於 b，係零；a 細過 b，係一。",
          s.scene(Type("vec.cpp", CMP, after="    }\n", at="type"), Type("vec.cpp", CMPLINE, before="}", last=True), Expect("vec.cpp", FINAL),
                  Run(c4, at="cc", recall=True), Run(r4))),
    Scene("rule",
          "一個提醒：[[like]]運算子要做佢應該做嘅嘢：加號就係加。[[bad]]如果加號偷偷做減數，用嘅人一定會出錯。",
          TileCard("運算子多載嘅規則", [
              Tile("✅", "似原本嘅意思", "+ 做加法，== 做比較", "like", GREEN),
              Tile("❌", "唔好亂嚟", "+ 偷偷做減數：害死人", "bad", RED),
          ], cols=2, height=330)),
    Scene("recap",
          "總結：[[r1]]運算子就係名叫 operator 嘅函數；[[r2]]operator 加，可以寫成成員函數；[[r3]]operator 兩個細過號，寫成普通函數，要回傳 out；"
          "[[r4]]C++20 嘅太空船運算子等於 default，一次過整晒比較。",
          BulletCard("今集重點", [("運算子：operator 函數", "r1"), ("operator+：成員函數", "r2"), ("operator<<：回傳 out", "r3"),
                                ("<=> = default：所有比較", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]為 Vec2 加減號，同埋乘一個整數。[[next]]下一集：物件嘅複製，同埋淺複製嘅陷阱。多謝收睇，下次見！",
          EndCard("為 Vec2 加 operator-（兩個向量相減）同 operator*（乘一個 int）。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

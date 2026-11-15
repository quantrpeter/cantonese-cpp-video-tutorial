#!/usr/bin/env python3
"""Video 105 (syllabus 8.18): string_view 同 span

countA(std::string_view) takes a std::string or a literal without copying: 3 3. total(std::span
<const int>) takes a vector or a C array: 6 15. The danger: a string_view made from a temporary
std::string really prints garbage, and AddressSanitizer really reports heap-use-after-free;
g++ -Wall says nothing. Run `python3 video8.18.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 105
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-18"
FINAL = (CODE / "view.cpp").read_text()
DANGLE = (CODE / "dangle.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
TOTAL = "int total" + FINAL.split("int total")[1].split("int main")[0]
SPANMAIN = "    std::vector<int> v{1, 2, 3};\n    int arr[] = {4, 5, 6};\n    std::cout << total(v) << ' ' << total(arr) << '\\n';\n"
V1 = FINAL.replace(TOTAL, "").replace(SPANMAIN, "").replace("#include <span>\n", "").replace("#include <vector>\n", "")
CC = "g++ -std=c++20 -Wall -Wextra view.cpp -o view"

(c1, r1, clr, c2, r2, clr2, cd, rd, ca, ra, cch, rch) = cpp.session({"view.cpp": V1, "dangle.cpp": DANGLE}, [
    CC, "./view", "clear", Write("view.cpp", FINAL), CC, "./view", "clear",
    "g++ -std=c++20 -Wall -Wextra dangle.cpp -o dg", "./dg", "g++ -std=c++20 -fsanitize=address dangle.cpp -o dg", "./dg",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "3 3\n" and r2.output == "3 3\n6 15\n", (r1.output, r2.output)
assert cd.output.strip() == "" and cd.code == 0 and "a temporary string, long enough" not in rd.output, rd.output
assert "heap-use-after-free" in ra.output and ra.code != 0
assert c1.code == c2.code == ca.code == cch.code == 0 and rch.output == "hello\n"

SAY = {"std::string_view": "S T D string view", "string_view": "string view", "std::span": "S T D span", "span": "span",
       "std::span<const int>": "span const int", "countA": "count A", "total": "total", "const std::string&": "const string reference",
       "heap-use-after-free": "heap use after free", "AddressSanitizer": "Address Sanitizer", "sv": "s v", "papaya": "papaya",
       "banana": "banana", "firstWord": "first word", "-Wall": "W all"}

s = Stage({"view.cpp": V1, "dangle.cpp": DANGLE}, title="string_view 同 span", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！有啲函數只係想睇一睇一段文字、一排數字，唔需要擁有佢哋。今集學兩個「只睇唔擁有」嘅類型：string_view 同 span，同埋佢哋最危險嘅地方。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "只睇唔擁有 · 懸空嘅危險")),
    Scene("goal",
          "今集會講：[[b1]]string_view 做參數；[[b2]]佢入面係乜；[[b3]]span 睇一排數；[[b4]]view 懸空。",
          BulletCard("今集學識", [("string_view 參數", "b1"), ("指標 + 長度", "b2"), ("span<const int>", "b3"), ("危險：懸空 view", "b4")])),
    Scene("sv",
          "[[fn]]countA 數有幾多個 a，參數係 string_view。[[call]]傳一個 std::string 得，[[lit]]直接傳雙引號字串都得，而且唔會整一個新 string 出嚟複製。"
          "[[cc]]編譯運行，[[o]]三同三：banana 同 papaya 都有三個 a。一個字都冇複製過。",
          s.scene(Open("view.cpp", at="fn"), Mark(5, at="fn"), Mark(18, at="call"), Mark(19, at="lit"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("inside",
          "[[ptr]]string_view 入面得兩樣嘢：一個指住文字嘅指標，同埋長度。[[own]]文字唔係佢嘅，佢只係借嚟睇。[[cheap]]所以複製一個 string_view 好平。",
          BoxesCard("std::string_view", [
              BoxRow([Box("指標", "→", "", at="ptr", color=PURPLE, w=200, key="p"), Box("長度", "6", "", at="ptr", color=PURPLE, w=200)], gap=20,
                     label="string_view"),
              BoxRow([Box("", "b a n a n a", "word 嘅文字（唔係佢嘅）", at="own", color=BLUE, w=520, key="t")]),
          ], arrows=[("p", "t", "own", PURPLE)], notes=[("複製好平：兩個數", "cheap")], top=CONTENT_TOP + 10, row_h=260, box_h=110, size=40)),
    Scene("span",
          "[[type]]span 係一排數嘅版本：total 收一個 span const int，[[call]]vector 同 C 陣列都傳得入去，仲知道有幾多個，唔會好似 4.5 咁退化。[[cc]]運行，[[o]]六同十五：一加二加三，四加五加六。同一個函數，兩種容器。",
          s.scene(Run(clr, at="type"), Replace("view.cpp", "#include <iostream>\n", "#include <iostream>\n#include <span>\n", at="type", rate=40),
                  Replace("view.cpp", "#include <string_view>\n", "#include <string_view>\n#include <vector>\n", rate=40),
                  Type("view.cpp", TOTAL, before="int main", rate=60), Type("view.cpp", SPANMAIN, before="}", last=True, at="call", rate=50),
                  Expect("view.cpp", FINAL), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("dangle",
          "危險嚟喇。[[open]]sv 由一個臨時 string 整出嚟；呢句完咗，臨時 string 就消失，sv 指住嘅記憶體已經還咗。[[cc]]編譯：冇任何警告。運行：[[o]]印出一堆垃圾！前面嘅字已經俾人改咗。",
          s.scene(Run(clr2, at="open"), Open("dangle.cpp", at="open"), Mark((6, 7), at="open"), Mark(None, at="cc"), Run(cd, at="cc"), Run(rd, at="o"))),
    Scene("asan",
          "[[cc]]用 address sanitizer：[[o]]heap use after free：讀咗一塊已經還咗嘅記憶體。同 5.4 嘅懸空指標一樣。",
          s.scene(Run(ca, at="cc"), Run(ra, at="o"), Scroll(at="o"))),
    Scene("rules",
          "規則：[[param]]string_view 同 span 最適合做函數參數；[[store]]唔好用佢哋保存臨時嘢；[[ret]]唔好回傳指住函數入面局部變數嘅 view。要保存，就用 string 同 vector。",
          TableCard("view 點用先安全", ["做法", "安全？"], [
              (["做函數參數", "安全"], "param", GREEN),
              (["string_view sv = std::string{…};", "懸空！"], "store", RED),
              (["return 指住局部 string 嘅 view", "懸空！"], "ret", RED),
          ], widths=[1.9, 0.8], code_cols=(), size=38)),
    Scene("recap",
          "總結：[[r1]]string_view 同 span 只睇唔擁有；[[r2]]做參數，乜都收得，又唔使複製；[[r3]]原本嘅資料消失，view 就懸空；[[r4]]-Wall 都未必警告，要靠 sanitizer 同小心。",
          BulletCard("今集重點", [("只睇唔擁有", "r1"), ("最啱做參數", "r2"), ("原資料冇咗 → 懸空", "r3"), ("-Wall 未必捉到", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 firstWord，收一個 string_view，回傳第一個空格之前嘅部分。[[next]]下一集：std::format 同 std::print。多謝收睇，下次見！",
          EndCard("寫 std::string_view firstWord(std::string_view s)：用 s.substr(0, s.find(' '))；firstWord(\"hello world\") 係 hello。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

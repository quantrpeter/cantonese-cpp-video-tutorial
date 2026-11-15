#!/usr/bin/env python3
"""Video 89 (syllabus 8.2): Iterator

An explicit begin()/end() loop with *it and ++it really prints 72 64 91. Writing through an
iterator (*it = 80) and jumping (it += 2) really prints 80 91. A std::list iterator cannot jump:
lt += 2 is a real "no match for 'operator+='" error; ++lt and std::next work (2 3). Iterator
categories explain why. Run `python3 video89.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 89
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-02"
FINAL = (CODE / "iter.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
JUMP = "    auto it = marks.begin();\n    *it = 80;\n    it += 2;\n    std::cout << marks[0] << ' ' << *it << '\\n';\n"
GOOD = "    ++lt;\n    std::cout << *lt << ' ' << *std::next(lt) << '\\n';\n"
BADL = "    lt += 2;\n    std::cout << *lt << '\\n';\n"
LIST = "    std::list<int> nums{1, 2, 3};\n    auto lt = nums.begin();\n" + GOOD
INCS = "#include <iterator>\n#include <list>\n"
BAD = FINAL.replace(GOOD, BADL)
V2 = FINAL.replace(LIST, "").replace(INCS, "")
V1 = V2.replace(JUMP, "")
CC = "g++ -std=c++20 -Wall -Wextra iter.cpp -o it"

(c1, r1, c2, r2, clr, c3, clr2, c4, r4, cch, rch) = cpp.session({"iter.cpp": V1}, [
    CC, "./it", Write("iter.cpp", V2), CC, "./it", "clear", Write("iter.cpp", BAD), CC, "clear", Write("iter.cpp", FINAL), CC, "./it",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert r1.output == "72 64 91 \n" and r2.output == "72 64 91 \n80 91\n" and r4.output == "72 64 91 \n80 91\n2 3\n", r4.output
assert "no match for 'operator+='" in cpp.visible(c3.output) and "_List_iterator<int>" in cpp.visible(c3.output)
assert c1.code == c2.code == c4.code == cch.code == 0 and rch.output == "91 64 72 \n"

SAY = {"*it": "星 it", "++it": "加加 it", "it += 2": "it 加等於二", "it != marks.end()": "it 唔等於 end", "it": "it", "lt": "l t",
       "++lt": "加加 l t", "lt += 2": "l t 加等於二", "std::next": "S T D next", "std::list": "S T D list", "begin()": "begin",
       "end()": "end", "rbegin": "r begin", "rend": "r end", "auto": "auto", "iterator": "iterator", "random access": "random access"}

s = Stage({"iter.cpp": V1}, title="Iterator", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集講，演算法經 iterator 去行容器。今集睇清楚 iterator 本身：佢點樣指住元素、點樣行、點樣改，同埋點解唔係個個 iterator 都識跳。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "begin · end · *it · ++it")),
    Scene("goal",
          "今集會講：[[b1]]用 iterator 寫迴圈；[[b2]]經 iterator 改元素；[[b3]]iterator 嘅種類；[[b4]]range-based for 其實係乜。",
          BulletCard("今集學識", [("begin、end、*it、++it", "b1"), ("*it = 80", "b2"), ("iterator 種類", "b3"), ("range-for 嘅真面目", "b4")])),
    Scene("loop",
          "[[it]]it 由 begin 開始，[[cond]]只要未去到 end，就繼續；[[star]]星號 it 攞到佢指住嘅元素，[[pp]]加加 it 行去下一個。"
          "[[cc]]編譯運行，[[o]]七十二、六十四、九十一，逐個行晒，同用 index 嘅效果一樣。",
          s.scene(Open("iter.cpp", at="it"), Mark(6, at="it"), Mark(7, at="star"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("ptr",
          "iterator 用起嚟好似指標：[[deref]]星號攞值，[[inc]]加加行下一格，[[cmp]]唔等於用嚟比較位置。[[end]]記住 end 係最後一個再後一格，唔可以用星號攞值。",
          TableCard("iterator 識做乜", ["寫法", "意思"], [
              (["*it", "攞（或者改）指住嘅元素"], "deref"),
              (["++it", "行去下一個"], "inc"),
              (["it != end", "仲未行完"], "cmp"),
              (["*end()", "唔得！end 冇元素"], "end", RED),
          ], widths=[1, 1.8], code_cols=(0,), size=40)),
    Scene("write",
          "[[type]]iterator 仲可以改嘢：it 指住第一個，星號 it 等於八十；[[jump]]it 加等於二，一下跳兩格，去到九十一。[[cc]]編譯運行，[[o]]第一個變咗八十，it 指住九十一。",
          s.scene(Type("iter.cpp", JUMP, before="}", last=True, at="type", rate=40), Expect("iter.cpp", V2), Mark(11, at="type"), Mark(12, at="jump"),
                  Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("list",
          "[[type]]換做 std::list，試吓一樣跳兩格。[[cc]]編譯：[[err]]錯誤！list 嘅 iterator 冇加等於，唔可以一下跳兩格。點解 vector 得，list 唔得？",
          s.scene(Run(clr, at="type"), Replace("iter.cpp", "#include <iostream>\n", "#include <iostream>\n" + INCS, at="type", rate=40),
                  Type("iter.cpp", LIST.replace(GOOD, BADL), before="}", last=True, rate=40), Expect("iter.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="err"))),
    Scene("cats",
          "因為 list 嘅元素唔係連埋一齊，要跳兩格，只可以一格一格咁行。所以 iterator 分幾種：[[fwd]]淨係識向前；[[bi]]識前後行，好似 list；"
          "[[ra]]識隨意跳，好似 vector。",
          TableCard("iterator 種類", ["種類", "識做", "例子"], [
              (["forward", "++", "forward_list"], "fwd"),
              (["bidirectional", "++ --", "list · map · set"], "bi"),
              (["random access", "++ -- += []", "vector · deque · array"], "ra", GREEN),
          ], widths=[1.2, 1.1, 1.5], code_cols=(0, 1, 2), size=36)),
    Scene("next",
          "[[type]]list 就用加加 it，一次行一格；[[nx]]或者用 std::next，攞下一格，佢自己會一格格咁行。[[cc]]編譯運行，[[o]]二同三。",
          s.scene(Run(clr2, at="type"), Replace("iter.cpp", BADL, GOOD, at="type", rate=30), Expect("iter.cpp", FINAL), Mark(18, at="type"),
                  Mark(19, at="nx"), Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("rangefor",
          "[[rf]]你成日寫嘅 range-based for，[[same]]其實就係呢個 iterator 迴圈嘅簡寫：編譯器幫你寫 begin、end、加加同星號。",
          CodeCard("range-for 嘅真面目", "for (int m : marks) {\n    use(m);\n}\n\n// 等於\nfor (auto it = marks.begin(); it != marks.end(); ++it) {\n    int m = *it;\n    use(m);\n}",
                   name="range-for", marks=[((1, 3), "你寫嘅", "rf"), ((6, 9), "編譯器變成嘅", "same", GREEN)], size=30)),
    Scene("recap",
          "總結：[[r1]]begin 到 end，包頭唔包尾；[[r2]]星號攞值，加加行下一格；[[r3]]vector 嘅 iterator 識跳，list 嘅唔識，要用 std::next；"
          "[[r4]]range-for 就係 iterator 迴圈嘅簡寫。",
          BulletCard("今集重點", [("begin() … end()", "r1"), ("*it、++it", "r2"), ("random access vs bidirectional", "r3"),
                                ("range-for = iterator 迴圈", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 rbegin 同 rend，由尾到頭印出 vector。[[next]]下一集：vector 深入。多謝收睇，下次見！",
          EndCard("用 marks.rbegin() 同 marks.rend() 寫迴圈，由尾到頭印出 marks，應該係 91、64、72。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

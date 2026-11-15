#!/usr/bin/env python3
"""Video 153 (syllabus 13.5): 圖書館管理系統（二）：完成

The finished library (header-only library.h): search by part of a title, borrow and giveBack that
throw on misuse (already borrowed, no such member, no such book), save to a CSV file. The real demo
prints the two "Harbour" books, then "error: already borrowed" and "error: no such book";
`cat books.csv` shows book 1 borrowed by member 1. doctest tests (test.cpp) really pass: 2 test
cases, 6 assertions. Run `python3 video13.5.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 153
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "13-05"
FILES = {f: (CODE / f).read_text() for f in ["library.h", "main.cpp", "test.cpp"]}
DOCTEST = (CODE / "doctest.h").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
LIB = FILES["library.h"].split("\n")


def ln(text, start=1, lines=LIB):
    return next(i + 1 for i in range(start - 1, len(lines)) if text in lines[i])


(c1, r1, cat, ct, rt, cch, rch) = cpp.session({**FILES, "doctest.h": DOCTEST}, [
    "g++ -std=c++20 -Wall -Wextra main.cpp -o lib", "./lib", "cat books.csv", "g++ -std=c++20 test.cpp -o test", "./test",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=58)
assert r1.output == "1 Harbour Stories\n3 Harbour Food\nerror: already borrowed\nerror: no such book\n", r1.output
assert cat.output == "1,Harbour Stories,Chan,1\n2,Night Market,Wong,0\n3,Harbour Food,Chan,0\n"
assert "2 passed | 0 failed" in cpp.visible(rt.output) and "SUCCESS" in cpp.visible(rt.output)
assert c1.code == ct.code == cch.code == 0 and "3 passed | 0 failed" in cpp.visible(rch.output)

SAY = {"library.h": "library 點 h", "main.cpp": "main 點 c p p", "test.cpp": "test 點 c p p", "search": "search", "borrow": "borrow",
       "giveBack": "give back", "save": "save", "find": "find", "books.csv": "books 點 c s v", "doctest": "doc test", "CHECK_THROWS": "CHECK THROWS",
       "CHECK_THROWS_AS": "CHECK THROWS AS", "std::invalid_argument": "invalid argument", "std::out_of_range": "out of range",
       "Harbour": "Harbour", "value_or(0)": "value or 零", "contains": "contains", "cat": "cat"}

s = Stage(FILES, title="圖書館系統（二）：完成", code_px=19)

scenes = [
    Scene("intro",
          "歡迎返嚟！圖書館系統第二集，亦都係最後一個項目：加埋搵書、借書還書、存檔，仲要寫測試，確保將來改 code 都唔會整壞。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "搵書 · 借還 · 存檔 · 測試")),
    Scene("goal",
          "今集會講：[[b1]]search；[[b2]]borrow 同 giveBack，錯就 throw；[[b3]]save 成 CSV；[[b4]]用 doctest 測試。",
          BulletCard("今集學識", [("search(字)", "b1"), ("borrow / giveBack + exception", "b2"), ("save → CSV", "b3"), ("doctest 測試", "b4")])),
    Scene("search",
          "[[open]]library.h 包晒成個 Library。[[search]]search 逐本書睇書名有冇包含個字，有就記低編號，用 4.7 嘅 find 同 npos。",
          s.scene(Open("library.h", mode="instant"), Mark((ln("std::vector<int> search"), ln("return found;") + 1), at="search"))),
    Scene("borrow",
          "[[find]]borrow 先用 find 搵書，搵唔到 find 會 throw out_of_range；[[member]]會員唔存在，throw invalid_argument；[[taken]]已經借咗，throw runtime_error；[[ok]]全部冇問題，先記低借咗俾邊個。"
          "[[back]]giveBack 就將佢清返。",
          s.scene(Mark((ln("Book& find(int id)"), ln('throw std::out_of_range("no such book");')), at="find"),
                  Mark((ln("if (!members_.contains(memberId))"), ln('throw std::invalid_argument')), at="member"),
                  Mark((ln("if (b.borrowedBy)"), ln('throw std::runtime_error("already borrowed");')), at="taken"),
                  Mark(ln("b.borrowedBy = memberId;"), at="ok"), Mark((ln("void giveBack"), ln("b.borrowedBy.reset();")), at="back"))),
    Scene("save",
          "[[save]]save 用 ofstream，每本書一行：編號、書名、作者，最後係借書人嘅編號；冇人借就寫零，value_or 零。",
          s.scene(Mark((ln("void save"), ln("out << b.borrowedBy.value_or(0)")), at="save"))),
    Scene("demo",
          "[[open]]main.cpp：加三本書同 Amy，搵 Harbour，Amy 借第一本，再試借多次，同埋借一本唔存在嘅書。[[cc]]編譯運行：[[o]]搵到兩本 Harbour；第二次借，already borrowed；九十九號，no such book。[[cat]]books.csv：第一本記住俾一號會員借咗。",
          s.scene(Mark(None), Open("main.cpp", at="open"), Run(c1, at="cc"), Run(r1, at="o"), Run(cat, at="cat"))),
    Scene("tests",
          "[[open]]test.cpp 用 10.5 嘅 doctest：[[t1]]借書之後 borrowedBy 係 Amy；再借一定要 throw；還咗之後冇人借；再還又要 throw。[[t2]]search 搵到一本，亂打就搵唔到。[[cc]]編譯測試要等一陣，因為 doctest 個 header 幾大。運行：[[o]]兩個 test case、六個檢查，全部 pass。以後改 library，先跑一次測試就安心。",
          s.scene(Open("test.cpp", mode="instant"), Mark((5, 15), at="t1"), Mark((17, 23), at="t2"), Mark(None, at="cc"), Run(ct, at="cc"), Run(rt, at="o"))),
    Scene("parts",
          "成個系統用咗：[[a]]class 同封裝；[[b]]vector、map、optional；[[c]]exception 處理錯誤；[[d]]檔案；[[e]]單元測試。",
          TableCard("圖書館系統用咗乜", ["技巧", "喺邊度"], [
              (["class、private", "Library"], "a"),
              (["vector、map、optional", "books_、members_、borrowedBy"], "b"),
              (["exception", "borrow、giveBack、find"], "c"),
              (["ofstream", "save"], "d"),
              (["doctest", "test.cpp"], "e"),
          ], widths=[1.4, 1.8], code_cols=(), size=34)),
    Scene("recap",
          "總結：[[r1]]用編號連結書同會員；[[r2]]用 exception 處理錯誤操作；[[r3]]CSV 簡單易讀；[[r4]]測試保護你嘅 code。兩個綜合項目都完成咗！",
          BulletCard("今集重點", [("編號連結", "r1"), ("錯誤 → exception", "r2"), ("CSV 存檔", "r3"), ("測試", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]加一個測試：借書俾唔存在嘅會員，要 throw invalid_argument。[[next]]最後一集：學完 C++，下一步去邊？多謝收睇，下次見！",
          EndCard("加 TEST_CASE(\"unknown member\")：CHECK_THROWS_AS(lib.borrow(b, 42), std::invalid_argument)。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

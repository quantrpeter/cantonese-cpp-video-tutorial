#!/usr/bin/env python3
"""Video 8 (syllabus 1.2): 初始化

An uninitialised total really prints garbage (with g++'s -Wuninitialized warning), `= 0` fixes
it; `=` vs `{}`; `int price = 9.99` silently becomes 9, `int price{9.99}` is a narrowing error,
and `double` is the right type. Run `python3 video8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 8
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-02"
TOTAL = (CODE / "total.cpp").read_text()
PRICE = (CODE / "price.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
NOINIT = TOTAL.replace("int total = 0;", "int total;")
P_EQ = PRICE.replace("double price{9.99};", "int price = 9.99;")
P_BRACE = PRICE.replace("double price{9.99};", "int price{9.99};")
CC = "g++ -std=c++20 -Wall -Wextra total.cpp -o total"
CP = "g++ -std=c++20 -Wall -Wextra price.cpp -o price"

(c1, r1, c2, r2, clr, p1, pr1, p2, p3, pr3, cch, rch) = cpp.session({"total.cpp": NOINIT, "price.cpp": P_EQ}, [
    CC, "./total",
    Write("total.cpp", TOTAL), CC, "./total",
    "clear", CP, "./price",
    Write("price.cpp", P_BRACE), CP,
    Write("price.cpp", PRICE), CP, "./price",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)

bad_total = int(r1.output.split("Total:")[1])
garbage = bad_total - 175
assert garbage != 0, "the uninitialised total happened to be 0; change the program so the video shows garbage"
assert "'total' is used uninitialized" in cpp.visible(c1.output) and c2.output.strip() == ""
assert "Total: 175" in r2.output and pr1.output.strip() == "Price: 9" and pr3.output.strip() == "Price: 9.99"
assert "narrowing conversion" in cpp.visible(p2.output) and p2.code != 0 and p1.output.strip() == ""
assert cch.code == 0 and "36.6" in rch.output

SAY = {"int total = 0": "int total 等如零", "int total{0}": "int total 大括號零", "int total{}": "int total 空大括號",
       "int price = 9.99": "int price 等如九點九九"}

s = Stage({"total.cpp": NOINIT, "price.cpp": P_EQ}, title="初始化")

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集我哋整咗第一個變數。今集講一個好容易忽略、但係好重要嘅習慣：初始化。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "= · {} · 垃圾值")),
    Scene("goal",
          "今集會講：[[b1]]變數唔初始化，會發生咩事；[[b2]]初始化嘅兩種寫法：等號同大括號；[[b3]]點解大括號更安全。",
          BulletCard("今集學識", [("唔初始化會點", "b1"), ("兩種寫法：= 同 {}", "b2"), ("點解 {} 更安全", "b3")])),
    Scene("bug",
          "[[open]]我哋買咗兩件嘢，所以 count 係二；total 用嚟加埋兩個價錢，但係宣告嗰陣，冇俾佢初始值。"
          "[[cc]]編譯，[[warn]]g++ 已經警告：total 未初始化就用咗。[[run]]照運行睇吓，"
          f"[[out]]total 竟然係{zh_int(bad_total)}！",
          s.scene(Open("total.cpp", at="open"), Mark(5, at=("open", 1.2)), Run(c1, at="cc"),
                  Note("warning：total 未初始化\n就已經用咗", at="warn", where="editor"), Run(r1, at="run"))),
    Scene("garbage",
          "點解？宣告變數，只係喺記憶體搵個位俾佢。[[old]]如果冇放值入去，個位入面係之前留低嘅數字，叫做垃圾值。"
          "[[add]]再加八十同九十五，就變咗呢個古怪數字。[[luck]]有時個垃圾值啱啱係零，睇落冇問題，但係下次就未必。",
          BoxesCard("冇初始化 = 垃圾值", [BoxRow([
              Box("count", "2", "int", at=None),
              Box("total", [("?", None), (str(garbage), "old"), (str(bad_total), "add")], "int", at=None, color=RED),
          ], gap=120)], box_h=150, size=64, top=CONTENT_TOP + 60,
              notes=[("之前留低嘅數字：垃圾值 garbage", "old"), (f"{garbage} + 80 + 95 = {bad_total}", "add")],
              footer=("有時啱啱係 0，下次就未必", "luck"))),
    Scene("fix",
          "解決方法好簡單：[[fix]]宣告嗰陣，就俾佢一個初始值：零。[[cc]]再編譯，[[ok]]警告冇咗；[[run]]運行，"
          "total 係一百七十五，啱晒。",
          s.scene(Note(None), Replace("total.cpp", "int total;", "int total = 0;", at="fix"), Mark(None),
                  Expect("total.cpp", TOTAL), Run(c2, at="cc", recall=True), Run(r2, at="run"))),
    Scene("ways",
          "初始化有兩種常見寫法。[[eq]]第一種用等號：int total = 0。[[brace]]第二種用大括號：int total{0}。"
          "[[empty]]大括號入面乜都唔寫，就係零。[[same]]三句嘅意思都一樣。",
          TableCard("初始化嘅寫法", ["寫法", "意思"], [
              (["int total = 0;", "用等號，初始值係 0"], "eq"),
              (["int total{0};", "用大括號，初始值係 0"], "brace"),
              (["int total{};", "空嘅大括號：初始值都係 0"], "empty"),
          ], widths=[1, 1.3], size=44, note=("三句都係 total = 0", "same"))),
    Scene("narrow1",
          "咁點解要學埋大括號？睇吓呢個例子。[[open]]價錢係九點九九，但係我哋用咗 int。[[cc]]編譯運行，"
          "[[out]]印出九。小數部分無聲無息咁冇咗，連警告都冇。",
          s.scene(Run(clr), Open("price.cpp", at="open"), Mark(4, at=("open", 1.0)), Run(p1, at="cc"), Run(pr1),
                  Note("9.99 變咗 9\n連警告都冇！", at="out", where="editor"))),
    Scene("narrow2",
          "[[fix]]改用大括號，[[cc]]再編譯。[[err]]今次 g++ 唔肯編譯，佢話 narrowing，即係收窄："
          "九點九九放入 int，會唔見咗啲資料。[[catch]]大括號會幫你捉到呢種錯誤。",
          s.scene(Note(None), Replace("price.cpp", "price = 9.99", "price{9.99}", at="fix"), Expect("price.cpp", P_BRACE),
                  Run(p2, at="cc", recall=True), Note("narrowing ＝ 收窄\n{} 幫你捉到", at="catch", where="editor"))),
    Scene("narrow3",
          "要裝小數，就要用另一個型別：double。[[fix]]將 int 改做 double，[[cc]]編譯運行，[[out]]今次係九點九九。"
          "double 下一集會詳細講。",
          s.scene(Note(None), Replace("price.cpp", "int price", "double price", at="fix"), Expect("price.cpp", PRICE),
                  Run(p3, at="cc", recall=True), Run(pr3))),
    Scene("recap",
          "總結：[[r1]]冇初始化嘅變數，入面係垃圾值；[[r2]]所以每個變數，宣告嗰陣就要初始化；"
          "[[r3]]可以用等號，或者大括號；[[r4]]大括號仲會捉到收窄，例如將小數放入 int。",
          BulletCard("今集重點", [("冇初始化：入面係垃圾值", "r1"), ("每個變數都要初始化", "r2"),
                                ("= 0 或者 {0}、{}", "r3"), ("{} 會捉到收窄 narrowing", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個變數 temperature，用大括號初始化做三十六點六，睇吓 g++ 點講，再改啱佢個型別。"
          "[[next]]下一集，我哋會認識 C++ 嘅基本型別。多謝收睇，下次見！",
          EndCard("整一個 int 變數 temperature，用大括號初始化做 36.6，睇吓 g++ 點講，再改啱佢個型別。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

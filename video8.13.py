#!/usr/bin/env python3
"""Video 100 (syllabus 8.13): 常用演算法

find, accumulate and min_element on {72, 45, 91, 58, 45} really print "91 at 2" and "311 45";
transform adds 5 to every mark (77 50 96 63 50). std::remove alone does not shrink the vector:
g++ really warns the nodiscard result was ignored and the run prints 77 96 63 63 50. The
erase-remove idiom prints 77 96 63. Run `python3 video8.13.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 100
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "08-13"
FINAL = (CODE / "algo.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
ERASE = "    m.erase(std::remove(m.begin(), m.end(), 50), m.end());\n"
REMOVE = "    std::remove(m.begin(), m.end(), 50);\n"
TRANS = "    std::transform" + FINAL.split("    std::transform")[1].split("    m.erase")[0]
LOOP = "    for (int x : m)" + FINAL.split("    for (int x : m)")[1].rsplit("}\n", 1)[0]
V2 = FINAL.replace(ERASE, "")
V1 = V2.replace(TRANS, "").replace(LOOP, "")
BAD = FINAL.replace(ERASE, REMOVE)
CC = "g++ -std=c++20 -Wall -Wextra algo.cpp -o algo"

(c1, r1, clr, c2, r2, clr2, c3, r3, clr3, c4, r4, cch, rch) = cpp.session({"algo.cpp": V1}, [
    CC, "./algo", "clear", Write("algo.cpp", V2), CC, "./algo", "clear", Write("algo.cpp", BAD), CC, "./algo",
    "clear", Write("algo.cpp", FINAL), CC, "./algo",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
HEAD = "91 at 2\n311 45\n"
assert r1.output == HEAD and r2.output == HEAD + "77 50 96 63 50 \n" and r3.output == HEAD + "77 96 63 63 50 \n", r3.output
assert r4.output == HEAD + "77 96 63 \n" and "ignoring return value" in cpp.visible(c3.output) and "nodiscard" in cpp.visible(c3.output)
assert c1.code == c2.code == c3.code == c4.code == cch.code == 0 and rch.output == "2 3\n"

SAY = {"std::find": "S T D find", "std::accumulate": "S T D accumulate", "accumulate": "accumulate", "std::min_element": "S T D min element",
       "min_element": "min element", "std::transform": "S T D transform", "transform": "transform", "std::remove": "S T D remove",
       "remove": "remove", "erase": "erase", "std::erase": "S T D erase", "std::count": "S T D count", "count_if": "count if",
       "nodiscard": "no discard", "<numeric>": "numeric", "it - m.begin()": "it 減 begin", "*lo": "星 lo", "erase-remove": "erase remove"}

s = Stage({"algo.cpp": V1}, title="常用演算法", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！搵嘢、加總、搵最細、逐個改、刪走某啲值，呢啲日常工作，標準庫全部有現成嘅演算法。今集逐個試，仲有一個好出名嘅陷阱。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "find · accumulate · transform · remove")),
    Scene("goal",
          "今集會講：[[b1]]find 同 min_element；[[b2]]accumulate；[[b3]]transform；[[b4]]remove 嘅陷阱，同 erase remove。",
          BulletCard("今集學識", [("find、min_element", "b1"), ("accumulate（<numeric>）", "b2"), ("transform", "b3"), ("remove 陷阱 → erase-remove", "b4")])),
    Scene("find",
          "[[find]]find 搵九十一，回傳一個 iterator；減 begin 就係佢嘅位置。[[acc]]accumulate 由零開始加晒，喺 numeric 入面。[[min]]min_element 回傳指住最細嗰個嘅 iterator，"
          "要加星號攞值。[[cc]]編譯運行，[[o]]位置二，因為由零開始數；總和三百一十一，最細四十五。三句，一個迴圈都冇寫。",
          s.scene(Open("algo.cpp", at="find"), Mark((8, 9), at="find"), Mark(10, at="acc"), Mark(11, at="min"), Mark(None, at="cc"), Run(c1, at="cc"), Run(r1))),
    Scene("transform",
          "[[type]]transform 將每個元素經過一個 lambda，結果寫去第三個參數，呢度寫返落 m 自己：每個分數加五。[[cc]]運行，[[o]]七十七、五十、九十六、六十三、五十。",
          s.scene(Run(clr, at="type"), Type("algo.cpp", TRANS + LOOP, before="}", last=True, at="type", rate=60), Expect("algo.cpp", V2),
                  Mark((13, 14), at="type"), Mark(None, at="cc"), Run(c2, at="cc", recall=True), Run(r2))),
    Scene("remove",
          "而家想刪走所有五十。[[type]]直覺會寫 std::remove。[[cc]]編譯：[[warn]]有警告，話我哋無視咗佢嘅回傳值。運行：[[o]]七十七、九十六、六十三、六十三、五十？仲係五個！",
          s.scene(Run(clr2, at="type"), Type("algo.cpp", REMOVE, before="    for (int x : m)", at="type", rate=40), Expect("algo.cpp", BAD),
                  Run(c3, at="cc", recall=True), Scroll(at="warn"), Run(r3, at="o"))),
    Scene("why",
          "[[algo]]因為演算法只識 iterator，冇權改 vector 嘅大小。[[move]]remove 只係將要保留嘅搬去前面，[[ret]]再回傳新嘅結尾；後面嘅位置仲喺度，入面係剩低嘅舊值。"
          "[[erase]]所以要用 erase，由新結尾刪到 end。",
          BoxesCard("std::remove(…, 50) 做咗乜", [
              BoxRow([Box("", "77", "", at="move", color=GREEN, w=130), Box("", "96", "", at="move", color=GREEN, w=130),
                      Box("", "63", "", at="move", color=GREEN, w=130), Box("", "63", "回傳 →", at="ret", color=RED, w=130, key="r"),
                      Box("", "50", "", at="ret", color=RED, w=130)], gap=10, label="保留 | 剩低"),
          ], notes=[("演算法改唔到 size", "algo"), ("m.erase(新結尾, m.end())", "erase")], top=CONTENT_TOP + 40, row_h=250, box_h=110, size=44)),
    Scene("idiom",
          "[[type]]呢個組合叫 erase remove：remove 回傳新結尾，erase 由嗰度刪到最尾。[[cc]]運行，[[o]]七十七、九十六、六十三，真係冇咗。[[cpp20]]C++20 仲有更簡單嘅 std::erase。",
          s.scene(Run(clr3, at="type"), Replace("algo.cpp", REMOVE, ERASE, at="type", rate=40), Expect("algo.cpp", FINAL), Mark(15, at="type"),
                  Mark(None, at="cc"), Run(c4, at="cc", recall=True), Run(r4), Note("C++20：std::erase(m, 50);", at="cpp20", where="editor"))),
    Scene("table",
          "[[f]]find 搵一個值；[[c]]count、count_if 數；[[a]]accumulate 加總；[[t]]transform 逐個轉換；[[m]]min、max element 搵最細最大；[[r]]刪嘢就用 erase remove。",
          TableCard("常用演算法", ["演算法", "做乜", "回傳"], [
              (["find", "搵一個值", "iterator（冇就 end）"], "f"),
              (["count / count_if", "數幾多個", "數目"], "c"),
              (["accumulate", "加總", "總和"], "a"),
              (["transform", "逐個轉換", "結尾 iterator"], "t"),
              (["min_element", "搵最細", "iterator"], "m"),
              (["erase(remove(…))", "真正刪走", "—"], "r", GREEN),
          ], widths=[1.3, 1, 1.3], code_cols=(0,), size=34)),
    Scene("recap",
          "總結：[[r1]]find、min_element 回傳 iterator，要加星號攞值；[[r2]]accumulate 要 include numeric；[[r3]]transform 逐個轉換；[[r4]]remove 唔會刪，要配 erase。",
          BulletCard("今集重點", [("find、min_element → iterator", "r1"), ("accumulate：<numeric>", "r2"), ("transform", "r3"), ("erase(remove(…), end())", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]用 std::count 數四十五有幾多個，再用 C++20 嘅 std::erase 刪晒佢哋，印出數目同剩低幾多個。[[next]]下一集：二分搜尋。多謝收睇，下次見！",
          EndCard("用 std::count 數 {72, 45, 91, 58, 45} 入面有幾多個 45，再 std::erase(m, 45)，印出 2 3。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

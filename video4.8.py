#!/usr/bin/env python3
"""Video 49 (syllabus 4.8): 字元同中文字

A password checker with <cctype> (std::isdigit, cast to unsigned char); "香港" really has
size() 6 and the bytes e9 a6 99 e6 b8 af (UTF-8); the six-character password 我的密碼12 really
passes the size() >= 8 rule; counting characters (bytes that do not start with 10) fixes it.
Run `python3 video4.8.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import CONTENT_TOP, ROOT

N = 49
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "04-08"
FINAL = (CODE / "pass.cpp").read_text()
BYTES = (CODE / "bytes.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
COUNT = FINAL.split("#include <string>\n\n")[1].split("int main")[0]
V1 = FINAL.replace(COUNT, "").replace("countChars(pw) >= 8", "pw.size() >= 8")
CP = "g++ -std=c++20 -Wall -Wextra pass.cpp -o pass"
CB = "g++ -std=c++20 -Wall -Wextra bytes.cpp -o bytes"
CN = "我的密碼12"

(c1, r1a, r1b, clr, c2, r2, r1c, clr2, c3, r3a, r3b, cch, rch) = cpp.session({"pass.cpp": V1, "bytes.cpp": BYTES}, [
    CP, Input("./pass", ["hello"]), Input("./pass", ["hello2025"]),
    "clear", CB, "./bytes", Input("./pass", [CN]),
    Write("pass.cpp", FINAL), "clear", CP, Input("./pass", [CN]), Input("./pass", ["hello2025"]),
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", Input("./ch", ["hong kong 2026"]),
], refresh=opts.fresh_runs, cols=48)
assert r1a.output.endswith("Weak\n") and r1b.output.endswith("Strong\n")
assert r2.output == "香港 6\ne9 a6 99 e6 b8 af \n", r2.output
assert r1c.output.endswith("Strong\n") and r3a.output.endswith("Weak\n") and r3b.output.endswith("Strong\n")
assert c1.code == c2.code == c3.code == cch.code == 0 and rch.output.endswith("HONG KONG 2026\n")
HEX = r2.output.split("\n")[1].split()

SAY = {"cctype": "C C type", "std::isdigit": "S T D is digit", "isdigit": "is digit", "isupper": "is upper", "toupper": "to upper",
       "UTF-8": "U T F 八", "size()": "size", "countChars": "count chars", "unsigned char": "unsigned char", "byte": "byte",
       "我的密碼12": "我的密碼一二", "std::hex": "S T D hex"}

s = Stage({"pass.cpp": V1, "bytes.cpp": BYTES}, title="字元同中文字", code_px=22)

scenes = [
    Scene("intro",
          "歡迎返嚟！之前講過，中文字串要等到今集先講。今集學點樣逐個字元檢查字串，同埋中文字喺電腦入面，其實係點樣儲存。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "<cctype> · UTF-8 · byte vs 字")),
    Scene("goal",
          "今集會講：[[b1]]cctype 入面檢查字元嘅函數；[[b2]]寫一個密碼檢查器；[[b3]]UTF-8：點解一個中文字係三個 byte。",
          BulletCard("今集學識", [("<cctype>：isdigit、isupper、toupper", "b1"), ("密碼檢查器", "b2"), ("UTF-8：byte 同字", "b3")])),
    Scene("cctype",
          "cctype 有好多檢查字元嘅函數：[[d]]isdigit 問係咪數字；[[a]]isalpha 問係咪英文字母；[[u]]isupper 問係咪大楷；"
          "[[t]]toupper 就將細楷變大楷。",
          TableCard("<cctype>", ["函數", "例子", "結果"], [
              (["std::isdigit", "'7'", "true"], "d"), (["std::isalpha", "'a'", "true"], "a"),
              (["std::isupper", "'a'", "false"], "u"), (["std::toupper", "'a'", "'A'"], "t"),
          ], widths=[1.3, 0.8, 0.8], code_cols=(0, 1, 2), size=42)),
    Scene("checker",
          "[[open]]密碼規則：最少八個字，而且要有數字。[[loop]]逐個字元檢查，係數字就加一。[[cast]]傳入 isdigit 之前，要轉做 unsigned char，"
          "等陣就知點解。[[rule]]最後睇長度同數字。",
          s.scene(Open("pass.cpp", at="open"), Mark((10, 14), at="loop"), Mark(11, at="cast"), Mark(15, at="rule"))),
    Scene("run1",
          "[[cc]]編譯運行。[[t1]]輸入 hello：[[o1]]得五個字，又冇數字，所以係 Weak。[[t2]]再試 hello 二零二五：[[o2]]夠長，又有數字，Strong。兩個條件都要過，先算 Strong。",
          s.scene(Mark(None), Run(c1, at="cc"), Run(r1a, keys=("t1",)), Run(r1b, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("bytes",
          "跟住睇中文。[[open]]呢個程式印出香港兩個字，同埋 size；[[loop]]再用十六進制，印出每一個 byte。[[cc]]編譯運行：[[o]]size 係六，唔係二！下面六個十六進制嘅數，就係嗰六個 byte。",
          s.scene(Run(clr, at="open"), Open("bytes.cpp", at="open"), Mark((5, 6), at="open"), Mark((7, 10), at="loop"), Mark(None, at="cc"),
                  Run(c2, at="cc"), Run(r2), Note("兩個字，size 係 6？", at="o", where="editor"))),
    Scene("utf8",
          "因為電腦用 UTF-8 儲存文字：[[en]]英文字母一個 byte；[[zh]]大部分中文字要三個 byte。香係三個 byte，港又係三個，加埋就係六。"
          "[[size]]所以 size 數嘅係 byte，唔係字。[[neg]]呢啲 byte 放入 char，會變成負數，所以傳入 isdigit 之前，要先轉做 unsigned char。",
          BoxesCard("\"香港\" 喺記憶體入面", [BoxRow(
              [Box("香" if i == 1 else "", HEX[i], f"byte {i}", at="zh", color=AMBER, w=150) for i in range(3)]
              + [Box("港" if i == 4 else "", HEX[i], f"byte {i}", at=("zh", 0.6), color=PURPLE, w=150) for i in range(3, 6)],
              gap=0)], top=CONTENT_TOP + 40, box_h=110, size=52,
              notes=[("英文字母：1 byte；中文字：通常 3 byte", "en"), ("size() 數 byte：\"香港\" 係 6", "size")])),
    Scene("bug",
          "咁密碼檢查器就有問題。[[t]]輸入我的密碼一二：[[o]]只有六個字，但係佢話 Strong！因為四個中文字佔咗十二個 byte，size 係十四。",
          s.scene(Note(None), Run(r1c, at="t", recall=True, keys=(("t", 0.9),)), Note("6 個字都 Strong？\nsize() 係 14 byte", at="o", where="editor"))),
    Scene("fix",
          "UTF-8 有條規則：[[rule]]一個字嘅第二、第三個 byte，開頭兩個 bit 一定係一零。[[fn]]countChars 唔數呢啲 byte，就數到真正有幾多個字。"
          "[[use]]最後，長度嘅檢查改用 countChars，唔再用 size：咁中文同英文都數得啱。",
          s.scene(Note(None), Type("pass.cpp", COUNT, before="int main", at="fn", rate=34), Mark(8, at="fn"),
                  Replace("pass.cpp", "pw.size() >= 8", "countChars(pw) >= 8", at="use"), Expect("pass.cpp", FINAL))),
    Scene("run2",
          "[[cc]]再編譯運行。[[t1]]我的密碼一二：[[o1]]今次係 Weak，只有六個字。[[t2]]hello 二零二五，[[o2]]照樣 Strong。中文英文都處理得啱。",
          s.scene(Mark(None), Run(clr2, at="cc"), Run(c3, recall=True), Run(r3a, recall=True, keys=("t1",)),
                  Run(r3b, at="t2", recall=True, keys=(("t2", 0.9),)))),
    Scene("recap",
          "總結：[[r1]]cctype 有 isdigit、isalpha、isupper、toupper；[[r2]]傳入之前轉做 unsigned char；[[r3]]中文用 UTF-8，通常三個 byte 一個字；"
          "[[r4]]size 同中括號都係數 byte，唔係數字。",
          BulletCard("今集重點", [("<cctype>：isdigit、toupper…", "r1"), ("先轉 unsigned char", "r2"),
                                ("UTF-8：中文字通常 3 byte", "r3"), ("size()、[] 係 byte，唔係字", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]讀入一句英文，用 toupper 將佢變晒做大楷。[[next]]下一集，我哋自己寫搜尋同排序。多謝收睇，下次見！",
          EndCard("讀入一句英文，用 std::toupper 將佢全部變做大楷再印出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

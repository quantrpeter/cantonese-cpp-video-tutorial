#!/usr/bin/env python3
"""Video 9 (syllabus 1.3): 基本型別

int, long long, double, char and bool, each with a sample value; bool prints as 1; the real error
for a char written with double quotes; sizeof for each type, with the real byte counts.
Run `python3 video9.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 9
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "01-03"
TYPES = (CODE / "types.cpp").read_text()
SIZES = (CODE / "sizes.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
SKEL = "#include <iostream>\n\nint main() {\n}\n"
NUMS = "    int students{32};\n    long long people{8000000000};\n    double height{1.68};\n"
CB = "    char grade{'A'};\n    bool passed{true};\n"
PRINT = ("\n    std::cout << students << '\\n';\n    std::cout << people << '\\n';\n"
         "    std::cout << height << ' ' << grade << '\\n';\n    std::cout << passed << '\\n';\n")
assert SKEL.replace("}\n", NUMS + CB + PRINT + "}\n") == TYPES
WRONG = TYPES.replace("{'A'}", '{"A"}')
CT = "g++ -std=c++20 -Wall -Wextra types.cpp -o types"
CS = "g++ -std=c++20 -Wall -Wextra sizes.cpp -o sizes"

(ct, rt, cw, clr, cs, rs, cch, rch) = cpp.session({"types.cpp": TYPES, "sizes.cpp": SIZES}, [
    CT, "./types",
    Write("types.cpp", WRONG), CT,
    Write("types.cpp", TYPES), "clear", CS, "./sizes",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert rt.output.split("\n")[:4] == ["32", "8000000000", "1.68 A", "1"], rt.output
assert "invalid conversion from 'const char*' to 'char'" in cpp.visible(cw.output), cw.output
size = dict(zip(["char", "bool", "int", "double", "long long"], map(int, rs.output.split())))
assert size == {"char": 1, "bool": 1, "int": 4, "double": 8, "long long": 8}, size
assert ct.code == cs.code == cch.code == 0 and rch.output.strip() == "P 1"

SAY = {"sizeof": "size of", "long long": "long long", "'A'": "A", "byte": "byte"}

s = Stage({"types.cpp": SKEL, "sizes.cpp": SIZES}, title="五個基本型別")

scenes = [
    Scene("intro",
          "歡迎返嚟！之前我哋見過 int 同 double。今集將 C++ 最常用嘅五個基本型別，一次過認識晒。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "int · long long · double · char · bool")),
    Scene("goal",
          "今集會講：[[b1]]五個基本型別，分別裝乜嘢；[[b2]]char 同 bool 點樣寫；[[b3]]用 sizeof 睇吓每個型別佔幾多記憶體。",
          BulletCard("今集學識", [("五個基本型別 type", "b1"), ("char 同 bool 嘅寫法", "b2"), ("sizeof：佔幾多 byte", "b3")])),
    Scene("table",
          "[[int]]int 裝整數，例如一班有三十二個學生；[[ll]]long long 都係整數，但係裝得落大好多嘅數，例如全世界大約八十億人；"
          "[[dbl]]double 裝有小數嘅數，例如身高一點六八米；[[chr]]char 裝一個字元，例如成績 A；"
          "[[bool]]bool 只有兩個值：true 同 false，即係真同假。",
          TableCard("五個基本型別", ["型別", "裝乜", "例子"], [
              (["int", "整數", "32"], "int"),
              (["long long", "好大嘅整數", "8000000000"], "ll"),
              (["double", "有小數嘅數", "1.68"], "dbl"),
              (["char", "一個字元", "'A'"], "chr"),
              (["bool", "真或者假", "true / false"], "bool"),
          ], widths=[1, 1, 1.1], code_cols=(0, 2), size=44)),
    Scene("nums",
          "我哋逐個寫。[[t1]]學生人數用 int；[[t2]]世界人口八十億，int 裝唔落，所以用 long long；[[t3]]身高有小數，用 double。",
          s.scene(Open("types.cpp", mode="instant"),
                  Type("types.cpp", NUMS.splitlines(True)[0], before="}", last=True, at="t1"),
                  Type("types.cpp", NUMS.splitlines(True)[1], before="}", last=True, at="t2"),
                  Type("types.cpp", NUMS.splitlines(True)[2], before="}", last=True, at="t3"))),
    Scene("charbool",
          "[[t4]]char 嘅值要用單引號包住，而且只可以有一個字元；[[t5]]bool 就寫 true 或者 false，唔使引號。",
          s.scene(Type("types.cpp", CB.splitlines(True)[0], before="}", last=True, at="t4"),
                  Note("char：單引號，一個字元", at=("t4", 1.6), where="editor"),
                  Type("types.cpp", CB.splitlines(True)[1], before="}", last=True, at="t5"))),
    Scene("print",
          "[[type]]最後用四句 cout，將佢哋全部印出嚟。第三句中間，用單引號包住一個空格，將兩個值隔開。[[cc]]編譯運行。[[out]]留意最後一行：bool 印出嚟唔係 true，而係一。"
          "因為印 bool 嘅時候，true 係一，false 係零。",
          s.scene(Note(None), Type("types.cpp", PRINT, before="}", last=True, at="type", rate=22), Expect("types.cpp", TYPES),
                  Run(ct, at="cc"), Run(rt), Mark(13, at="out"),
                  Note("bool 印出嚟：\ntrue 係 1，false 係 0", at="out", where="editor"))),
    Scene("mistake",
          "新手好常見嘅錯誤：[[typo]]將 char 嘅單引號寫咗做雙引號。[[cc]]編譯，[[err]]出錯：雙引號入面係字串，唔係一個字元，"
          "放唔入 char。[[fix]]改返單引號就得。",
          s.scene(Note(None), Mark(None), Replace("types.cpp", "{'A'}", '{"A"}', at="typo"), Expect("types.cpp", WRONG),
                  Run(cw, at="cc", recall=True), Note("'A'：一個字元 char\n\"A\"：字串，唔係 char", at="err", where="editor"),
                  Replace("types.cpp", '{"A"}', "{'A'}", at="fix"), Expect("types.cpp", TYPES))),
    Scene("sizeof",
          "每個型別佔嘅記憶體都唔同。[[open]]sizeof 可以話你知，一個型別佔幾多個 byte。[[cc]]編譯運行：[[out]]char 同 bool 佔一個 byte，"
          "int 佔四個，double 同 long long 佔八個。",
          s.scene(Note(None), Run(clr), Open("sizes.cpp", at="open"), Run(cs, at="cc"), Run(rs))),
    Scene("bytes",
          "[[bars]]一個 byte 有八個 bit。int 有四個 byte，最大大約係二十一億；[[ll]]long long 有八個 byte，"
          "大約可以去到九後面跟十八個零。[[note]]所以好似人口咁大嘅數，就要用 long long。",
          BarCard("每個型別佔幾多 byte？", [Bar(k, v, f"{v} byte", c) for (k, v), c in
                                           zip(size.items(), [TEAL, PURPLE, BLUE, AMBER, RED])],
                  at="bars", top=270, step=118, stagger=0.4,
                  note=("int 最大 2147483647　long long 最大約 9.2 × 10¹⁸", "ll"))),
    Scene("recap",
          "總結：[[r1]]int 同 long long 裝整數，大數用 long long；[[r2]]double 裝小數；[[r3]]char 用單引號裝一個字元；"
          "[[r4]]bool 係 true 或者 false；[[r5]]sizeof 話你知佔幾多 byte。",
          BulletCard("今集重點", [("整數：int；好大嘅整數：long long", "r1"), ("小數：double", "r2"),
                                ("一個字元：char，用單引號 'A'", "r3"), ("真假：bool，true / false", "r4"),
                                ("sizeof：佔幾多 byte", "r5")], gap=30)),
    Scene("outro",
          "小挑戰：[[ch]]加一個 char 變數 initial，裝你英文名嘅第一個字母；再加一個 bool 變數，記住你鍾唔鍾意 C++，印晒出嚟。"
          "[[next]]下一集，我哋會學點樣用 cin 讀取使用者輸入。多謝收睇，下次見！",
          EndCard("加一個 char 變數 initial，裝你英文名嘅第一個字母；再加一個 bool 變數 likesCpp，印晒出嚟。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

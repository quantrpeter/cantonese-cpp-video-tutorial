#!/usr/bin/env python3
"""Video 40 (syllabus 3.11): namespace

Two print() functions with the same parameters are a real "redefinition" error; namespaces
english and cantonese keep them apart (english::print()); std is the standard library's
namespace; with `using namespace std;` a global named count is a real "ambiguous" error.
Run `python3 video3.11.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 40
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

CODE = ROOT / "code" / "03-11"
NS = (CODE / "ns.cpp").read_text()
CLASH = (CODE / "clash.cpp").read_text()
CHALLENGE = (CODE / "challenge.cpp").read_text()
BODY_NS = NS.split("#include <iostream>\n\n")[1].split("int main() {")[0]
BODY_V1 = ("void print() {\n    std::cout << \"Hello!\\n\";\n}\n\n"
           "void print() {\n    std::cout << \"Nei hou!\\n\";\n}\n\n")
CALLS_NS = "    english::print();\n    cantonese::print();\n"
V1 = NS.replace(BODY_NS, BODY_V1).replace(CALLS_NS, "    print();\n")
USING = "using namespace std;\n"
CBAD = CLASH.replace("#include <algorithm>\n", "#include <algorithm>\n" + USING).replace("std::cout", "cout")
CN = "g++ -std=c++20 -Wall -Wextra ns.cpp -o ns"
CC = "g++ -std=c++20 -Wall -Wextra clash.cpp -o clash"

(c1, c2, r2, clr, c3, c4, r4, cch, rch) = cpp.session({"ns.cpp": V1, "clash.cpp": CBAD}, [
    CN, Write("ns.cpp", NS), CN, "./ns", "clear", CC, Write("clash.cpp", CLASH), CC, "./clash",
    Write("challenge.cpp", CHALLENGE), "g++ -std=c++20 -Wall -Wextra challenge.cpp -o ch", "./ch",
], refresh=opts.fresh_runs, cols=48)
assert "redefinition of 'void print()'" in cpp.visible(c1.output), c1.output
assert r2.output == "Hello!\nNei hou!\n" and c2.code == 0
assert "reference to 'count' is ambiguous" in cpp.visible(c3.output), c3.output[:400]
assert c4.code == 0 and r4.output.strip() == "1" and cch.code == 0 and rch.output.strip() == "24"

SAY = {"namespace": "namespace", "english::print()": "english print", "cantonese::print()": "cantonese print",
       "::": "兩個冒號", "using namespace std": "using namespace S T D", "std::": "S T D 兩個冒號", "count": "count",
       "using std::cout": "using S T D see out"}

s = Stage({"ns.cpp": V1, "clash.cpp": CBAD}, title="namespace", code_px=24)

scenes = [
    Scene("intro",
          "歡迎返嚟！如果兩個人，各自寫咗一個同名嘅函數，點算？今集講 namespace，即係命名空間。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "namespace · :: · using")),
    Scene("goal",
          "今集會講：[[b1]]名撞咗會點；[[b2]]用 namespace 分開佢哋；[[b3]]std 其實都係一個 namespace；[[b4]]點解唔好亂用 using namespace std。",
          BulletCard("今集學識", [("名撞咗會點", "b1"), ("namespace 分開", "b2"), ("std 都係 namespace", "b3"),
                                ("小心 using namespace std", "b4")])),
    Scene("clash",
          "[[open]]一個 print 印英文，另一個 print 印廣東話，參數一模一樣。[[cc]]編譯，[[err]]出錯：print 重複定義。"
          "[[why]]參數一樣，多載都幫唔到手。",
          s.scene(Open("ns.cpp", at="open"), Mark((3, 9), at=("open", 0.8)), Mark(None, at="cc"), Run(c1, at="cc"))),
    Scene("wrap",
          "[[ns]]將佢哋分別放入兩個 namespace：english 同 cantonese。[[call]]用嘅時候，就寫 namespace 名，加兩個冒號，再加函數名，好似英文嘅 print，就寫 english 兩個冒號 print。",
          s.scene(Replace("ns.cpp", BODY_V1, BODY_NS, at="ns", rate=34),
                  Replace("ns.cpp", "    print();\n", CALLS_NS, at="call"), Expect("ns.cpp", NS))),
    Scene("run1",
          "[[cc]]編譯運行，[[o]]Hello，同埋 Nei hou。兩個 print 各自喺自己嘅 namespace 入面，唔會再撞。",
          s.scene(Run(c2, at="cc", recall=True), Run(r2))),
    Scene("anatomy",
          "[[ns]]english 係命名空間嘅名；[[col]]兩個冒號讀做『入面嘅』；[[fn]]print 就係函數。[[std]]所以 std::cout，"
          "意思係標準庫 std 入面嘅 cout：標準庫嘅嘢，全部都喺 std 呢個 namespace 入面。",
          AnatomyCard("english::print();", [
              Part("english", "命名空間", PURPLE, "ns"),
              Part("::", "入面嘅", AMBER, "col"),
              Part("print", "函數", BLUE, "fn"),
              Part("();", "", MUTED, "fn"),
          ], size=90, note=("std::cout ＝ std 入面嘅 cout", "std"))),
    Scene("using",
          "網上好多教學，會寫 using namespace std，咁就唔使寫 std::。[[open]]但係睇吓呢個程式：我哋有個變數叫 count，"
          "記得 3.8 講過，全域變數唔好亂用，呢度只係示範。[[cc]]編譯，[[err]]出錯：count 有歧義。"
          "因為標準庫入面都有個 count，using namespace std 將佢哋全部攞咗出嚟，撞埋一齊。",
          s.scene(Run(clr, at="open"), Open("clash.cpp", at="open"), Mark(3, at="open"), Mark(5, at=("open", 1.5)), Mark(None, at="cc"), Run(c3, at="cc"),
                  Note("using namespace std：\nstd::count 同我哋嘅 count 撞名", at="err", where="editor"))),
    Scene("fix",
          "[[del]]刪走 using namespace std，[[std]]cout 前面寫返 std::。[[cc]]再編譯運行，[[o]]印出一，冇問題：count 就係我哋自己嗰個。",
          s.scene(Note(None), Replace("clash.cpp", USING, "", at="del"), Replace("clash.cpp", "    cout", "    std::cout", at="std"),
                  Expect("clash.cpp", CLASH), Run(c4, at="cc", recall=True), Run(r4))),
    Scene("rules",
          "所以：[[r1]]標頭檔入面，絕對唔好寫 using namespace std，因為所有 include 佢嘅檔案都會受影響；"
          "[[r2]]cpp 檔入面，寫 std:: 最清楚；[[r3]]真係想短啲，可以用 using std::cout，淨係攞一樣出嚟。",
          BulletCard("點樣用 using？", [("標頭檔：絕對唔好 using namespace std", "r1"), (".cpp：寫 std:: 最清楚", "r2"),
                                      ("想短啲：using std::cout;", "r3")])),
    Scene("recap",
          "總結：[[r1]]namespace 將名分開，避免撞名；[[r2]]用兩個冒號攞 namespace 入面嘅嘢；[[r3]]標準庫喺 std 入面；"
          "[[r4]]小心 using namespace std。",
          BulletCard("今集重點", [("namespace：避免撞名", "r1"), ("名::嘢：入面嘅", "r2"), ("標準庫：std", "r3"),
                                ("小心 using namespace std", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]寫一個 namespace shapes，入面有 area 函數，喺 main 用 shapes::area 呼叫佢。"
          "[[next]]下一集係第三章嘅小項目：計數機。多謝收睇，下次見！",
          EndCard("寫一個 namespace shapes，入面有 area(w, h)；喺 main 用 shapes::area 呼叫佢。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts, say=SAY)

#!/usr/bin/env python3
"""Video 3 (syllabus 0.3): Hello, World!

hello.cpp typed line by line with each line explained, compiled and run for real, a second line
added, and a missing semicolon shown with the real g++ error. Run `python3 video3.py --help`.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 3
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

# The finished program (code/00-03/hello.cpp) and the versions on the way to it.
FULL = (ROOT / "code" / "00-03" / "hello.cpp").read_text()
LINE2 = '    std::cout << "I am learning C++.\\n";\n'
ONE = FULL.replace(LINE2, "")                       # Hello, World! only
NOSEMI = FULL.replace('C++.\\n";', 'C++.\\n"')       # the mistake
CC = "g++ hello.cpp -o hello"

cc1, run1, cc2, run2, clear, cc3, cc4, run4 = cpp.session({"hello.cpp": ONE}, [
    CC, "./hello",
    Write("hello.cpp", FULL), CC, "./hello",
    Write("hello.cpp", NOSEMI), "clear", CC,
    Write("hello.cpp", FULL), CC, "./hello",
], refresh=opts.fresh_runs, cols=48)
assert cc1.code == cc2.code == cc4.code == 0 and cc3.code != 0
assert "expected ';' before 'return'" in cpp.visible(cc3.output), cc3.output

demo = Stage({"hello.cpp": ONE}, title="今集成品")
s = Stage({"hello.cpp": ONE}, title="逐行寫 Hello, World!")

scenes = [
    Scene("intro",
          "歡迎返嚟 C++ 全攻略！今集我哋終於會寫第一個 C++ 程式，就係每個程式員嘅第一課：Hello, World！",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "你嘅第一個 C++ 程式")),
    Scene("goal",
          "今集會：[[b1]]寫出第一個 C++ 程式；[[b2]]逐行明白每一句做乜；[[b3]]學識編譯同運行；[[b4]]仲會改吓個程式，印多幾句。",
          BulletCard("今集學識", [("寫出第一個 C++ 程式", "b1"), ("逐行明白每一句做乜", "b2"),
                                ("編譯同運行", "b3"), ("改程式、印多幾句", "b4")])),
    Scene("demo",
          "先睇吓今集嘅成品：[[code]]短短六行程式，[[run]]編譯、運行，螢幕就會印出 Hello, World!",
          demo.scene(Open("hello.cpp", at="code", mode="lines", rate=10), Run(cc1, at="run"), Run(run1))),
    Scene("line1",
          "好，由一張白紙開始。[[type]]第一行：#include <iostream>。[[mark]]include 即係「借用」，iostream 係一個工具箱，"
          "入面有負責輸入同輸出嘅工具。我哋要喺螢幕印字，所以要借佢。",
          s.scene(Open("hello.cpp", mode="empty"), Type("hello.cpp", "#include <iostream>\n", at="type"),
                  Mark(1, at="mark"), Note("#include：借用工具箱\n<iostream>：輸入同輸出嘅工具", at="mark"))),
    Scene("main",
          "[[type]]跟住空一行，打 int main，一對括號，再加一對大括號。[[mark]]main 係程式嘅起點，電腦一開始，就係由 main 入面做起。"
          "[[box]]大括號就好似一個盒，main 要做嘅嘢，全部放喺入面。",
          s.scene(Mark(None), Note(None), Type("hello.cpp", "\nint main() {\n}", at="type"),
                  Mark((3, 4), at="mark"), Note("main：程式由呢度開始", at="mark"),
                  Note("main：程式由呢度開始\n{ }：main 要做嘅嘢，放入面", at="box"))),
    Scene("cout",
          "[[type]]喺大括號入面，打呢一行。[[mark]]std::cout 係輸出，即係印去螢幕。兩個細過號好似箭咀咁，將後面嘅字送去 cout。",
          s.scene(Mark(None), Note(None),
                  Type("hello.cpp", '    std::cout << "Hello, World!\\n";\n', after="int main() {\n", at="type"),
                  Mark(4, at="mark"), Note("std::cout：輸出到螢幕\n<<：將字送過去", at="mark"))),
    Scene("anatomy",
          "拆開嚟睇：[[cout]]std::cout 負責輸出；[[arrow]]兩個細過號，將嘢送過去；[[str]]雙引號入面嘅係字串，即係要印嘅字；"
          "[[nl]]反斜線 n 代表換行；[[semi]]最後嘅分號，就好似中文嘅句號，代表呢句完結。C++ 每句指令，都要用分號收尾。",
          AnatomyCard("拆解第四行", [
              Part("std::cout", "輸出到螢幕", BLUE, "cout"),
              Part(" << ", "送去", TEAL, "arrow"),
              Part('"Hello, World!', "要印嘅字（字串）", GREEN, "str"),
              Part("\\n", "換行", AMBER, "nl"),
              Part('"', "", GREEN, "str"),
              Part(";", "一句完結", RED, "semi"),
          ])),
    Scene("ret",
          "[[type]]最後一行，return 0。[[mark]]意思係話俾電腦知：程式順利完成。其實 main 唔寫 return 0 都得，但係寫埋會清楚啲。",
          s.scene(Mark(None), Note(None),
                  Type("hello.cpp", "    return 0;\n", after='World!\\n";\n', at="type"),
                  Mark(5, at="mark"), Note("return 0：話俾電腦知\n程式順利完成", at="mark"),
                  Expect("hello.cpp", ONE))),
    Scene("compile",
          "程式寫好，記得儲存。[[cc]]跟住喺 Terminal 打：g++ hello.cpp -o hello。意思係將 hello.cpp 翻譯，整一個叫 hello 嘅程式。"
          "[[ok]]冇任何訊息出現，就代表成功。",
          s.scene(Mark(None), Note(None), Run(cc1, at="cc"), Note("冇訊息 ＝ 編譯成功", at="ok"))),
    Scene("run",
          "[[run]]然後打 ./hello 運行。[[out]]成功喇！螢幕印出 Hello, World!。[[win]]用 Windows 嘅話，個程式會叫 hello.exe，"
          "一樣打 ./hello 就行到。恭喜你，呢個就係你嘅第一個 C++ 程式！",
          s.scene(Note(None), Run(run1, at="run"), Note("你嘅第一個 C++ 程式！", at="out"),
                  Note("Windows：程式叫 hello.exe\n一樣打 ./hello 運行", at="win"))),
    Scene("more",
          "想印多句？[[type]]加多一行 cout 就得。[[cc]]改完程式，要重新編譯，[[run]]再運行。"
          "[[out]]兩句都印咗出嚟，而且因為有反斜線 n，佢哋分開兩行。",
          s.scene(Note(None), Type("hello.cpp", LINE2, after='World!\\n";\n', at="type"), Expect("hello.cpp", FULL),
                  Run(cc2, at="cc"), Run(run2, at="run"))),
    Scene("mistake",
          "如果唔小心漏咗分號，會點？[[del]]我哋刪咗第五行尾嘅分號，[[cc]]再編譯。[[err]]g++ 即刻話有 error："
          "喺 return 前面，應該要有個分號。編譯失敗，就唔會整出新嘅程式。下下集，我哋會詳細講點樣睇錯誤訊息。",
          s.scene(Replace("hello.cpp", 'C++.\\n";', 'C++.\\n"', at="del"), Expect("hello.cpp", NOSEMI),
                  Run(clear, at="cc"), Run(cc3), Note("漏咗分號 → error\n編譯失敗", at="err"))),
    Scene("fix",
          "[[fix]]加返個分號，[[cc]]再編譯，再運行，兩句又印返出嚟喇。記住：C++ 每句指令後面，都要有分號。",
          s.scene(Note(None), Type("hello.cpp", ";", after='C++.\\n"', at="fix"), Expect("hello.cpp", FULL),
                  Run(cc4, at="cc"), Run(run4))),
    Scene("recap",
          "總結一下：[[r1]]#include <iostream> 借用輸入輸出工具；[[r2]]程式由 main 開始；[[r3]]std::cout 加 << 印字，\\n 換行；"
          "[[r4]]每句指令用分號收尾；[[r5]]改完程式，記得重新編譯。",
          BulletCard("今集重點", [("#include <iostream>：借用輸入輸出工具", "r1"), ("程式由 int main() 開始", "r2"),
                                ("std::cout << 印字，\\n 換行", "r3"), ("每句指令用分號 ; 收尾", "r4"),
                                ("改完程式，要重新編譯", "r5")], size=48, gap=36)),
    Scene("outro",
          "小挑戰：[[ch]]改個程式，用三行英文，印出你嘅名、你讀邊間學校，同埋你最鍾意食乜。"
          "[[next]]下一集，我哋會睇清楚，編譯嗰陣背後發生咩事。多謝收睇，下次見！",
          EndCard("改個程式，用三行英文印出：你嘅名、你讀邊間學校、你最鍾意食乜。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)

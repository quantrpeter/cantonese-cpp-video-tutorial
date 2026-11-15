#!/usr/bin/env python3
"""Video 5 (syllabus 0.5): 睇得明編譯錯誤

Four real g++ errors made on camera (missing semicolon, typo, missing #include, a missing quote
that cascades), how to read file:line:col, fixing the first error first, and warnings with
-Wall -Wextra. All messages and colours are g++'s own. Run `python3 video0.5.py --help` for options.
"""

import re

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import NAVY, ROOT

N = 5
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

GOOD = (ROOT / "code" / "00-05" / "hello.cpp").read_text()
E1 = GOOD.replace('World!\\n";', 'World!\\n"')                   # missing semicolon, line 4
E2 = GOOD.replace('cout << "I am', 'cuot << "I am')               # typo, line 5
E3 = GOOD.replace("#include <iostream>\n", "")                    # missing include
E4 = GOOD.replace('C++.\\n";', 'C++.\\n;')                       # missing closing quote
WARN = GOOD.replace("int main() {\n", "int main() {\n    int x = 5;\n")
CC = "g++ -std=c++20 hello.cpp -o hello"
CCW = "g++ -std=c++20 -Wall -Wextra hello.cpp -o hello"

(ok0, run0, clr, e1, ok1, e2, e3, e4, ok4, w_plain, w_wall, run_w) = cpp.session({"hello.cpp": GOOD}, [
    CC, "./hello",
    Write("hello.cpp", E1), "clear", CC,
    Write("hello.cpp", GOOD), CC,
    Write("hello.cpp", E2), CC,
    Write("hello.cpp", E3), CC,
    Write("hello.cpp", E4), CC,
    Write("hello.cpp", GOOD), CC,
    Write("hello.cpp", WARN), CC, CCW, "./hello",
], refresh=opts.fresh_runs, cols=59)

text = {k: cpp.visible(r.output) for k, r in dict(e1=e1, e2=e2, e3=e3, e4=e4, w=w_wall).items()}
assert "expected ';' before 'std'" in text["e1"]
assert "did you mean 'cout'?" in text["e2"]
assert text["e3"].count("error:") == 2 and "#include <iostream>" in text["e3"]
assert len(re.findall(r": (?:error|warning): ", text["e4"])) == 3, text["e4"]
assert "unused variable 'x'" in text["w"] and w_wall.code == 0 and w_plain.output.strip() == ""
assert ok0.code == ok1.code == ok4.code == 0

# The error line taken apart, straight from g++'s real output.
first = next(l for l in text["e1"].splitlines() if ": error: " in l)
f_, line_, col_, msg_ = re.match(r"(\S+?):(\d+):(\d+): error: (.*)", first).groups()

s = Stage({"hello.cpp": GOOD}, title="睇得明編譯錯誤", split=0.45)

scenes = [
    Scene("intro",
          "歡迎返嚟！寫程式，出錯係好正常嘅事，連專業程式員每日都會見到錯誤訊息。今集教你，點樣睇得明 g++ 講乜。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "error · warning · 點樣改")),
    Scene("goal",
          "今集會講：[[b1]]錯誤訊息嘅格式；[[b2]]三種最常見嘅錯誤；[[b3]]點解要先改第一個錯誤；[[b4]]仲有點樣用 -Wall 同 -Wextra 開警告。",
          BulletCard("今集學識", [("錯誤訊息嘅格式", "b1"), ("三種常見錯誤", "b2"),
                                ("點解要先改第一個錯誤", "b3"), ("用 -Wall -Wextra 開警告", "b4")])),
    Scene("setup",
          "我哋用返上一集嘅程式，再加多一句。[[cc]]而家編譯同運行都冇問題。跟住，我哋逐個錯誤試吓。",
          s.scene(Open("hello.cpp", mode="instant"), Run(ok0, at="cc"), Run(run0))),
    Scene("err1",
          "第一個錯誤：[[del]]刪走第四行尾嘅分號，[[cc]]再編譯。撳鍵盤嘅上箭咀，就可以叫返上一句指令，唔使再打過。"
          "[[err]]出咗一大段字，唔使驚，我哋逐行睇。",
          s.scene(Replace("hello.cpp", 'World!\\n";', 'World!\\n"', at="del"), Expect("hello.cpp", E1),
                  Run(clr, at="cc"), Note("撳 ↑：叫返上一句指令", where="editor"), Run(e1, recall=True), Note(None, at="err"))),
    Scene("anatomy",
          "錯誤訊息最重要係呢一行。[[file]]開頭係檔名，[[line]]跟住係第幾行，[[col]]再嚟係嗰行第幾個字。[[kind]]error 即係錯誤，"
          "[[msg]]最後係原因：喺 std 前面，應該要有個分號。",
          AnatomyCard("錯誤訊息點樣睇？", [
              Part(f_, "檔名", BLUE, "file"),
              Part(f":{line_}", "第幾行", PURPLE, "line"),
              Part(f":{col_}", "第幾個字", TEAL, "col"),
              Part(": error:", "錯誤", RED, "kind"),
              Part(f" {msg_}", "原因", NAVY, "msg"),
          ])),
    Scene("err1_read",
          "[[mark]]返去第四行睇吓。[[caret]]訊息入面仲畫咗個箭咀，指住出事嘅位置，下面甚至提示你加個分號。"
          "[[fix]]我哋加返分號，[[cc]]再編譯，[[ok]]冇訊息，即係成功。",
          s.scene(Mark(4, at="mark"), Note("^ 指住出事位置\n下面仲提示你加 ;", at="caret", where="editor"),
                  Type("hello.cpp", ";", after='World!\\n"', at="fix"), Note(None), Mark(None), Expect("hello.cpp", GOOD),
                  Run(clr, at="cc"), Run(ok1, recall=True))),
    Scene("err2",
          "第二種常見錯誤：串錯字。[[typo]]將第五行嘅 cout 打錯做 cuot，[[cc]]編譯。[[err]]佢話 cuot 唔係 std 入面嘅嘢，"
          "[[hint]]仲好貼心咁問你：你係咪想打 cout？[[fix]]改返就得。",
          s.scene(Replace("hello.cpp", 'cout << "I am', 'cuot << "I am', at="typo"), Expect("hello.cpp", E2),
                  Run(clr, at="cc"), Run(e2, recall=True), Note("did you mean 'cout'?\n＝ 你係咪想打 cout？", at="hint", where="editor"),
                  Replace("hello.cpp", "cuot", "cout", at="fix"), Note(None))),
    Scene("err3",
          "第三種：唔記得 include。[[del]]刪走第一行，[[cc]]再編譯。[[err]]今次有兩個 error，都係話 cout 唔係 std 嘅成員。"
          "[[note]]再睇下面嘅 note：佢話 std::cout 喺 iostream 入面，叫你加返 #include <iostream>。[[fix]]照做就搞掂。",
          s.scene(Replace("hello.cpp", "#include <iostream>\n", "", at="del"), Expect("hello.cpp", E3),
                  Run(clr, at="cc"), Run(e3, recall=True), Note("note：叫你加返\n#include <iostream>", at="note", where="editor"),
                  Note(None, at="fix"), Type("hello.cpp", "#include <iostream>\n", before="\nint main"),
                  Expect("hello.cpp", GOOD))),
    Scene("err4",
          "有時一個細錯誤，會引發一大串訊息。[[del]]今次刪走第五行收尾嘅引號，[[cc]]編譯。[[err]]出咗三個訊息，連 return 嗰行都話有錯。"
          "[[rule]]秘訣係：永遠先改第一個，因為後面嗰啲，好多時都係俾第一個錯誤連累出嚟嘅。",
          s.scene(Replace("hello.cpp", 'C++.\\n";', 'C++.\\n;', at="del"), Expect("hello.cpp", E4),
                  Run(clr, at="cc"), Run(e4, recall=True), Note("永遠先改第一個錯誤！\n後面嘅好多時係連累出嚟", at="rule", where="editor"))),
    Scene("err4_fix",
          "[[fix]]淨係加返嗰個引號，[[cc]]再編譯一次。[[ok]]你睇，三個訊息一次過消失晒，因為佢哋其實都係同一個錯誤搞出嚟嘅。",
          s.scene(Note(None), Type("hello.cpp", '"', after="C++.\\n", at="fix"), Expect("hello.cpp", GOOD),
                  Run(clr, at="cc"), Run(ok4, recall=True))),
    Scene("warn1",
          "最後講警告。[[type]]加一行 int x = 5，即係整咗一個叫 x 嘅變數，但係之後完全冇用到。變數第一章會詳細教。"
          "[[cc]]普通咁編譯，[[quiet]]g++ 乜都冇講。",
          s.scene(Type("hello.cpp", "    int x = 5;\n", after="int main() {\n", at="type"), Expect("hello.cpp", WARN),
                  Run(clr, at="cc"), Run(w_plain, recall=True), Note("乜都冇講……\n唔代表冇問題", at="quiet", where="editor"))),
    Scene("warn2",
          "[[cc]]加上 -Wall 同 -Wextra，叫 g++ 開晒啲警告。[[warn]]今次佢用紫色話你知：x 冇用到。[[diff]]warning 同 error 唔同："
          "有 warning 都照樣整到程式，[[run]]照行得。但係 warning 通常代表程式有啲地方唔妥，所以都要睇。",
          s.scene(Note(None), Run(clr), Run(w_wall, at="cc"),
                  Note("紅色 error：編譯失敗\n紫色 warning：照編譯，但要留意", at="diff", where="editor"),
                  Run(run_w, at="run"))),
    Scene("habit",
          "所以由今日開始，我哋都會用呢個完整指令編譯：[[gpp]]g++，[[std]]用 C++20，[[warn]]開晒警告，[[src]]原始碼，[[out]]同埋程式名。",
          AnatomyCard("以後咁樣編譯", [
              Part("g++", "編譯器", BLUE, "gpp"),
              Part(" -std=c++20", "C++20", PURPLE, "std"),
              Part(" -Wall -Wextra", "開晒警告", AMBER, "warn"),
              Part(" hello.cpp", "原始碼", GREEN, "src"),
              Part(" -o hello", "程式檔名", TEAL, "out"),
          ])),
    Scene("recap",
          "總結：[[r1]]錯誤訊息嘅格式係：檔名、行、位置、種類、原因；[[r2]]永遠先改第一個錯誤；[[r3]]睇埋 note 同提示，好多時連答案都有；"
          "[[r4]]用 -Wall 同 -Wextra 開警告，warning 都要理。",
          BulletCard("今集重點", [("格式：檔名:行:位置: error: 原因", "r1"), ("永遠先改第一個錯誤", "r2"),
                                ("睇埋 note 同提示，好多時有答案", "r3"), ("-Wall -Wextra 開警告，warning 都要理", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]故意整三個錯：漏咗一個大括號、將 main 打錯、漏咗一個引號，睇吓 g++ 點講。"
          "[[next]]下一集，我哋會學點樣寫註解，同埋寫出整齊易睇嘅程式。多謝收睇，下次見！",
          EndCard("故意整三個錯：漏咗一個大括號、將 main 打錯、漏咗一個引號，睇吓 g++ 點講。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)

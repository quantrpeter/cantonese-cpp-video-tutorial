#!/usr/bin/env python3
"""Video 4 (syllabus 0.4): 編譯係點運作

Source file vs program file (ls, ls -l with the real sizes), a.out and -o, why an edit needs a new
compile (run without recompiling and see the old output, for real), and -std=c++20.
Run `python3 video4.py --help` for options.
"""

from cpptut import *  # noqa: F403  (switches to the video venv first if needed)
from cpptut.style import ROOT

N = 4
opts = options(N)
ep = course.episode(N)
nxt = course.episode(N + 1)

NEW = (ROOT / "code" / "00-04" / "hello.cpp").read_text()   # after the edit
OLD = NEW.replace("Hong Kong", "World")
CC = "g++ hello.cpp -o hello"
CC20 = "g++ -std=c++20 hello.cpp -o hello"

(ls1, cc_a, ls2, run_a, cc_o, ls3, ll, clear1, run_old, cc_new, run_new, clear2, cc_std, run_std) = cpp.session(
    {"hello.cpp": OLD}, [
        "ls", "g++ hello.cpp", "ls", "./a.out", CC, "ls", "ls -l",
        Write("hello.cpp", NEW), "clear", "./hello", CC, "./hello",
        "clear", CC20, "./hello",
    ], refresh=opts.fresh_runs, cols=48)
assert "Hello, World!" in run_old.output and "Hello, Hong Kong!" in run_new.output, "the stale-program demo failed"

sizes = {ln.split()[-1]: int(ln.split()[4]) for ln in cpp.visible(ll.output).splitlines() if ln.startswith("-")}
src, exe = sizes["hello.cpp"], sizes["hello"]


def roughly(n: int) -> str:
    """七萬幾, 一千幾, 八十六."""
    for unit in (10000, 1000):
        if n >= unit:
            return zh_int(n // unit * unit) + "幾"
    return zh_int(n)


s = Stage({"hello.cpp": OLD}, title="編譯：原始碼 → 程式檔")

scenes = [
    Scene("intro",
          "歡迎返嚟！上一集我哋寫咗 Hello World。今集睇清楚：打 g++ 嗰陣，背後究竟發生咩事。",
          TitleCard(course.SERIES, ep.id, ep.part.zh, ep.title, "原始碼 · 程式檔 · 重新編譯")),
    Scene("goal",
          "今集會講：[[b1]]原始碼同程式檔有乜分別；[[b2]]a.out 同 -o 係乜；[[b3]]點解改完程式要重新編譯；[[b4]]仲有 -std=c++20 呢個選項。",
          BulletCard("今集學識", [("原始碼同程式檔有乜分別", "b1"), ("a.out 同 -o", "b2"),
                                ("改完程式，點解要重新編譯", "b3"), ("-std=c++20 係乜", "b4")])),
    Scene("flow",
          "重溫一下：[[src]]我哋寫嘅 hello.cpp 叫原始碼，係人睇得明嘅文字。[[cc]]g++ 係編譯器，[[exe]]佢將原始碼翻譯做程式檔，"
          "入面係電腦識行嘅機器碼。[[run]]我哋運行嘅，其實係呢個程式檔。",
          FlowCard("編譯做咗咩？", [Row("C++", "編譯過程", BLUE, [
              Node("原始碼", "hello.cpp", "src"), Node("編譯器", "g++", "cc"),
              Node("程式檔", "hello", "exe"), Node("運行", "./hello", "run"),
          ], note="原始碼係人睇嘅，程式檔係電腦行嘅", note_at="run")])),
    Scene("ls1",
          "我哋實際睇吓。[[ls]]打 ls，可以列出資料夾入面有咩檔案。而家得一個：hello.cpp。",
          s.scene(Open("hello.cpp", mode="instant"), Run(ls1, at="ls"))),
    Scene("aout",
          "[[cc]]如果淨係打 g++ hello.cpp，[[ls]]再 ls，會多咗個叫 a.out 嘅檔案。冇講個程式叫咩名，g++ 就會用 a.out 呢個預設名。"
          "[[run]]打 ./a.out，一樣行到。[[win]]喺 Windows，呢個預設名係 a.exe。",
          s.scene(Run(cc_a, at="cc"), Run(ls2, at="ls"), Run(run_a, at="run"),
                  Note("冇 -o：程式叫 a.out\nWindows：叫 a.exe", at="win"))),
    Scene("dash_o",
          "[[cc]]加個 -o hello，o 即係 output，意思係輸出去 hello 呢個名。[[ls]]再 ls，就見到 hello 呢個程式檔。"
          "[[note]]以後我哋都會用 -o，改個好名。",
          s.scene(Note(None), Run(cc_o, at="cc"), Run(ls3, at="ls"), Note("-o ＝ output\n自己改程式檔名", at="note"))),
    Scene("sizes",
          f"[[ls]]用 ls -l 睇吓檔案大細。[[note]]hello.cpp 只係得{zh_int(src)} byte，但係 hello 有{roughly(exe)} byte，"
          "因為入面係翻譯好嘅機器碼，仲有運行需要嘅其他資料。",
          s.scene(Note(None), Run(ll, at="ls"), Note(f"hello.cpp：{src} byte\nhello：{exe:,} byte", at="note", where="editor"))),
    Scene("edit",
          "而家改吓程式，[[edit]]將 Hello World 嘅 World，改做 Hong Kong，儲存。[[run]]唔編譯，直接再行 ./hello。"
          "[[out]]咦？點解仲係印 Hello, World？",
          s.scene(Note(None), Run(clear1), Replace("hello.cpp", "World", "Hong Kong", at="edit"), Expect("hello.cpp", NEW),
                  Run(run_old, at="run"), Note("改咗程式……\n但係仲係舊嘅輸出？", at="out")), seed=12),
    Scene("why_old",
          "因為[[src]]我哋改嘅係原始碼，[[exe]]但係行嘅係程式檔，佢仲係上次翻譯嗰個舊版本。[[recipe]]就好似改咗食譜，煮好咗嗰碟餸，唔會自己變。",
          TileCard("點解仲係舊嘅？", [
              Tile("📄", "原始碼 hello.cpp", "已經改咗：Hong Kong", "src", GREEN),
              Tile("💾", "程式檔 hello", "仲係上次翻譯嗰個：World", "exe", RED),
          ], cols=2, height=330, footer=("改咗食譜，煮好咗嘅餸唔會自己變", "recipe"))),
    Scene("recompile",
          "所以，[[cc]]每次改完程式，都要重新編譯，[[run]]再運行，先會見到 Hello, Hong Kong!。[[rule]]記住呢個次序：改、編譯、運行。",
          s.scene(Note(None), Run(cc_new, at="cc"), Run(run_new, at="run"), Note("改 → 編譯 → 運行", at="rule"))),
    Scene("std",
          "最後介紹多個選項。[[gpp]]g++ 後面，[[std]]加 -std=c++20，即係叫佢用 C++20 呢個版本嘅規則嚟翻譯。[[src]]然後係原始碼，"
          "[[out]]同埋 -o 程式名。[[def]]唔寫嘅話，我哋用嘅 g++ 預設係 C++17。呢個課程用 C++20，所以我哋都會咁樣編譯。",
          AnatomyCard("完整嘅編譯指令", [
              Part("g++", "編譯器", BLUE, "gpp"),
              Part(" -std=c++20", "用 C++20 規則", PURPLE, "std"),
              Part(" hello.cpp", "原始碼", GREEN, "src"),
              Part(" -o hello", "程式檔名", AMBER, "out"),
          ], note=("唔寫 -std：g++ 15 預設用 C++17", "def"))),
    Scene("std_run",
          "[[cc]]試吓用呢個完整指令編譯，[[run]]再運行，一樣冇問題。下一集，我哋仲會加多兩個好有用嘅選項。",
          s.scene(Note(None), Run(clear2), Run(cc_std, at="cc"), Run(run_std, at="run"))),
    Scene("recap",
          "總結一下：[[r1]]g++ 將原始碼翻譯做程式檔；[[r2]]冇 -o 就叫 a.out，-o 可以自己改名；[[r3]]改完程式，一定要重新編譯；"
          "[[r4]]-std=c++20 即係用 C++20 嘅規則。",
          BulletCard("今集重點", [("g++ 將原始碼翻譯做程式檔", "r1"), ("冇 -o 就叫 a.out；-o 自己改名", "r2"),
                                ("改完程式，一定要重新編譯", "r3"), ("-std=c++20：用 C++20 規則", "r4")])),
    Scene("outro",
          "小挑戰：[[ch]]整一個叫 bye 嘅程式，印出 Goodbye!，再用 ls 睇吓多咗咩檔案。"
          "[[next]]下一集，我哋會學點樣睇得明編譯錯誤。多謝收睇，下次見！",
          EndCard("整一個叫 bye 嘅程式，印出 Goodbye!，再用 ls 睇吓多咗咩檔案。",
                  f"下一集：{nxt.id} {nxt.title}", challenge_at="ch", next_at="next")),
]

build(N, scenes, opts)
